import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Education & Career Success Dashboard",
    layout="wide" 
)

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

df = load_data()

# Load and preprocess data

df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

df_grouped = df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Sidebar filters
st.sidebar.title("Filters")
job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels = st.sidebar.multiselect("Select Job Levels", job_levels, default=job_levels)

min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

selected_statuses = st.sidebar.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])

# Filter data
filtered = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_levels)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]

# Font size adjustment based on bar count
def get_font_size(n):
    return {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8, 10: 7}.get(n, 6)

# Chart colors
color_map = {'Yes': '#FFD700', 'No': '#004080'}
level_order = ['Entry', 'Executive', 'Mid', 'Senior']
visible_levels = [lvl for lvl in level_order if lvl in selected_levels]

# Page title
st.title("🚀 Education & Career Success Dashboard")

# Display each level's charts
for level in visible_levels:
    data = filtered[filtered['Current_Job_Level'] == level]
    if data.empty:
        st.write(f"### {level} – No data available")
        continue

    ages = sorted(data['Age'].unique())
    font_size = get_font_size(len(ages))
    chart_width = max(400, min(1200, 50 * len(ages) + 100))

    # Stacked Bar Chart (Percentage)
    fig_bar = px.bar(
        data,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Percentage': 'Percentage'},
        height=400,
        width=chart_width,
        title=f"{level} Level – Entrepreneurship by Age (%)"
    )

    for status in ['No', 'Yes']:
        for _, row in data[data['Entrepreneurship'] == status].iterrows():
            if row['Percentage'] > 0:
                y_pos = row['Percentage'] + 0.08
                y_pos = 0.20 if status == 'No' else 0.90
                fig_bar.add_annotation(
                    x=row['Age'],
                    y=y_pos,
                    text=f"{row['Percentage']:.0%}",
                    showarrow=False,
                    font=dict(color="white", size=font_size),
                    xanchor="center",
                    yanchor="middle"
                )

    fig_bar.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90,
        bargap=0.1
    )
    fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

    # Area Chart with Markers (Count)
    fig_area = px.area(
        data,
        x='Age',
        y='Count',
        color='Entrepreneurship',
        markers=True,
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Count': 'Count'},
        height=400,
        width=chart_width,
        title=f"{level} Level – Entrepreneurship by Age (Count)"
    )

    fig_area.update_traces(line=dict(width=2), marker=dict(size=8))
    fig_area.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90
    )
    fig_area.update_yaxes(title="Count")

    # Show charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_area, use_container_width=True)


