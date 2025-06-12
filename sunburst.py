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

# Sidebar Filters
st.sidebar.title("🎯 Filter Options")

# Gender filter (multi)
genders = sorted(df['Gender'].dropna().unique())
selected_genders = st.sidebar.multiselect("Select Gender", genders, default=genders)

# Job level filter (single)
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Apply filters to base dataframe
df_filtered = df[
    (df['Gender'].isin(selected_genders)) &
    (df['Current_Job_Level'] == selected_level)
]

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

# Age filter (chỉ lấy từ df_filtered)
min_age, max_age = int(df_filtered['Age'].min()), int(df_filtered['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Entrepreneurship filter
selected_statuses = st.sidebar.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])

# Nhóm lại dữ liệu theo các tiêu chí
df_grouped = (
    df_filtered.groupby(['Age', 'Entrepreneurship'])
      .size()
      .reset_index(name='Count')
)
df_grouped['Percentage'] = df_grouped.groupby('Age')['Count'].transform(lambda x: x / x.sum())

# Áp dụng filter tuổi và status
filtered = df_grouped[
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]
