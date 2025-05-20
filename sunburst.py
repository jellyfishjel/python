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

# Gán nhãn
sunburst_data['Ent_Label'] = sunburst_data['Entrepreneurship']
sunburst_data['Field_Label'] = sunburst_data['Field_of_Study']
sunburst_data['Salary_Label'] = sunburst_data['Salary_Group']
sunburst_data['Color_Key'] = sunburst_data['Entrepreneurship'] + " / " + sunburst_data['Field_of_Study']

# Màu theo ngành học
field_colors = {
    'Engineering': '#1f77b4',       # Blue
    'Business': '#ff7f0e',          # Orange
    'Arts': '#2ca02c',              # Green
    'Science': '#d62728',           # Red
    'IT': '#9467bd',                # Purple
    'Education': '#8c564b',         # Brown
    'Medicine': '#e377c2',          # Pink
    'Law': '#7f7f7f',               # Gray
    'Social Science': '#bcbd22',    # Yellow-green
    'Other': '#17becf'              # Cyan
}

# Gán màu cho mỗi tổ hợp "Yes / Ngành" và "No / Ngành"
color_discrete_map = {}
for field, color in field_colors.items():
    color_discrete_map[f'Yes / {field}'] = color
    color_discrete_map[f'No / {field}'] = color

# Vẽ biểu đồ
fig = px.sunburst(
    sunburst_data,
    path=['Ent_Label', 'Field_Label', 'Salary_Label'],
    values='Count',
    color='Color_Key',
    color_discrete_map=color_discrete_map,
    title='🌞 Sunburst Chart'
)

# Hiện nhãn và phần trăm
fig.update_traces(textinfo='label+percent entry', insidetextorientation='radial')

# Ẩn thanh màu và legend
fig.update_layout(showlegend=False)

# Hiển thị biểu đồ
st.plotly_chart(fig, use_container_width=True)
