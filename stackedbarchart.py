import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

df = load_data()
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]


df_grouped = df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

st.sidebar.title("Filters")
job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels = st.sidebar.multiselect("Job Levels", job_levels, default=job_levels)

ages = sorted(df_grouped['Age'].unique())
ages_all = ['ALL'] + [str(a) for a in ages]
selected_ages = st.sidebar.multiselect("Ages", ages_all, default=['ALL'])

statuses = ['Yes', 'No']
selected_statuses = st.sidebar.multiselect("Entrepreneurship", statuses, default=statuses)

mode = st.sidebar.radio("Show as:", ["Percentage (%)", "Count"])

if 'ALL' in selected_ages:
    filtered = df_grouped[
        df_grouped['Current_Job_Level'].isin(selected_levels) &
        df_grouped['Entrepreneurship'].isin(selected_statuses)
    ]
else:
    selected_ages_int = [int(a) for a in selected_ages]
    filtered = df_grouped[
        (df_grouped['Current_Job_Level'].isin(selected_levels)) &
        (df_grouped['Age'].isin(selected_ages_int)) &
        (df_grouped['Entrepreneurship'].isin(selected_statuses))
    ]

if mode == "Percentage (%)":
    y_col = 'Percentage'
    fmt = lambda x: f"{x:.0%}"
    y_axis_title = "Percentage"
    y_tick_format = ".0%"
else:
    y_col = 'Count'
    fmt = lambda x: str(x)
    y_axis_title = "Count"
    y_tick_format = None

colors = {'Yes': '#FFD700', 'No': '#004080'}
order_levels = ['Entry', 'Executive', 'Mid', 'Senior']
levels_to_show = [lvl for lvl in order_levels if lvl in selected_levels]

st.title("🚀 Education & Career Success Dashboard")

cols = st.columns(2)

for i, lvl in enumerate(levels_to_show):
    data_lvl = filtered[filtered['Current_Job_Level'] == lvl]
    if data_lvl.empty:
        with cols[i % 2]:
            st.write(f"### {lvl} — No data")
        continue

    fig = px.bar(
        data_lvl,
        x='Age',
        y=y_col,
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=colors,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': sorted(data_lvl['Age'].unique())},
        text=data_lvl[y_col].apply(fmt),
        labels={'Age': 'Age', y_col: y_axis_title},
        height=350,
        width=600,
        title=f"{lvl} Level"
    )

    fig.update_traces(textposition='inside')
    fig.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90
    )

    fig.update_yaxes(title=y_axis_title)
    if y_tick_format:
        fig.update_yaxes(tickformat=y_tick_format)

    with cols[i % 2]:
        st.plotly_chart(fig, use_container_width=True)
