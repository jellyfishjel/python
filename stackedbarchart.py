import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Entrepreneurship Analysis", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

st.title("📈 Entrepreneurship and Job Offers by Age")
st.markdown("Analyze the relationship between entrepreneurship status, job level, and job offers across age groups.")

st.sidebar.title("Filter Options")

# Gender filter (with 'All')
gender_options = ['All'] + sorted(df['Gender'].dropna().unique())
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)
if selected_gender != 'All':
    df = df[df['Gender'] == selected_gender]

# Job level filter
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Age filter
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Entrepreneurship filter (with 'All')
entrepreneur_options = ['All', 'Yes', 'No']
selected_status = st.sidebar.selectbox("Select Entrepreneurship Status", entrepreneur_options)

# Convert to list for filtering
selected_statuses = ['Yes', 'No'] if selected_status == 'All' else [selected_status]

# Color mapping
color_map = {'Yes': '#FFD700', 'No': '#004080'}

# Grouped data for percentage bar chart
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
    .size()
    .reset_index(name='Count')
)
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

df_bar = df_grouped[
    (df_grouped['Current_Job_Level'] == selected_level) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]
if selected_status != 'All':
    df_bar = df_bar[df_bar['Entrepreneurship'] == selected_status]

# Bar chart
fig_bar = px.bar(
    df_bar,
    x='Age',
    y='Percentage',
    color='Entrepreneurship',
    barmode='stack',
    color_discrete_map=color_map,
    category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': sorted(df_bar['Age'].unique())},
    labels={'Age': 'Age', 'Percentage': 'Percentage'},
    height=400,
    title=f"Entrepreneurship Distribution by Age – {selected_level} Level"
)
fig_bar.update_layout(
    margin=dict(t=40, l=40, r=40, b=40),
    legend_title_text='Entrepreneurship',
    xaxis_tickangle=90,
    bargap=0.1
)
fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

# Line chart: Average Job Offers
df_avg_offers = (
    df[(df['Current_Job_Level'] == selected_level) &
       (df['Entrepreneurship'].isin(selected_statuses)) &
       (df['Age'].between(age_range[0], age_range[1]))]
    .groupby(['Age', 'Entrepreneurship'])['Job_Offers']
    .mean()
    .reset_index()
)

fig_line = go.Figure()

for status in selected_statuses:  # ['Yes', 'No'] hoặc ['Yes'] hoặc ['No']
    data_status = df_avg_offers[df_avg_offers["Entrepreneurship"] == status]
    fig_line.add_trace(go.Scatter(
        x=data_status["Age"],
        y=data_status["Job_Offers"],
        mode="lines+markers",
        name=status,
        line=dict(color=color_map[status], width=2),
        marker=dict(size=6),
        hovertemplate="%{y:.2f}"  # chỉ hiện giá trị, tên và màu line sẽ auto hiện
    ))

fig_line.update_layout(
    title=f"Average Job Offers by Age – {selected_level} Level",
    xaxis_title="Age",
    yaxis_title="Average Job Offers",
    height=400,
    margin=dict(t=40, l=40, r=40, b=40),
    legend_title_text='Entrepreneurship',
    xaxis_tickangle=90,
    hovermode="x unified",  # 👈 để vẫn hiện cả 2 điểm cùng lúc
    xaxis=dict(
        showspikes=True,
        spikemode='across',
        spikesnap='cursor',
        spikethickness=1.2,
        spikedash='dot',
        spikecolor='gray'
    )
)
# Biểu đồ bar nằm phía trên – cao hơn chút
fig_bar.update_layout(height=500)

# Biểu đồ line nằm phía dưới – thấp hơn
fig_line.update_layout(height=350)

fig_line.update_yaxes(title="Average Job Offers")

# Display charts
st.plotly_chart(fig_bar, use_container_width=True)
st.plotly_chart(fig_line, use_container_width=True)
