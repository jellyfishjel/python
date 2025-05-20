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

# Tạo nhãn
sunburst_data['Ent_Label'] = sunburst_data['Entrepreneurship']
sunburst_data['Field_Label'] = sunburst_data['Field_of_Study']
sunburst_data['Salary_Label'] = sunburst_data['Salary_Group']
sunburst_data['Color_Key'] = sunburst_data['Entrepreneurship'] + " / " + sunburst_data['Field_of_Study']

# Màu gốc cho từng ngành
base_colors = {
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

# Hàm làm nhạt màu (pha trắng)
def lighten_color(hex_color, factor=0.5):
    hex_color = hex_color.lstrip('#')
    rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    light_rgb = [int((1 - factor) * c + factor * 255) for c in rgb]
    return '#' + ''.join(f'{c:02x}' for c in light_rgb)

# Tạo color_discrete_map cho từng tổ hợp Yes/No + Ngành
color_discrete_map = {}
for field, base in base_colors.items():
    color_discrete_map[f"Yes / {field}"] = base
    color_discrete_map[f"No / {field}"] = lighten_color(base, factor=0.5)

# Vẽ biểu đồ
fig = px.sunburst(
    sunburst_data,
    path=['Ent_Label', 'Field_Label', 'Salary_Label'],
    values='Count',
    color='Color_Key',
    color_discrete_map=color_discrete_map,
    title='🌞 Sunburst Chart'
)

fig.update_traces(maxdepth=2, branchvalues="total")
st.plotly_chart(fig, use_container_width=True)
