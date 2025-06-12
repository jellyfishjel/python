import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load and preprocess data
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

df = load_data()

# Categorize salary into groups
def categorize_salary(salary):
    if pd.isnull(salary):
        return 'Unknown'
    elif salary < 30000:
        return '<30K'
    elif salary < 50000:
        return '30K–50K'
    elif salary < 70000:
        return '50K–70K'
    else:
        return '70K+'

df['Salary_Group'] = df['Starting_Salary'].apply(categorize_salary)

# Filter only valid job levels
valid_levels = df['Current_Job_Level'].dropna().unique().tolist()
valid_levels.sort()

# Sidebar filters
st.sidebar.title("🎯 Filter")
selected_level = st.sidebar.selectbox("Select Job Level", valid_levels)

min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Filter data for selected job level and age range
filtered_df = df[(df['Current_Job_Level'] == selected_level) & (df['Age'].between(age_range[0], age_range[1]))]

# Function to draw donut charts
def plot_donut(data, column, title):
    count_data = data[column].value_counts().reset_index()
    count_data.columns = [column, 'Count']
    fig = px.pie(
        count_data,
        names=column,
        values='Count',
        hole=0.5,
        title=title
    )
    fig.update_traces(textinfo='percent+label', showlegend=False)
    fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
    return fig

# Donut charts: Gender, Field of Study, Salary Group
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(plot_donut(filtered_df, 'Gender', 'Gender Distribution'), use_container_width=True)
with col2:
    st.plotly_chart(plot_donut(filtered_df, 'Field_of_Study', 'Field of Study'), use_container_width=True)
with col3:
    st.plotly_chart(plot_donut(filtered_df, 'Salary_Group', 'Starting Salary Group'), use_container_width=True)

st.title(f"📊 {selected_level} – Career Trends by Age")

# Group data for visualizations
grouped = filtered_df.groupby(['Age', 'Salary_Group']).size().reset_index(name='Count')
grouped['Percentage'] = grouped.groupby('Age')['Count'].transform(lambda x: x / x.sum())

salary_order = ['<30K', '30K–50K', '50K–70K', '70K+', 'Unknown']
grouped['Salary_Group'] = pd.Categorical(grouped['Salary_Group'], categories=salary_order, ordered=True)
grouped = grouped.sort_values(['Age', 'Salary_Group'])

# Color map for salary groups
color_map = {
    '<30K': '#f94144',
    '30K–50K': '#f3722c',
    '50K–70K': '#43aa8b',
    '70K+': '#277da1',
    'Unknown': '#adb5bd'
}

ages = sorted(grouped['Age'].unique())
font_size = {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8, 10: 7}.get(len(ages), 6)
chart_width = max(400, min(1200, 50 * len(ages) + 100))

# Stacked Bar Chart (Percentage)
fig_bar = px.bar(
    grouped,
    x='Age',
    y='Percentage',
    color='Salary_Group',
    barmode='stack',
    color_discrete_map=color_map,
    category_orders={'Salary_Group': salary_order, 'Age': ages},
    labels={'Age': 'Age', 'Percentage': 'Percentage'},
    height=400,
    width=chart_width,
    title="Salary Group Distribution by Age (%)"
)

for _, row in grouped.iterrows():
    if row['Percentage'] > 0.05:
        y_pos = row['Percentage'] / 2
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
    legend_title_text='Salary Group',
    xaxis_tickangle=90,
    bargap=0.1
)
fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

# Area Chart (Count)
fig_area = px.area(
    grouped,
    x='Age',
    y='Count',
    color='Salary_Group',
    markers=True,
    color_discrete_map=color_map,
    category_orders={'Salary_Group': salary_order, 'Age': ages},
    labels={'Age': 'Age', 'Count': 'Count'},
    height=400,
    width=chart_width,
    title="Salary Group Count by Age"
)

fig_area.update_traces(line=dict(width=2), marker=dict(size=8))
fig_area.update_layout(
    margin=dict(t=40, l=40, r=40, b=40),
    legend_title_text='Salary Group',
    xaxis_tickangle=90
)
fig_area.update_yaxes(title="Count")

# Show charts
col4, col5 = st.columns(2)
with col4:
    st.plotly_chart(fig_bar, use_container_width=True)
with col5:
    st.plotly_chart(fig_area, use_container_width=True)
