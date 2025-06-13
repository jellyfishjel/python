import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np

st.set_page_config(layout="wide")

# Load and preprocess data
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Sidebar filters
st.sidebar.title("Filters")

# Dropdown Job Level
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Age range slider
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Dropdown for Entrepreneurship status
status_options = ['All', 'Yes', 'No']
selected_status = st.sidebar.selectbox("Select Entrepreneurship Status", status_options)

# Filter data based on selections
filtered_df = df[df['Current_Job_Level'] == selected_level]
filtered_df = filtered_df[filtered_df['Age'].between(age_range[0], age_range[1])]

if selected_status != 'All':
    filtered_df = filtered_df[filtered_df['Entrepreneurship'] == selected_status]

# Select variable to visualize
chart_option = st.selectbox("Select Variable for Visualization", ['Gender', 'Field of Study'])

# Check if enough data exists
if filtered_df.empty:
    st.write("Not enough data to display charts.")
else:
    col1, col2 = st.columns([1, 1]) 

    # ----- DENSITY CHART (Area) -----
    with col1:
        fig_density = go.Figure()

        if chart_option == 'Gender':
            categories = filtered_df['Gender'].unique()
            title = "Age Distribution by Gender (Area Chart)"
            group_col = 'Gender'

        elif chart_option == 'Field of Study':
            categories = filtered_df['Field_of_Study'].dropna().unique()
            title = "Age Distribution by Field of Study"
            group_col = 'Field_of_Study'

        for cat in categories:
            age_data = filtered_df[filtered_df[group_col] == cat]['Age']

            if len(age_data) > 1:
                kde = gaussian_kde(age_data)
                x_vals = np.linspace(age_range[0], age_range[1], 100)
                y_vals = kde(x_vals)

                fig_density.add_trace(go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode='lines',
                    name=str(cat),
                    fill='tozeroy'
                ))

        fig_density.update_layout(
            title=title,
            xaxis_title="Age",
            yaxis_title="Density",
            height=500,
            margin=dict(t=40, l=40, r=40, b=80),  # tăng b để chừa chỗ cho legend bên dưới
            legend=dict(
                orientation="h",         # horizontal
                yanchor="bottom",
                y= 0.5,                  # khoảng cách dưới biểu đồ
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig_density, use_container_width=True)


    # ----- DONUT CHART -----
    with col2:
        if chart_option == 'Gender':
            gender_counts = filtered_df['Gender'].value_counts().reset_index()
            gender_counts.columns = ['Gender', 'Count']
            fig_donut = go.Figure(data=[go.Pie(
                labels=gender_counts['Gender'],
                values=gender_counts['Count'],
                hole=0.5
            )])
            fig_donut.update_layout(title="Gender Distribution (Donut Chart)")

        elif chart_option == 'Field of Study':
            field_counts = filtered_df['Field_of_Study'].value_counts().reset_index()
            field_counts.columns = ['Field of Study', 'Count']
            fig_donut = go.Figure(data=[go.Pie(
                labels=field_counts['Field of Study'],
                values=field_counts['Count'],
                hole=0.5
            )])
            fig_donut.update_layout(title="Field of Study Distribution (Donut Chart)")

        fig_donut.update_layout(
            height=350,
            margin=dict(t=40, l=40, r=40, b=40),
            showlegend=True
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
