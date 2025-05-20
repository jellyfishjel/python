import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sunburst Chart", layout="wide")
st.title("🌞 Sunburst Chart – Salary, Field, and Entrepreneurship")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name='education_career_success')

df = load_data()

# Nhóm lương
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

# Tạo dữ liệu cho biểu đồ
sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')
total = sunburst_data['Count'].sum()
sunburst_data['Percentage'] = (sunburst_data['Count'] / total * 100).round(2)

# Tạo biểu đồ
fig = px.sunburst(
    sunburst_data,
    path=['Entrepreneurship', 'Field_of_Study', 'Salary_Group'],
    values='Percentage',
    title='🌞 Sunburst Chart – Grouped by Salary'
)

fig.update_traces(maxdepth=2, branchvalues="total")
st.plotly_chart(fig, use_container_width=True)
