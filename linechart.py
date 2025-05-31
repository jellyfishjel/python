import streamlit as st
import plotly.graph_objects as go
import pandas as pd


@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# Tính trung bình Work-Life Balance theo Job Level và Years_to_Promotion
avg_balance = (
    df.groupby(['Current_Job_Level', 'Years_to_Promotion'])['Work_Life_Balance']
    .mean()
    .reset_index()
)

# Sắp xếp thứ tự cấp bậc công việc
job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
avg_balance['Current_Job_Level'] = pd.Categorical(
    avg_balance['Current_Job_Level'], categories=job_levels_order, ordered=True
)

# Sidebar chọn cấp bậc
selected_levels = st.sidebar.multiselect(
    "Select Job Levels to Display",
    options=job_levels_order + ["All"],
    default=["All"]
)

if "All" in selected_levels or not selected_levels:
    filtered_data = avg_balance
else:
    filtered_data = avg_balance[avg_balance["Current_Job_Level"].isin(selected_levels)]

# Tạo biểu đồ bằng go.Figure
fig = go.Figure()

colors = {
    "Entry": "#1f77b4",      # blue
    "Mid": "#ff7f0e",        # orange
    "Senior": "#2ca02c",     # green
    "Executive": "#d62728"   # red
}

# Thêm từng trace cho mỗi Job Level
for level in job_levels_order:
    if "All" in selected_levels or level in selected_levels:
        data_level = filtered_data[filtered_data["Current_Job_Level"] == level]
        fig.add_trace(go.Scatter(
            x=data_level["Years_to_Promotion"],
            y=data_level["Work_Life_Balance"],
            mode="lines+markers",
            name=level,
            line=dict(color=colors[level]),
            hovertemplate=f"%{{y:.2f}}"  # chỉ hiện giá trị, tên & màu trace tự hiển thị theo format 'x unified'
        ))

# Cấu hình layout
fig.update_layout(
    title="Average Work-Life Balance by Years to Promotion",
    xaxis_title="Years to Promotion",
    yaxis_title="Average Work-Life Balance",
    height=600,
    width=900,
    title_x=0.5,
    legend_title_text="Job Level",
    hovermode="x unified",  # Tooltip gom nhóm & hiển thị line màu như ảnh mẫu
    xaxis=dict(
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikedash="dot",
        spikethickness=1,
        spikecolor="gray"
    ),
    yaxis=dict(
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikedash="dot",
        spikethickness=1,
        spikecolor="gray"
    )
)

# Hiển thị biểu đồ
st.plotly_chart(fig, use_container_width=True)
