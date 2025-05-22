import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Đọc dữ liệu từ file Excel
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# Pivot lại dữ liệu: tạo dataframe dạng mỗi job level là một cột
df = df.pivot_table(
    index='Years_to_Promotion',
    columns='Current_Job_Level',
    values='Work_Life_Balance'
).reset_index()

# Đổi tên cột columns để tiện dùng
df.columns.name = None  # xóa tên group của cột

# Tạo biểu đồ
fig = go.Figure()

# Danh sách các nhóm và màu tương ứng
levels = {
    "Entry": "blue",
    "Mid": "orange",
    "Senior": "green",
    "Executive": "red"
}

# Thêm từng nhóm vào biểu đồ nếu có
for level, color in levels.items():
    if level in df.columns:
        fig.add_trace(go.Scatter(
            x=df["Years_to_Promotion"],
            y=df[level],
            mode="lines+markers",
            name=level,
            line=dict(color=color),
            hovertemplate=f"%{{y:.2f}}"
        ))

# Cài đặt layout
fig.update_layout(
    title="Average Work-Life Balance by Years to Promotion",
    xaxis_title="Years to Promotion",
    yaxis_title="Average Work-Life Balance",
    hovermode="x unified",
    template="plotly_dark"
)

# Hiển thị biểu đồ
st.plotly_chart(fig)
