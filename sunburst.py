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

# Biểu đồ với màu gradient đẹp
fig = px.sunburst(
    sunburst_data,
    path=['Entrepreneurship', 'Field_of_Study', 'Salary_Group'],
    values='Percentage',
    color='Percentage',
    color_continuous_scale='Viridis',  # 🎨 Gradient đẹp mắt
    title='🌿 Sunburst Chart – Salary Distribution'
)

fig.update_traces(maxdepth=2, branchvalues="total")
fig.update_coloraxes(colorbar_title="Percentage (%)")  # Hiển thị thanh màu
st.plotly_chart(fig, use_container_width=True)
