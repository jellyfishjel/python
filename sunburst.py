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

# Tạo cột nối tên để đánh màu riêng theo Entrepreneurship + Field
sunburst_data['Ent_Field'] = sunburst_data['Entrepreneurship'] + " - " + sunburst_data['Field_of_Study']

# Màu cho Entrepreneurship = Yes (xanh biển đậm)
yes_colors = {
    'Engineering': '#003366',
    'Business': '#004080',
    'Arts': '#0059b3',
    'Computer Science': '#0073e6',
    'Medicine': '#3399ff',
    'Law': '#66b3ff',
    'Mathematics': '#99ccff'
}

# Màu cho Entrepreneurship = No (xanh lá)
no_colors = {
    'Engineering': '#009ac7',
    'Business': '#03396c',
    'Arts': '#005b96',
    'Computer Science': '#8ed2ed',
    'Medicine': '#b3cde0',
    'Law': '#5dc4e1',
    'Mathematics': '#0a70a9'
}

# Tạo dictionary màu cho Ent_Field
color_map = {}

for ent in ['Yes', 'No']:
    for field in yes_colors.keys():
        key = f"{ent} - {field}"
        if ent == 'Yes':
            color_map[key] = yes_colors[field]
        else:
            color_map[key] = no_colors[field]

# Vẽ biểu đồ với color là cột 'Ent_Field'
fig = px.sunburst(
    sunburst_data,
    path=['Ent_Label', 'Field_Label', 'Salary_Label'],
    values='Count',
    color='Ent_Field',
    color_discrete_map=color_map,
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
