import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Career Insights by Job Level",
    layout="wide",
    page_icon="🍩"
)

st.title("🍩 Career Insights by Job Level")

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name='education_career_success')

df = load_data()

# Sidebar: Job Level Selection (single choice)
st.sidebar.header("🎯 Filter by Job Level")
job_levels = sorted(df['Current_Job_Level'].dropna().unique().tolist())
selected_level = st.sidebar.selectbox("Select one Job Level:", job_levels)

# Main page: Gender Filter
gender_options = df['Gender'].dropna().unique().tolist()
selected_gender = st.selectbox("🔍 Filter by Gender:", ["All"] + gender_options)

# Filter data based on Job Level
filtered_df = df[df['Current_Job_Level'] == selected_level]

# Further filter by Gender
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

# Function to generate donut chart without legend
def plot_donut(data, column, title):
    count_data = data[column].value_counts().reset_index()
    count_data.columns = [column, 'Count']
    fig = px.pie(
        count_data,
        names=column,
        values='Count',
        hole=0.5,
        title=title
    )
    fig.update_traces(textinfo='percent+label', showlegend=False)
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    return fig

# Layout: 3 donut charts
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(plot_donut(filtered_df, 'Entrepreneurship', 'Entrepreneurship'), use_container_width=True)

with col2:
    st.plotly_chart(plot_donut(filtered_df, 'Years_to_Promotion', 'Years to Promotion'), use_container_width=True)

with col3:
    st.plotly_chart(plot_donut(filtered_df, 'Field_of_Study', 'Field of Study'), use_container_width=True)

# Display number of records
st.markdown(f"### 👥 Total Records for '{selected_level}'{' and Gender: ' + selected_gender if selected_gender != 'All' else ''}: {len(filtered_df)}")
