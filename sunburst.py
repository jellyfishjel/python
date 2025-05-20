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

# Gom nhóm
sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')

# Tạo nhãn đơn giản cho từng cấp
sunburst_data['Ent_Label'] = sunburst_data['Entrepreneurship']
sunburst_data['Field_Label'] = sunburst_data['Field_of_Study']
sunburst_data['Salary_Label'] = sunburst_data['Salary_Group']

color_discrete_map = {
    "Yes": "#1f77b4",  # xanh dương
    "No": "#ffffff"    # trắng
}

# Mỗi ngành 1 màu
field_colors = {
    'Engineering': '#1f77b4',
    'Business': '#ff7f0e',
    'Arts': '#2ca02c',
    'Science': '#d62728',
    'IT': '#9467bd',
    'Education': '#8c564b',
    'Medicine': '#e377c2',
    'Law': '#7f7f7f',
    'Social Science': '#bcbd22',
    'Other': '#17becf'
}

# Vẽ biểu đồ – dùng màu theo Field
fig = px.sunburst(
    sunburst_data,
    path=['Ent_Label', 'Field_Label', 'Salary_Label'],
    values='Count',
    color='Field_Label',  # Dựa vào ngành để tô màu
    color_discrete_map=field_colors,
    title='🌞 Sunburst Chart'
)

# Hiện phần trăm và label
fig.update_traces(
    textinfo='label+percent entry',
    insidetextorientation='radial',
    maxdepth=2,
    branchvalues="total"
)

# Ẩn legend (nếu muốn)
fig.update_layout(showlegend=False)

# Hiển thị biểu đồ
st.plotly_chart(fig, use_container_width=True)
