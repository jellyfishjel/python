import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv("education_career_success.csv")

# Tính trung bình Work-Life Balance theo từng Job Level và Years to Promotion
avg_wlb = df.groupby(["Years_to_Promotion", "Current_Job_Level"])["Work_Life_Balance"].mean().reset_index()

# Pivot lại cho đúng định dạng như DataFrame tay ban đầu
pivot_df = avg_wlb.pivot(index="Years_to_Promotion", columns="Current_Job_Level", values="Work_Life_Balance").reset_index()

# Tạo biểu đồ
fig = go.Figure()

# Danh sách các nhóm và màu tương ứng
levels = {
    "Entry": "blue",
    "Mid": "orange",
    "Senior": "green",
    "Executive": "red"
}

# Thêm từng nhóm vào biểu đồ
for level, color in levels.items():
    if level in pivot_df.columns:
        fig.add_trace(go.Scatter(
            x=pivot_df["Years_to_Promotion"],
            y=pivot_df[level],
            mode="lines+markers",
            name=level,
            line=dict(color=color),
            hovertemplate=f"%{{y:.2f}}"  # tooltip hiển thị giá trị y
        ))

# Cài đặt layout
fig.update_layout(
    title="Average Work-Life Balance by Years to Promotion",
    xaxis_title="Years to Promotion",
    yaxis_title="Average Work-Life Balance",
    hovermode="x unified",
    template="plotly_dark"
)

# Hiển thị biểu đồ trong Streamlit
st.plotly_chart(fig)
