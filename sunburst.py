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

# Tạo color key cho mỗi tổ hợp Yes/No + ngành
sunburst_data['Color_Key'] = sunburst_data['Entrepreneurship'] + " / " + sunburst_data['Field_of_Study']

# Tạo bảng màu riêng biệt
yes_fields = sunburst_data[sunburst_data['Entrepreneurship'] == 'Yes']['Field_of_Study'].unique()
no_fields = sunburst_data[sunburst_data['Entrepreneurship'] == 'No']['Field_of_Study'].unique()

yes_colors = px.colors.qualitative.Set2
no_colors = px.colors.qualitative.Pastel1

color_discrete_map = {}

for i, field in enumerate(yes_fields):
    color_discrete_map[f"Yes / {field}"] = yes_colors[i % len(yes_colors)]
for i, field in enumerate(no_fields):
    color_discrete_map[f"No / {field}"] = no_colors[i % len(no_colors)]

# Vẽ biểu đồ
fig = px.sunburst(
    sunburst_data,
    path=['Ent_Label', 'Field_Label', 'Salary_Label'],
    values='Count',
    color='Color_Key',
    color_discrete_map=color_discrete_map,
    title='🌞 Sunburst Chart – Mỗi ngành 1 màu, Yes/No phân biệt rõ'
)

fig.update_traces(maxdepth=2, branchvalues="total")
st.plotly_chart(fig, use_container_width=True)
