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

# Filter data based on selection
filtered_df = df[df['Current_Job_Level'] == selected_level]

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
    st.plotly_chart(plot_donut(filtered_df, 'Gender', 'Gender Distribution'), use_container_width=True)

with col2:
    st.plotly_chart(plot_donut(filtered_df, 'Years_to_Promotion', 'Years to Promotion'), use_container_width=True)

with col3:
    st.plotly_chart(plot_donut(filtered_df, 'Field_of_Study', 'Field of Study'), use_container_width=True)

# Display number of records
st.markdown(f"### 👥 Total Records for '{selected_level}': {len(filtered_df)}")

# === Stacked Bar Chart for Years to Promotion by Age ===
st.subheader("Job Level vs. Age by Entrepreneurship")

df2 = df[df['Entrepreneurship'].isin(['Yes', 'No'])]
df_grouped = df2.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels = st.multiselect("Select Job Levels", job_levels, default=job_levels, key="level_selector")
min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())
age_range = st.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age), key="age_slider")
selected_statuses = st.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'], key="status_selector")

filtered = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_levels)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]

color_map2 = {'Yes': '#FFD700', 'No': '#004080'}
level_order = ['Entry', 'Executive', 'Mid', 'Senior']
visible_levels = [lvl for lvl in level_order if lvl in selected_levels]

for level in visible_levels:
    data = filtered[filtered['Current_Job_Level'] == level]
    if data.empty:
        st.write(f"### {level} – No data available")
        continue

    ages = sorted(data['Age'].unique())

    fig_bar = px.bar(
        data,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map2,
        height=400,
        width=500,
        title=f"{level} Level – Entrepreneurship by Age (%)"
    )
    fig_bar.update_layout(margin=dict(t=30, l=30, r=30, b=30), legend_title_text='Entrepreneurship', xaxis_tickangle=90)
    fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

    fig_area = px.area(
        data,
        x='Age',
        y='Count',
        color='Entrepreneurship',
        markers=True,
        color_discrete_map=color_map2,
        height=400,
        width=500,
        title=f"{level} Level – Entrepreneurship by Age (Count)"
    )
    for status in ['Yes', 'No']:
        avg_age = data[data['Entrepreneurship'] == status]['Age'].mean()
        fig_area.add_vline(x=avg_age, line_dash="dot", line_color=color_map2[status], line_width=1.2)
        fig_area.add_trace(go.Scatter(
            x=[None], y=[None], mode='markers',
            marker=dict(symbol='circle', size=10, color=color_map2[status]),
            name=f"{status} Avg Age: {avg_age:.1f}"
        ))
    fig_area.update_traces(line=dict(width=2), marker=dict(size=8))
    fig_area.update_layout(margin=dict(t=30, l=30, r=30, b=30), legend_title_text='Entrepreneurship')

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col_b:
        st.plotly_chart(fig_area, use_container_width=True)
