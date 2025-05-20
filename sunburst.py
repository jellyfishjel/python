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

# Thêm dòng giả để gán màu cho 'Yes' và 'No' ở vòng trong
yes_total = sunburst_data[sunburst_data['Ent_Label'] == 'Yes']['Count'].sum()
no_total = sunburst_data[sunburst_data['Ent_Label'] == 'No']['Count'].sum()

extra_rows = pd.DataFrame([
    {'Ent_Label': 'Yes', 'Field_Label': '', 'Salary_Label': '', 'Count': yes_total, 'Ent_Field': 'Yes'},
    {'Ent_Label': 'No', 'Field_Label': '', 'Salary_Label': '', 'Count': no_total, 'Ent_Field': 'No'}
])

# Nối thêm vào sunburst_data
sunburst_data = pd.concat([sunburst_data, extra_rows], ignore_index=True)

# Gán màu cho 'Yes' và 'No'
color_map['Yes'] = '#d49c6c'  # cam trung tính
color_map['No'] = '#78c2d8'   # xanh pastel


# Màu cho Entrepreneurship = Yes (xanh biển đậm)
yes_colors = {
    'Engineering': '#d2a56d',
    'Business': '#ce8b54',
    'Arts': '#bd7e4a',
    'Computer Science': '#ccaa87',
    'Medicine': '#83502e',
    'Law': '#96613d',
    'Mathematics': '#bd9c7b'
}

# Màu cho Entrepreneurship = No (xanh lá)
no_colors = {
    'Engineering': '#009ac7',
    'Business': '#03396c',
    'Arts': '#005b96',
    'Computer Science': '#8ed2ed',
    'Medicine': '#0a70a9',
    'Law': '#5dc4e1',
    'Mathematics': '#b3cde0'
}

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


# Hiển thị biểu đồ
st.plotly_chart(fig, use_container_width=True)
