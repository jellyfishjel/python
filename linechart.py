import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Dữ liệu gốc
df = pd.DataFrame({
    "Years_to_Promotion": [1, 2, 3, 4],
    "Entry": [5.4, 5.3, 5.6, 5.25],
    "Mid": [5.7, 5.5, 5.7, 5.85],
    "Senior": [5.8, 5.7, 5.8, 5.75],
    "Executive": [5.9, 6.0, 5.95, 6.05],
})

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
    fig.add_trace(go.Scatter(
        x=df["Years_to_Promotion"],
        y=df[level],
        mode="lines+markers",
        name=level,
        line=dict(color=color),
        hovertemplate=f"%{{y:.2f}}"  # tooltip hiển thị số y, giữ màu line như bạn muốn
    ))

# Cài đặt layout
fig.update_layout(
    title="Average Work-Life Balance by Years to Promotion",
    xaxis_title="Years to Promotion",
    yaxis_title="Average Work-Life Balance",
    hovermode="x unified",  # hiển thị nhiều giá trị cùng lúc như bạn yêu cầu
    template="plotly_dark"  # giữ nền đen như ảnh bạn chụp
)

# Hiển thị lên Streamlit
st.plotly_chart(fig)
