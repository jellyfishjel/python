import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np

st.set_page_config(page_title="Entrepreneurship Analysis", layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

st.title("📊 Entrepreneurship and Job Offers by Age")
st.markdown("Analyze the relationship between entrepreneurship status, job level, and job offers across age groups.")

st.sidebar.title("Filter Options")

# Gender filter (multi-select with 'All')
gender_options = sorted(df['Gender'].dropna().unique())
selected_genders = st.sidebar.multiselect("Select Gender", options=['All'] + gender_options, default=['All'])
if 'All' not in selected_genders:
    df = df[df['Gender'].isin(selected_genders)]

# Job level filter
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Age filter
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Entrepreneurship filter (checkboxes with 'All')
st.sidebar.markdown("**Select Entrepreneurship Status**")
status_yes = st.sidebar.checkbox("Yes", value=True)
status_no = st.sidebar.checkbox("No", value=True)
selected_statuses = []
if status_yes:
    selected_statuses.append("Yes")
if status_no:
    selected_statuses.append("No")

# Color mapping
color_map = {'Yes': '#FFD700', 'No': '#004080'}

# Grouped data for percentage bar chart
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
    .size()
    .reset_index(name='Count')
)
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Filter bar data
df_bar = df_grouped[
    (df_grouped['Current_Job_Level'] == selected_level) &
    (df_grouped['Age'].between(age_range[0], age_range[1])) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses))
]

# Filter only even ages for ticks
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
    df[(df['Current_Job_Level'] == selected_level) &
       (df['Entrepreneurship'].isin(selected_statuses)) &
       (df['Age'].between(age_range[0], age_range[1]))]
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

# Display charts
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_bar, use_container_width=True)
with col2:
    st.plotly_chart(fig_line, use_container_width=True)
