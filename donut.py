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
chart_option = st.selectbox("Select Variable for Visualization", 
                            ['Gender', 'Field of Study', 'Years to Promotion'])

# Check if enough data exists
if filtered_df.empty:
    st.write("Not enough data to display charts.")
else:
    col1, col2 = st.columns(2)

    # ----- DENSITY CHART -----
    with col1:
        fig_density = go.Figure()

        if chart_option == 'Gender':
            categories = filtered_df['Gender'].unique()
            title = "Age Distribution by Gender (Area Chart)"
            group_col = 'Gender'

        elif chart_option == 'Field of Study':
            categories = filtered_df['Field_of_Study'].value_counts().nlargest(6).index  # Top 6 fields
            title = "Age Distribution by Field of Study (Top 6)"
            group_col = 'Field_of_Study'

        elif chart_option == 'Years to Promotion':
            promo_bins = pd.cut(filtered_df['Years_to_Promotion'], bins=[-1, 1, 3, 5, np.inf],
                                labels=['0-1 yrs', '2-3 yrs', '4-5 yrs', '6+ yrs'])
            filtered_df['Promo_Group'] = promo_bins
            categories = filtered_df['Promo_Group'].dropna().unique()
            title = "Age Distribution by Years to Promotion Group"
            group_col = 'Promo_Group'

        for cat in categories:
            if chart_option == 'Years to Promotion':
                age_data = filtered_df[filtered_df['Promo_Group'] == cat]['Age']
            else:
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
            margin=dict(t=40, l=40, r=40, b=40)
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

        elif chart_option == 'Years to Promotion':
            promo_bins = pd.cut(filtered_df['Years_to_Promotion'], bins=[-1, 1, 3, 5, np.inf],
                                labels=['0-1 yrs', '2-3 yrs', '4-5 yrs', '6+ yrs'])
            promo_counts = promo_bins.value_counts().sort_index().reset_index()
            promo_counts.columns = ['Years to Promotion', 'Count']
            fig_donut = go.Figure(data=[go.Pie(
                labels=promo_counts['Years to Promotion'],
                values=promo_counts['Count'],
                hole=0.5
            )])
            fig_donut.update_layout(title="Years to Promotion (Donut Chart)")

        fig_donut.update_layout(
            height=500,
            margin=dict(t=40, l=40, r=40, b=40),
            showlegend=True
        )
        st.plotly_chart(fig_donut, use_container_width=True)
