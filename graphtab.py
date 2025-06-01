import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----- Page Configuration -----
st.set_page_config(page_title="Education & Career Success", layout="wide", page_icon="📊")
st.title("📊 Education & Career Success Dashboard")

# ----- Load Data -----
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

df = load_data()

# =======================
# 1. SUNBURST CHART
# =======================
st.header("🌞 Career Path Sunburst")

def categorize_salary(salary):
    if salary < 30000:
        return '<30K'
    elif salary < 50000:
        return '30K–50K'
    elif salary < 70000:
        return '50K–70K'
    else:
        return '70K+'

df['Salary_Group'] = df['Starting_Salary'].apply(categorize_salary)

sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')
total_count = sunburst_data['Count'].sum()
sunburst_data['Percentage'] = (sunburst_data['Count'] / total_count * 100).round(2)

ent_totals = sunburst_data.groupby('Entrepreneurship')['Count'].sum()
sunburst_data['Ent_Label'] = sunburst_data['Entrepreneurship'].map(
    lambda x: f"{x}<br>{round(ent_totals[x] / total_count * 100, 2)}%"
)

field_totals = sunburst_data.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].sum()
sunburst_data['Field_Label'] = sunburst_data.apply(
    lambda row: f"{row['Field_of_Study']}<br>{round(field_totals[(row['Entrepreneurship'], row['Field_of_Study'])] / total_count * 100, 2)}%",
    axis=1
)

sunburst_data['Salary_Label'] = sunburst_data['Salary_Group'] + '<br>' + sunburst_data['Percentage'].astype(str) + '%'
sunburst_data['Ent_Field'] = sunburst_data['Entrepreneurship'] + " - " + sunburst_data['Field_of_Study']

yes_colors = {
    'Engineering': '#aedea7', 'Business': '#dbf1d5', 'Arts': '#0c7734',
    'Computer Science': '#73c375', 'Medicine': '#00441b', 'Law': '#f7fcf5', 'Mathematics': '#37a055'
}
no_colors = {
    'Engineering': '#005b96', 'Business': '#03396c', 'Arts': '#009ac7',
    'Computer Science': '#8ed2ed', 'Medicine': '#b3cde0', 'Law': '#5dc4e1', 'Mathematics': '#0a70a9'
}

color_map = {f"Yes - {f}": c for f, c in yes_colors.items()}
color_map.update({f"No - {f}": c for f, c in no_colors.items()})
color_map['Yes'] = '#ffd16a'
color_map['No'] = '#ffd16a'

fig1 = px.sunburst(
    sunburst_data,
    path=['Ent_Label', 'Field_Label', 'Salary_Label'],
    values='Count',
    color='Ent_Field',
    color_discrete_map=color_map,
    custom_data=['Percentage'],
    title='Career Path Insights: Education, Salary & Entrepreneurship'
)

fig1.update_traces(
    insidetextorientation='radial',
    maxdepth=2,
    branchvalues="total",
    textinfo='label+text',
    hovertemplate="<b>%{label}</b><br>Value: %{value}<br>"
)

fig1.update_layout(margin=dict(t=50, l=0, r=0, b=0))
st.plotly_chart(fig1, use_container_width=True)

# =======================
# 2. LINE CHART: Work-Life Balance
# =======================
st.header("📈 Work-Life Balance by Promotion Time")

avg_balance = df.groupby(['Current_Job_Level', 'Years_to_Promotion'])['Work_Life_Balance'].mean().reset_index()
job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
avg_balance['Current_Job_Level'] = pd.Categorical(avg_balance['Current_Job_Level'], categories=job_levels_order, ordered=True)

selected_levels = st.multiselect("Select Job Levels to Display", options=job_levels_order + ["All"], default=["All"])

filtered_data = avg_balance if "All" in selected_levels or not selected_levels else avg_balance[avg_balance["Current_Job_Level"].isin(selected_levels)]

fig2 = go.Figure()
colors = {"Entry": "#1f77b4", "Mid": "#ff7f0e", "Senior": "#2ca02c", "Executive": "#d62728"}

for level in job_levels_order:
    if "All" in selected_levels or level in selected_levels:
        data_level = filtered_data[filtered_data["Current_Job_Level"] == level]
        fig2.add_trace(go.Scatter(
            x=data_level["Years_to_Promotion"],
            y=data_level["Work_Life_Balance"],
            mode="lines+markers",
            name=level,
            line=dict(color=colors[level])
        ))

fig2.update_layout(
    title="Average Work-Life Balance by Years to Promotion",
    xaxis_title="Years to Promotion",
    yaxis_title="Average Work-Life Balance",
    hovermode="x unified"
)
st.plotly_chart(fig2, use_container_width=True)

# =======================
# 3. BAR + AREA: Entrepreneurship by Age
# =======================
st.header("📊 Entrepreneurship by Age & Job Level")

df_e = df[df['Entrepreneurship'].isin(['Yes', 'No'])]
df_grouped = df_e.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels_e = st.multiselect("Filter Levels (For Chart 3)", job_levels, default=job_levels)
age_range = st.slider("Select Age Range", int(df_grouped['Age'].min()), int(df_grouped['Age'].max()), value=(20, 60))
selected_statuses = st.multiselect("Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])

filtered = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_levels_e)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]

color_map_e = {'Yes': '#FFD700', 'No': '#004080'}
level_order = ['Entry', 'Executive', 'Mid', 'Senior']
visible_levels = [lvl for lvl in level_order if lvl in selected_levels_e]

def get_font_size(n):
    return {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8, 10: 7}.get(n, 6)

for level in visible_levels:
    data = filtered[filtered['Current_Job_Level'] == level]
    if data.empty:
        st.write(f"### {level} – No data available")
        continue

    ages = sorted(data['Age'].unique())
    font_size = get_font_size(len(ages))
    chart_width = max(400, min(1200, 50 * len(ages) + 100))

    fig_bar = px.bar(
        data,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map_e,
        category_orders={'Entrepreneurship': ['No', 'Yes']},
        height=400,
        width=chart_width,
        title=f"{level} – Entrepreneurship by Age (%)"
    )

    for status in ['No', 'Yes']:
        for _, row in data[data['Entrepreneurship'] == status].iterrows():
            if row['Percentage'] > 0:
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

    fig_area = px.area(
        data,
        x='Age',
        y='Count',
        color='Entrepreneurship',
        markers=True,
        color_discrete_map=color_map_e,
        category_orders={'Entrepreneurship': ['No', 'Yes']},
        height=400,
        width=chart_width,
        title=f"{level} – Entrepreneurship by Age (Count)"
    )

    fig_area.update_traces(line=dict(width=2), marker=dict(size=8))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_area, use_container_width=True)

# =======================
# 4. SCATTER PLOT: GPA vs Salary
# =======================
st.header("🎓 GPA vs. Starting Salary")

df["GPA_Group"] = pd.cut(
    df["University_GPA"],
    bins=[2.0, 2.5, 3.0, 3.5, 4.0],
    labels=["2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"],
    include_lowest=True
)

selected_gpa = st.selectbox("Select GPA Group", ["All"] + df["GPA_Group"].cat.categories.tolist())

salary_min, salary_max = int(df["Starting_Salary"].min()), int(df["Starting_Salary"].max())
salary_range = st.slider("Select Salary Range", salary_min, salary_max, (salary_min, salary_max), 1000)

mask = df["Starting_Salary"].between(*salary_range)
if selected_gpa != "All":
    mask &= (df["GPA_Group"] == selected_gpa)
filtered_df = df[mask]

fig4 = px.scatter(
    filtered_df,
    x="University_GPA",
    y="Starting_Salary",
    trendline="ols",
    opacity=0.7,
    title="GPA vs. Starting Salary"
)

fig4.data[0].marker.color = '#00BFFF'
fig4.data[1].line.color = '#FFA500'
fig4.update_layout(height=700)
st.plotly_chart(fig4, use_container_width=True)
