import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Entrepreneurship by Age & Gender", layout="wide")
# Load and preprocess data
# LOAD DATA
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()


# Sidebar filters

st.title("📊 Entrepreneurship Trends by Age and Gender")
st.markdown("Explore how entrepreneurship varies across age groups and job levels.")

st.sidebar.title("Filters")

# Gender filter
genders = sorted(df['Gender'].dropna().unique())
selected_genders = st.sidebar.multiselect("Select Gender", genders, default=genders)

# Filter data based on selected genders first
df = df[df['Gender'].isin(selected_genders)]

# Group and calculate percentage
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
      .size()
      .reset_index(name='Count')
)
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Job level filter
job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Age filter
min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Entrepreneurship filter
selected_statuses = st.sidebar.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])

# Final filtered dataset
filtered = df_grouped[
    (df_grouped['Current_Job_Level'] == selected_level) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]

color_map = {'Yes': '#FFD700', 'No': '#004080'}

if filtered.empty:
    st.write(f"### No data available for {selected_level} level.")
else:
    ages = sorted(filtered['Age'].unique())
    
    # Bar chart: Percentage
    fig_bar = px.bar(
        filtered,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Percentage': 'Percentage'},
        height=400,
        title=f"{selected_level} – Entrepreneurship by Age (%)"
    )
    fig_bar.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90,
        bargap=0.1
    )
    fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

  df_line = (
    df[
        (df['Entrepreneurship'].isin(selected_statuses)) &
        (df['Age'].between(age_range[0], age_range[1])) &
        (df['Gender'].isin(selected_genders))
    ]
    .groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])['Job_Offers']
    .mean()
    .reset_index()
)

# Xác định thứ tự Job Level
job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
df_line['Current_Job_Level'] = pd.Categorical(
    df_line['Current_Job_Level'],
    categories=job_levels_order,
    ordered=True
)
df_line = df_line.sort_values(['Current_Job_Level', 'Age'])

# Tạo biểu đồ line
fig_line = px.line(
    df_line,
    x='Age',
    y='Job_Offers',
    color='Entrepreneurship',
    facet_col='Current_Job_Level',
    facet_col_wrap=2,
    markers=True,
    color_discrete_map=color_map,
    category_orders={
        'Current_Job_Level': job_levels_order,
        'Entrepreneurship': ['No', 'Yes']
    },
    labels={'Age': 'Age', 'Job_Offers': 'Avg Job Offers'},
    height=600,
    title="Avg Job Offers by Age, Entrepreneurship & Job Level"
)

fig_line.update_traces(line=dict(width=2), marker=dict(size=6))
fig_line.update_layout(
    margin=dict(t=40, l=40, r=40, b=40),
    legend_title_text='Entrepreneurship',
    xaxis_tickangle=90,
    hovermode="x unified"
)
fig_line.update_yaxes(title="Avg Job Offers")

col1, col2 = st.columns(2)
with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
with col2:
        st.plotly_chart(fig_line, use_container_width=True)

