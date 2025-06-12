import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import gaussian_kde
import numpy as np

st.set_page_config(layout="wide")

# Load and preprocess data
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

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

# Check if enough data exists
if filtered_df.empty or filtered_df['Gender'].nunique() < 2:
    st.write("Not enough data to display charts.")
else:
    # Prepare data
    genders = filtered_df['Gender'].unique()
    gender_counts = filtered_df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    # Create combined figure
    fig_combined = make_subplots(
        rows=1, col
