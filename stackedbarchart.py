import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Entrepreneurship by Age & Gender", layout="wide")

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

    # Area chart: Count
    fig_line = px.line(
        df,
        x="Years_to_Promotion",
        y="Entrepreneurship",
        color="Current_Job_Level",  # hoặc "Gender"
        markers=True,
        title="Entrepreneurship by Years to Promotion and Job Level"
    )

    fig.update_layout(
        xaxis_title="Age",
        yaxis_title="Entrepreneurship (%)",
        hovermode="x unified",
        title_x=0.5
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_line, use_container_width=True)



