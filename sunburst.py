import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Education & Career Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

df = load_data()

# Categorize salary
def categorize_salary(salary):
    if salary < 30000:
        return '<30K'
    elif salary < 50000:
        return '30K–50K'
    elif salary < 70000:
        return '50K–70K'
    else:
        return '70K+'

df['Salary_Group'] = df['Starting_Salary'].apply(categorize_salary)

# Sidebar filters
st.sidebar.title("🔍 Filters")

job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

df_filtered = df[
    (df['Current_Job_Level'] == selected_level) &
    (df['Age'].between(age_range[0], age_range[1]))
]

st.title("🚀 Education & Career Success Dashboard")
st.subheader(f"Job Level: {selected_level}")

# Donut charts
cols = st.columns(3)

for i, col in enumerate(['Gender', 'Field_of_Study', 'Salary_Group']):
    group_data = df_filtered[col].value_counts().reset_index()
    group_data.columns = [col, 'Count']
    fig = px.pie(
        group_data,
        names=col,
        values='Count',
        hole=0.5,
        title=col,
    )
    fig.update_layout(showlegend=False, height=400, margin=dict(t=40, l=40, r=40, b=40))
    cols[i].plotly_chart(fig, use_container_width=True)

# Group data for bar/area charts
grouped = df_filtered.groupby(['Age', 'Salary_Group']).size().reset_index(name='Count')
grouped['Percentage'] = grouped.groupby('Age')['Count'].transform(lambda x: x / x.sum())

# Define color mapping
color_map = {
    '<30K': '#d73027',
    '30K–50K': '#fc8d59',
    '50K–70K': '#91bfdb',
    '70K+': '#4575b4'
}

ages = sorted(grouped['Age'].unique())

# Stacked Bar Chart (Percentage)
fig_bar = px.bar(
    grouped,
    x='Age',
    y='Percentage',
    color='Salary_Group',
    barmode='stack',
    color_discrete_map=color_map,
    category_orders={'Age': ages, 'Salary_Group': list(color_map.keys())},
    labels={'Percentage': 'Percentage'},
    height=400,
    title=f"{selected_level} Level – Salary Group by Age (%)"
)

fig_bar.update_layout(margin=dict(t=40, l=40, r=40, b=40))
fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

# Area Chart (Count)
fig_area = px.area(
    grouped,
    x='Age',
    y='Count',
    color='Salary_Group',
    markers=True,
    color_discrete_map=color_map,
    category_orders={'Age': ages, 'Salary_Group': list(color_map.keys())},
    labels={'Count': 'Count'},
    height=400,
    title=f"{selected_level} Level – Salary Group by Age (Count)"
)
fig_area.update_traces(line=dict(width=2), marker=dict(size=8))
fig_area.update_layout(margin=dict(t=40, l=40, r=40, b=40))
fig_area.update_yaxes(title="Count")

# Display both charts side-by-side
col1, col2 = st.columns(2)
col1.plotly_chart(fig_bar, use_container_width=True)
col2.plotly_chart(fig_area, use_container_width=True)
