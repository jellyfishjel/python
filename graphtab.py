import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# PAGE CONFIG
st.set_page_config(page_title="Career Success Dashboard", layout="wide", page_icon="📊")
st.title("Education Career Success Analysis")

# LOAD DATA
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# ======= GRAPH 1: SUNBURST =======
st.subheader("Career Path Sunburst")

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

yes_colors = {'Engineering': '#aedea7', 'Business': '#dbf1d5', 'Arts': '#0c7734',
              'Computer Science': '#73c375', 'Medicine': '#00441b', 'Law': '#f7fcf5', 'Mathematics': '#37a055'}
no_colors = {'Engineering': '#005b96', 'Business': '#03396c', 'Arts': '#009ac7',
             'Computer Science': '#8ed2ed', 'Medicine': '#b3cde0', 'Law': '#5dc4e1', 'Mathematics': '#0a70a9'}
color_map = {f"Yes - {k}": v for k, v in yes_colors.items()} | {f"No - {k}": v for k, v in no_colors.items()}
color_map.update({'Yes': '#ffd16a', 'No': '#ffd16a'})

fig1 = px.sunburst(
    sunburst_data,
    path=['Ent_Label', 'Field_Label', 'Salary_Label'],
    values='Count',
    color='Ent_Field',
    color_discrete_map=color_map,
    title='Career Path Insights: Education, Salary & Entrepreneurship'
)
fig1.update_traces(insidetextorientation='radial', maxdepth=2, branchvalues="total", textinfo='label+text')
fig1.update_layout(width=500, height=500, margin=dict(t=40, l=0, r=0, b=0))

col_sun, col_sun_txt = st.columns([3, 1])
with col_sun:
    st.plotly_chart(fig1, use_container_width=True)
with col_sun_txt:
    st.markdown("### 💡 How to use")
    st.markdown("""
- Inner ring: *Entrepreneurship*  
- Middle ring: *Field of Study*  
- Outer ring: *Salary Group*  
- Percentages show segment distribution  
- Click to zoom in on specific segments.
""")


# ======= GRAPH 2: JOB LEVEL BY AGE & ENTREPRENEURSHIP =======
st.subheader("Job Level vs. Age by Entrepreneurship")

df2 = df[df['Entrepreneurship'].isin(['Yes', 'No'])]
df_grouped = df2.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels = st.multiselect("Select Job Levels", job_levels, default=job_levels, key="level_selector")
min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())
age_range = st.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age), key="age_slider")
selected_statuses = st.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'], key="status_selector")

filtered = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_levels)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]

color_map2 = {'Yes': '#FFD700', 'No': '#004080'}
level_order = ['Entry', 'Executive', 'Mid', 'Senior']
visible_levels = [lvl for lvl in level_order if lvl in selected_levels]

for level in visible_levels:
    data = filtered[filtered['Current_Job_Level'] == level]
    if data.empty:
        st.write(f"### {level} – No data available")
        continue

    ages = sorted(data['Age'].unique())


    fig_bar = px.bar(
        data,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map2,
        height=400,
        width=500,
        title=f"{level} Level – Entrepreneurship by Age (%)"
    )
    fig_bar.update_layout(margin=dict(t=30, l=30, r=30, b=30), legend_title_text='Entrepreneurship', xaxis_tickangle=90)
    fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

    fig_area = px.area(
        data,
        x='Age',
        y='Count',
        color='Entrepreneurship',
        markers=True,
        color_discrete_map=color_map2,
        height=400,
        width=500,
        title=f"{level} Level – Entrepreneurship by Age (Count)"
    )
    for status in ['Yes', 'No']:
        avg_age = data[data['Entrepreneurship'] == status]['Age'].mean()
        fig_area.add_vline(x=avg_age, line_dash="dot", line_color=color_map2[status], line_width=1.2)
        fig_area.add_trace(go.Scatter(
            x=[None], y=[None], mode='markers',
            marker=dict(symbol='circle', size=10, color=color_map2[status]),
            name=f"{status} Avg Age: {avg_age:.1f}"
        ))
    fig_area.update_traces(line=dict(width=2), marker=dict(size=8))
    fig_area.update_layout(margin=dict(t=30, l=30, r=30, b=30), legend_title_text='Entrepreneurship')

    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col_b:
        st.plotly_chart(fig_area, use_container_width=True)


# ======= GRAPH 3: WORK-LIFE BALANCE =======
st.subheader("Work-Life Balance by Years to Promotion")

avg_balance = (
    df.groupby(['Current_Job_Level', 'Years_to_Promotion'])['Work_Life_Balance']
    .mean()
    .reset_index()
)

job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
avg_balance['Current_Job_Level'] = pd.Categorical(
    avg_balance['Current_Job_Level'], categories=job_levels_order, ordered=True
)

selected_balance_levels = st.multiselect(
    "Select Job Levels to Display (Work-Life Balance)",
    options=job_levels_order + ["All"],
    default=["All"]
)

if "All" in selected_balance_levels or not selected_balance_levels:
    filtered_balance = avg_balance
else:
    filtered_balance = avg_balance[avg_balance["Current_Job_Level"].isin(selected_balance_levels)]

colors = {
    "Entry": "#1f77b4",
    "Mid": "#ff7f0e",
    "Senior": "#2ca02c",
    "Executive": "#d62728"
}

fig3 = go.Figure()
for level in job_levels_order:
    if "All" in selected_balance_levels or level in selected_balance_levels:
        data_level = filtered_balance[filtered_balance["Current_Job_Level"] == level]
        fig3.add_trace(go.Scatter(
            x=data_level["Years_to_Promotion"],
            y=data_level["Work_Life_Balance"],
            mode="lines+markers",
            name=level,
            line=dict(color=colors[level]),
            hovertemplate=f"%{{y:.2f}}"
        ))

fig3.update_layout(
    title="Average Work-Life Balance by Years to Promotion",
    xaxis_title="Years to Promotion",
    yaxis_title="Average Work-Life Balance",
    height=400,
    width=700,
    title_x=0.5,
    legend_title_text="Job Level",
    legend=dict (font=dict(size=14)),
    hovermode="x unified",
    xaxis=dict(showspikes=True, spikemode="across", spikecolor="gray"),
    yaxis=dict(showspikes=True, spikemode="across", spikecolor="gray")
)
st.plotly_chart(fig3, use_container_width=True)
