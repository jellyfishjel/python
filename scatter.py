import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🎓 University GPA vs. Starting Salary")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

df = load_data()

# Tạo nhóm GPA
df["GPA_Group"] = pd.cut(
    df["University_GPA"],
    bins=[2.0, 2.5, 3.0, 3.5, 4.0],
    labels=["2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"],
    include_lowest=True
)

# Lựa chọn nhóm GPA
selected_gpa = st.selectbox("Select GPA Group", ["All"] + df["GPA_Group"].cat.categories.tolist())

# Lựa chọn khoảng lương
salary_min, salary_max = int(df["Starting_Salary"].min()), int(df["Starting_Salary"].max())
salary_range = st.slider("Select Starting Salary Range", salary_min, salary_max, (salary_min, salary_max), 1000)

# Lọc dữ liệu
mask = df["Starting_Salary"].between(*salary_range)
if selected_gpa != "All":
    mask &= (df["GPA_Group"] == selected_gpa)
filtered_df = df[mask]

# Vẽ biểu đồ scatter plot có đường hồi quy bằng plotly express
fig = px.scatter(
    filtered_df,
    x="University_GPA",
    y="Starting_Salary",
    trendline="ols",  # thêm đường hồi quy tuyến tính
    opacity=0.7,
    labels={
        "University_GPA": "University GPA",
        "Starting_Salary": "Starting Salary"
    },
    title="GPA vs. Starting Salary"
)

fig.data[1].line.color = '#FFA500'  # màu cam

fig.data[0].marker.color = '#00BFFF'  # màu DeepSkyBlue (xanh dương sáng)

# Tăng chiều cao biểu đồ
fig.update_layout(
    height=600,
)
st.plotly_chart(fig, use_container_width=True)
