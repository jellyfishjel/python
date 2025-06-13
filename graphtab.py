import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

# PAGE CONFIG
st.set_page_config(page_title="Education & Career Insights", layout="wide", page_icon="📊")

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# SIDEBAR FILTERS
st.sidebar.title("Filters")

# Gender filter
gender_options = ['All'] + sorted(df['Gender'].dropna().unique())
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)
if selected_gender != 'All':
    df = df[df['Gender'] == selected_gender]

# Job Level
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)
df = df[df['Current_Job_Level'] == selected_level]

# Age Range
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))
df = df[df['Age'].between(age_range[0], age_range[1])]

# Entrepreneurship
entrepreneur_options = ['All', 'Yes', 'No']
selected_status = st.sidebar.selectbox("Select Entrepreneurship Status", entrepreneur_options)
selected_statuses = ['Yes', 'No'] if selected_status == 'All' else [selected_status]
df = df[df['Entrepreneurship'].isin(selected_statuses)]

# MAIN PAGE
st.title("📊 Career and Education Insights")
st.markdown("Analyze the relationship between demographics, entrepreneurship, and job offers.")

tab1, tab2 = st.tabs(["Entrepreneurship & Job Offers", "Demographics Visualization"])

# -------- TAB 1 -------- #
with tab1:
    st.subheader("Entrepreneurship and Job Offers by Age")

    # Grouped data for bar chart
    df_grouped = (
        df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
        .size()
        .reset_index(name='Count')
    )
    df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())
    df_bar = df_grouped

    even_ages = sorted(df_bar['Age'].unique())
    even_ages = [age for age in even_ages if age % 2 == 0]
    color_map = {'Yes': '#FFD700', 'No': '#004080'}

    fig_bar = px.bar(
        df_bar,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes']},
        labels={'Age': 'Age', 'Percentage': 'Percentage'},
        height=450,
        width=1250,
        title=f"Entrepreneurship Distribution by Age – {selected_level} Level"
    )
    fig_bar.update_traces(
        hovertemplate="Entrepreneurship=%{customdata[0]}<br>Age=%{x}<br>Percentage=%{y:.0%}<extra></extra>",
        customdata=df_bar[['Entrepreneurship']].values
    )
    fig_bar.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        xaxis=dict(tickvals=even_ages),
        yaxis=dict(title="Percentage", range=[0, 1], tickformat=".0%"),
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
    )

    # Line chart: Average Job Offers
    df_avg = df.groupby(['Age', 'Entrepreneurship'])['Job_Offers'].mean().reset_index()

    fig_line = go.Figure()
    for status in selected_statuses:
        temp = df_avg[df_avg['Entrepreneurship'] == status]
        fig_line.add_trace(go.Scatter(
            x=temp['Age'],
            y=temp['Job_Offers'],
            mode="lines+markers",
            name=status,
            line=dict(color=color_map[status], width=2),
            marker=dict(size=6),
            hovertemplate="%{y:.2f}"
        ))
    fig_line.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        hovermode="x unified",
        width=1250,
        xaxis=dict(tickvals=even_ages, title="Age"),
        yaxis=dict(title="Average Job Offers"),
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_line, use_container_width=True)

# -------- TAB 2 -------- #
with tab2:
    st.subheader("Age Distribution & Category Proportions")

    chart_option = st.selectbox("Select Variable for Visualization", ['Gender', 'Field of Study'])

    col1, col2 = st.columns(2)

    # ----- AREA CHART -----
    with col1:
        fig_density = go.Figure()
        if chart_option == 'Gender':
            categories = df['Gender'].dropna().unique()
            group_col = 'Gender'
            title = "Age Distribution by Gender"
        else:
            categories = df['Field_of_Study'].dropna().unique()
            group_col = 'Field_of_Study'
            title = "Age Distribution by Field of Study"

        for cat in categories:
            age_data = df[df[group_col] == cat]['Age']
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
            margin=dict(t=40, l=40, r=40, b=80),
            legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
        )
        st.plotly_chart(fig_density, use_container_width=True)

    # ----- DONUT CHART -----
    with col2:
        if chart_option == 'Gender':
            counts = df['Gender'].value_counts().reset_index()
            counts.columns = ['Gender', 'Count']
            labels = counts['Gender']
            values = counts['Count']
            title = "Gender Distribution"
        else:
            counts = df['Field_of_Study'].value_counts().reset_index()
            counts.columns = ['Field of Study', 'Count']
            labels = counts['Field of Study']
            values = counts['Count']
            title = "Field of Study Distribution"

        fig_donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
        fig_donut.update_layout(
            title=title,
            height=350,
            margin=dict(t=40, l=40, r=40, b=40),
            legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
