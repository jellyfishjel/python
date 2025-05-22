import streamlit as st
import pandas as pd
import plotly.express as px

# Load dữ liệu
@st.cache_data
def load_data():
    return pd.read_csv("education_career_success.csv")

df = load_data()

# Tính trung bình Work-Life Balance theo từng Job Level và Years_to_Promotion
avg_balance = (
    df.groupby(['Current_Job_Level', 'Years_to_Promotion'])['Work_Life_Balance']
    .mean()
    .reset_index()
)

# Sắp xếp các cấp bậc theo thứ tự mong muốn
job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
avg_balance['Current_Job_Level'] = pd.Categorical(
    avg_balance['Current_Job_Level'], categories=job_levels_order, ordered=True
)

# Sidebar Filter
selected_levels = st.sidebar.multiselect(
    "Select Job Levels to Display",
    options=job_levels_order + ["All"],
    default=["All"]
)

# Lọc dữ liệu theo lựa chọn người dùng
if "All" in selected_levels or not selected_levels:
    filtered_data = avg_balance
else:
    filtered_data = avg_balance[avg_balance["Current_Job_Level"].isin(selected_levels)]

# Plot
fig = px.line(
    filtered_data,
    x="Years_to_Promotion",
    y="Work_Life_Balance",
    color="Current_Job_Level",
    markers=True,
    line_shape="linear",
    hover_name="Current_Job_Level",
    hover_data={
        "Years_to_Promotion": True,
        "Work_Life_Balance": ':.2f',
        "Current_Job_Level": False  # đã hiển thị ở hover_name
    },
    color_discrete_map={
        "Entry": "#1f77b4",
        "Mid": "#ff7f0e",
        "Senior": "#2ca02c",
        "Executive": "#d62728"
    },
    labels={
        "Years_to_Promotion": "Years to Promotion",
        "Work_Life_Balance": "Average Work-Life Balance",
        "Current_Job_Level": "Job Level"
    },
    title="Average Work-Life Balance by Years to Promotion"
)

fig.update_layout(
    height=600,
    width=900,
    legend_title_text="Job Level",
    title_x=0.5,
    hovermode="x",  # Compare data on hover (tương tự biểu đồ trắng)

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
