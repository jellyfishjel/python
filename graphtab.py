import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Education & Career Success Dashboard", layout="wide", page_icon="📊")
st.title("📊 Education & Career Success Dashboard")

# === Caching and shared data ===
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# === SECTION 1: Career Path Sunburst ===
st.markdown("## 🌞 Career Path Sunburst")

sunburst_df = df.copy()

def categorize_salary(salary):
    if salary < 30000:
        return '<30K'
    elif salary < 50000:
        return '30K–50K'
    elif salary < 70000:
        return '50K–70K'
    else:
        return '70K+'

sunburst_df['Salary_Group'] = sunburst_df['Starting_Salary'].apply(categorize_salary)

sunburst_data = sunburst_df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')
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
    'Engineering': '#aedea7',
    'Business': '#dbf1d5',
    'Arts': '#0c7734',
    'Computer Science': '#73c375',
    'Medicine': '#00441b',
    'Law': '#f7fcf5',
    'Mathematics': '#37a055'
}

no_colors = {
    'Engineering': '#005b96',
    'Business': '#03396c',
    'Arts': '#009ac7',
    'Computer Science': '#8ed2ed',
    'Medicine': '#b3cde0',
    'Law': '#5dc4e1',
    'Mathematics': '#0a70a9'
}

color_map = {}

for status in ['Yes', 'No']:
    label = f"{status}<br>{round(ent_totals[status] / total_count * 100, 2)}%"
    color_map[label] = '#FFD700'

for field, color in yes_colors.items():
    color_map[f"Yes - {field}"] = color
for field, color in no_colors.items():
    color_map[f"No - {field}"] = color

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

col1, col2 = st.columns([3, 1])
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.markdown("### 💡 How to use")
    st.markdown("""
- **Inner ring**: Entrepreneurship  
- **Middle**: Field of Study  
- **Outer**: Salary group  
- Labels include percentage share  
- Click to zoom into segments  
    """)

# === SECTION 2: Job Level vs Age (Bar + Area) ===
st.markdown("📊 Entrepreneurship by Age & Job Level")
    job_df = df[df['Entrepreneurship'].isin(['Yes', 'No'])].copy()
    grouped = job_df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
    grouped['Percentage'] = grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

    st.sidebar.title("Filters")
    job_levels = sorted(grouped['Current_Job_Level'].unique())
    selected_levels = st.sidebar.multiselect("Select Job Levels", job_levels, default=job_levels)
    age_min, age_max = int(grouped['Age'].min()), int(grouped['Age'].max())
    age_range = st.sidebar.slider("Select Age Range", min_value=age_min, max_value=age_max, value=(age_min, age_max))
    selected_statuses = st.sidebar.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])

    filtered = grouped[
        (grouped['Current_Job_Level'].isin(selected_levels)) &
        (grouped['Entrepreneurship'].isin(selected_statuses)) &
        (grouped['Age'].between(age_range[0], age_range[1]))
    ]

    color_map = {'Yes': '#FFD700', 'No': '#004080'}
    level_order = ['Entry', 'Executive', 'Mid', 'Senior']
    visible_levels = [lvl for lvl in level_order if lvl in selected_levels]

    for level in visible_levels:
        data = filtered[filtered['Current_Job_Level'] == level]
        if data.empty:
            st.write(f"### {level} – No data available")
            continue

        ages = sorted(data['Age'].unique())
        font_size = {1: 20, 2: 18, 3: 16, 4: 14, 5: 12}.get(len(ages), 10)
        chart_width = max(400, min(1200, 50 * len(ages) + 100))

        fig_bar = px.bar(
            data, x='Age', y='Percentage', color='Entrepreneurship', barmode='stack',
            color_discrete_map=color_map, height=400, width=chart_width,
            title=f"{level} Level – Entrepreneurship by Age (%)"
        )
        fig_bar.update_layout(margin=dict(t=40, l=40, r=40, b=40), xaxis_tickangle=90, bargap=0.1)
        fig_bar.update_yaxes(tickformat=".0%")


        fig_area = px.area(
            data, x='Age', y='Count', color='Entrepreneurship', markers=True,
            color_discrete_map=color_map, height=400, width=chart_width,
            title=f"{level} Level – Entrepreneurship by Age (Count)"
        )

        fig_area.update_layout(
    hovermode='x',
    spikedistance=-1,
    xaxis=dict(
        showspikes=True,
        spikemode='toaxis',      
        spikesnap='cursor',       
        showline=True,
        spikethickness=1,
        spikecolor="gray",
        spikedash="dot"
    ),
    yaxis=dict(
        showspikes=False  
    )
)

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.plotly_chart(fig_area, use_container_width=True)


# === SECTION 3: GPA vs. Salary Scatter Plot ===
st.markdown("🎓 GPA vs. Starting Salary", expanded=True)
    df["GPA_Group"] = pd.cut(df["University_GPA"], bins=[2.0, 2.5, 3.0, 3.5, 4.0],
                             labels=["2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"], include_lowest=True)

    selected_gpa = st.selectbox("Select GPA Group", ["All"] + df["GPA_Group"].cat.categories.tolist())
    salary_min, salary_max = int(df["Starting_Salary"].min()), int(df["Starting_Salary"].max())
    salary_range = st.slider("Select Starting Salary Range", salary_min, salary_max, (salary_min, salary_max), 1000)

    mask = df["Starting_Salary"].between(*salary_range)
    if selected_gpa != "All":
        mask &= (df["GPA_Group"] == selected_gpa)
    filtered_df = df[mask]

    fig3 = px.scatter(
    filtered_df, x="University_GPA", y="Starting_Salary",
    opacity=0.7,
    title="GPA vs. Starting Salary"
)
    fig3.data[0].marker.color = '#00BFFF'
    fig3.update_layout(height=700)
    st.plotly_chart(fig3, use_container_width=True)

# === SECTION 4: Work-Life Balance Line Chart ===
with st.expander("⚖️ Work-Life Balance by Promotion Time")
    avg_balance = df.groupby(['Current_Job_Level', 'Years_to_Promotion'])['Work_Life_Balance'].mean().reset_index()
    job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
    avg_balance['Current_Job_Level'] = pd.Categorical(avg_balance['Current_Job_Level'],
                                                      categories=job_levels_order, ordered=True)
# === SECTION 4: Work-Life Balance Line Chart ===
with st.expander("⚖️ Work-Life Balance by Promotion Time", expanded=True):
    avg_balance = (
        df.groupby(['Current_Job_Level', 'Years_to_Promotion'])['Work_Life_Balance']
        .mean()
        .reset_index()
    )

    job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
    avg_balance['Current_Job_Level'] = pd.Categorical(
        avg_balance['Current_Job_Level'], categories=job_levels_order, ordered=True
    )

    selected_levels = st.sidebar.multiselect(
        "Select Job Levels to Display (Work-Life Balance)",
        options=job_levels_order + ["All"],
        default=["All"]
    )

    if "All" in selected_levels or not selected_levels:
        filtered_data = avg_balance
    else:
        filtered_data = avg_balance[avg_balance["Current_Job_Level"].isin(selected_levels)]

    fig = go.Figure()
    colors = {
        "Entry": "#1f77b4",      # blue
        "Mid": "#ff7f0e",        # orange
        "Senior": "#2ca02c",     # green
        "Executive": "#d62728"   # red
    }

    for level in job_levels_order:
        if "All" in selected_levels or level in selected_levels:
            data_level = filtered_data[filtered_data["Current_Job_Level"] == level]
            fig.add_trace(go.Scatter(
                x=data_level["Years_to_Promotion"],
                y=data_level["Work_Life_Balance"],
                mode="lines+markers",
                name=level,
                line=dict(color=colors[level]),
                hovertemplate="%{y:.2f}"
            ))

    fig.update_layout(
        title="Average Work-Life Balance by Years to Promotion",
        xaxis_title="Years to Promotion",
        yaxis_title="Average Work-Life Balance",
        height=600,
        width=900,
        title_x=0.5,
        legend_title_text="Job Level",
        hovermode="x unified",
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

    st.plotly_chart(fig, use_container_width=True)
