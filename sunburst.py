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

# Gán nhãn cho từng cấp
sunburst_data['Ent_Label'] = sunburst_data['Entrepreneurship']
sunburst_data['Field_Label'] = sunburst_data['Field_of_Study']
sunburst_data['Salary_Label'] = sunburst_data['Salary_Group']

# Màu cho Entrepreneurship
ent_colors = {
    'Yes': '#1f77b4',   # xanh dương
    'No': '#ffffff'     # trắng
}

# Màu cho ngành học
field_colors = {
    'Engineering': '#ff7f0e',
    'Business': '#2ca02c',
    'Arts': '#d62728',
    'Science': '#9467bd',
    'IT': '#8c564b',
    'Education': '#8c564b',
    'Medicine': '#e377c2',
    'Law': '#7f7f7f',
    'Social Science': '#bcbd22',
    'Other': '#17becf'
}

# Hàm lấy màu theo cấp độ
def get_color(row, level):
    if level == 0:  # Entrepreneurship
        return ent_colors.get(row['Ent_Label'], '#cccccc')
    elif level == 1:  # Field_of_Study
        return field_colors.get(row['Field_Label'], '#999999')
    else:  # Salary or else
        return '#dddddd'

# Tạo cột màu cho plotly
# plotly sunburst dùng 1 cột color duy nhất, ta lấy màu của Field_Label khi level=1,
# còn tầng 0 lấy màu của Ent_Label
def assign_color(row):
    # Khi vẽ sunburst, mỗi row là 1 tổ hợp (Ent, Field, Salary),
    # ta ưu tiên màu ngành ở tầng 1, và màu yes/no ở tầng 0.
    # Ở đây ta chọn màu theo tầng 1 (Field_Label)
    return field_colors.get(row['Field_Label'], '#999999')

sunburst_data['Color'] = sunburst_data.apply(assign_color, axis=1)

# Vẽ biểu đồ
fig = px.sunburst(
    sunburst_data,
    path=['Ent_Label', 'Field_Label', 'Salary_Label'],
    values='Count',
    color='Color',
    title='🌞 Sunburst Chart',
)

fig.update_traces(
    textinfo='label+percent entry',
    insidetextorientation='radial',
    maxdepth=2,
    branchvalues="total"
)

# Để màu Yes / No ở tầng 0 khác biệt (xanh dương vs trắng),
# ta thêm layout cho nền trắng cho No và màu xanh cho Yes bằng cách sửa trace.
# Nhưng plotly không hỗ trợ trực tiếp, nên ta chỉ dùng màu nền mặc định cho No bằng trắng
# và màu ngành riêng ở tầng 1.

# Ẩn legend
fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)
