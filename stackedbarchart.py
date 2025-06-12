import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Entrepreneurship by Age & Gender", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

st.title("📊 Entrepreneurship Analysis by Age and Gender")
st.markdown("This dashboard explores the relationship between entrepreneurship, job levels, and job offers across different age groups.")

st.sidebar.title("Filter Options")

# Gender filter
genders = sorted(df['Gender'].dropna().unique())
selected_genders = st.sidebar.selectbox("Select Gender", genders)

# Filter by gender first
df = df[df['Gender'].isin(selected_genders)]

# Job level filter
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Age filter
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Entrepreneurship filter (select one only)
selected_status = st.sidebar.selectbox("Select Entrepreneurship Status", ['Yes', 'No','All'])

# Filtered for grouped percentage chart
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
    .size()
    .reset_index(name='Count')
)
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

filtered = df_grouped[
    (df_grouped['Current_Job_Level'] == selected_level) &
    (df_grouped['Entrepreneurship'] == selected_status) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]

color_map = {'Yes': '#FFD700', 'No': '#004080'}

if filtered.empty:
    st.warning(f"No data available for Job Level '{selected_level}' and Entrepreneurship = '{selected_status}'.")
else:
    ages = sorted(filtered['Age'].unique())

    # Bar chart: Percentage of Entrepreneurs by Age
    fig_bar = px.bar(
        filtered,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Percentage': 'Entrepreneurship Rate'},
        height=400,
        title=f"Entrepreneurship Rate by Age – {selected_level} Level"
    )
    fig_bar.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship Status',
        xaxis_tickangle=90,
        bargap=0.1
    )
    fig_bar.update_yaxes(tickformat=".0%", title="Entrepreneurship Rate")

    # Line chart: Avg Job Offers by Age
    df_avg_offers = (
        df[(df['Current_Job_Level'] == selected_level) &
           (df['Entrepreneurship'] == selected_status) &
           (df['Age'].between(age_range[0], age_range[1]))]
        .groupby(['Age'])['Job_Offers']
        .mean()
        .reset_index()
    )

    fig_line = px.line(
        df_avg_offers,
        x='Age',
        y='Job_Offers',
        markers=True,
        color_discrete_sequence=['#228B22'],
        labels={'Age': 'Age', 'Job_Offers': 'Average Number of Job Offers'},
        height=400,
        title=f"Average Job Offers by Age – {selected_level} Level (Entrepreneurship: {selected_status})"
    )
    fig_line.update_traces(line=dict(width=2), marker=dict(size=6))
    fig_line.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        hovermode="x unified"
    )
    fig_line.update_yaxes(title="Average Job Offers")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_line, use_container_width=True)
