import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np

st.set_page_config(page_title="Entrepreneurship & Demographics", layout="wide")

# Load and preprocess data
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")

# Gender filter (with 'All')
gender_options = ['All'] + sorted(df['Gender'].dropna().unique())
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)
if selected_gender != 'All':
    df = df[df['Gender'] == selected_gender]

# Dropdown Job Level
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)
df = df[df['Current_Job_Level'] == selected_level]

# Age range slider
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))
df = df[df['Age'].between(age_range[0], age_range[1])]

# Entrepreneurship status (checkbox style)
entrepreneur_options = ['Yes', 'No']
selected_statuses = st.sidebar.multiselect("Select Entrepreneurship Status", entrepreneur_options, default=entrepreneur_options)
df = df[df['Entrepreneurship'].isin(selected_statuses)]

# --- Tabs for Graphs ---
tab1, tab2 = st.tabs(["📊 Entrepreneurship & Job Offers", "📈 Demographics Analysis"])

# TAB 1
with tab1:
    st.title("\U0001F4C8 Entrepreneurship and Job Offers by Age")
    st.markdown("Analyze the relationship between entrepreneurship status, job level, and job offers across age groups.")

    # Color mapping
    color_map = {'Yes': '#FFD700', 'No': '#004080'}

    # Grouped data for percentage bar chart
    df_grouped = (
        df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
        .size()
        .reset_index(name='Count')
    )
    df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

    df_bar = df_grouped[df_grouped['Entrepreneurship'].isin(selected_statuses)]

    even_ages = sorted(df_bar['Age'].unique())
    even_ages = [age for age in even_ages if age % 2 == 0]

    # Bar chart
    fig_bar = px.bar(
        df_bar,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': sorted(df_bar['Age'].unique())},
        labels={'Age': 'Age', 'Percentage': 'Percentage'},
        height=450,
        width=1250,
        title=f"Entrepreneurship Distribution by Age – {selected_level} Level"
    )

    fig_bar.update_traces(
        hovertemplate="Entrepreneurship=%{customdata[0]}<br>Age=%{x}<br>Percentage=%{y:.0%}<extra></extra>",
        customdata=df_bar[['Entrepreneurship']].values,
        hoverinfo="skip"
    )

    fig_bar.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=0,
        bargap=0.1,
        xaxis=dict(tickvals=even_ages),
        yaxis=dict(title="Percentage", range=[0, 1], tickformat=".0%"),
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
    )

    # Line chart: Average Job Offers
    df_avg_offers = (
        df[df['Entrepreneurship'].isin(selected_statuses)]
        .groupby(['Age', 'Entrepreneurship'])['Job_Offers']
        .mean()
        .reset_index()
    )

    fig_line = go.Figure()

    for status in selected_statuses:
        data_status = df_avg_offers[df_avg_offers["Entrepreneurship"] == status]
        fig_line.add_trace(go.Scatter(
            x=data_status["Age"],
            y=data_status["Job_Offers"],
            mode="lines+markers",
            name=status,
            line=dict(color=color_map[status], width=2),
            marker=dict(size=6),
            hovertemplate="%{y:.2f}"
        ))

    fig_line.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=0,
        hovermode="x unified",
        width=1250,
        xaxis=dict(
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikethickness=1.2,
            spikedash='dot',
            tickvals=even_ages
        ),
        yaxis=dict(
            title="Average Job Offers",
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikethickness=1.2,
            spikedash='dot'
        ),
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_line, use_container_width=True)

# TAB 2
with tab2:
    st.title("\U0001F4CA Demographic Analysis")

    chart_option = st.selectbox("Select Variable for Visualization", ['Gender', 'Field of Study'])

    if df.empty:
        st.write("Not enough data to display charts.")
    else:
        col1, col2 = st.columns([1, 1])

        # Density Chart
        with col1:
            fig_density = go.Figure()

            if chart_option == 'Gender':
                categories = df['Gender'].unique()
                title = "Age Distribution by Gender (Area Chart)"
                group_col = 'Gender'
            else:
                categories = df['Field_of_Study'].dropna().unique()
                title = "Age Distribution by Field of Study"
                group_col = 'Field_of_Study'

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
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title=title,
                xaxis_title="Age",
                yaxis_title="Density",
                height=500,
                margin=dict(t=40, l=40, r=40, b=80),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.35,
                    xanchor="center",
                    x=0.5
                )
            )
            st.plotly_chart(fig_density, use_container_width=True)

        # Donut Chart
        with col2:
            if chart_option == 'Gender':
                counts = df['Gender'].value_counts().reset_index()
                counts.columns = ['Gender', 'Count']
                fig_donut = go.Figure(data=[go.Pie(
                    labels=counts['Gender'],
                    values=counts['Count'],
                    hole=0.5
                )])
                fig_donut.update_layout(title="Gender Distribution (Donut Chart)")
            else:
                counts = df['Field_of_Study'].value_counts().reset_index()
                counts.columns = ['Field of Study', 'Count']
                fig_donut = go.Figure(data=[go.Pie(
                    labels=counts['Field of Study'],
                    values=counts['Count'],
                    hole=0.5
                )])
                fig_donut.update_layout(title="Field of Study Distribution (Donut Chart)")

            fig_donut.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=350,
                margin=dict(t=40, l=40, r=40, b=40),
                showlegend=True
            )
            st.plotly_chart(fig_donut, use_container_width=True)
