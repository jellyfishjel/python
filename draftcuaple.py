import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Constants / Configurations ---
JOB_LEVELS_ORDER = ['Entry', 'Mid', 'Senior', 'Executive']
COLOR_MAP_ENT = {
    'Yes - Engineering': '#aedea7', 'No - Engineering': '#005b96',
    'Yes - Business': '#dbf1d5', 'No - Business': '#03396c',
    'Yes - Arts': '#0c7734', 'No - Arts': '#009ac7',
    'Yes - Computer Science': '#73c375', 'No - Computer Science': '#8ed2ed',
    'Yes - Medicine': '#00441b', 'No - Medicine': '#b3cde0',
    'Yes - Law': '#f7fcf5', 'No - Law': '#5dc4e1',
    'Yes - Mathematics': '#37a055', 'No - Mathematics': '#0a70a9',
    'Yes': '#ffd16a', 'No': '#ffd16a'
}
COLOR_MAP_ENTREPRENEURSHIP = {'Yes': '#FFD700', 'No': '#004080'}
FONT_SIZES = {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8, 10: 7}

st.set_page_config(page_title="📊 Education & Career Insights", layout="wide")

# --- Helper Functions ---

def categorize_salary(salary):
    if salary < 30000:
        return '<30K'
    elif salary < 50000:
        return '30K–50K'
    elif salary < 70000:
        return '50K–70K'
    else:
        return '70K+'

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

@st.cache_data
def get_sunburst_data(df):
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
    
    return sunburst_data, total_count

@st.cache_data
def get_avg_work_life_balance(df):
    avg_balance = (
        df.groupby(['Current_Job_Level', 'Years_to_Promotion'])['Work_Life_Balance']
        .mean().reset_index()
    )
    avg_balance['Current_Job_Level'] = pd.Categorical(avg_balance['Current_Job_Level'], categories=JOB_LEVELS_ORDER, ordered=True)
    return avg_balance

@st.cache_data
def get_entrepreneurship_grouped(df):
    df_filtered = df[df['Entrepreneurship'].isin(['Yes', 'No'])]
    df_grouped = df_filtered.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
    df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())
    return df_grouped

def get_font_size(n):
    return FONT_SIZES.get(n, 6)

def plot_entrepreneurship_charts(data, level, chart_width, font_size):
    ages = sorted(data['Age'].unique())
    
    # Bar chart: Entrepreneurship %
    fig_bar = px.bar(
        data, x='Age', y='Percentage', color='Entrepreneurship', barmode='stack',
        color_discrete_map=COLOR_MAP_ENTREPRENEURSHIP,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Percentage': 'Percentage'},
        height=400, width=chart_width,
        title=f"{level} Level – Entrepreneurship by Age (%)"
    )
    
    # Add percentage annotations inside bars
    for status in ['No', 'Yes']:
        for _, row in data[data['Entrepreneurship'] == status].iterrows():
            if row['Percentage'] > 0:
                y_pos = 0.20 if status == 'No' else 0.90
                fig_bar.add_annotation(
                    x=row['Age'], y=y_pos, text=f"{row['Percentage']:.0%}",
                    showarrow=False, font=dict(color="white", size=font_size),
                    xanchor="center", yanchor="middle"
                )
    fig_bar.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90, bargap=0.1
    )
    fig_bar.update_yaxes(tickformat=".0%", title="Percentage")
    
    # Area chart: Entrepreneurship counts
    fig_area = px.area(
        data, x='Age', y='Count', color='Entrepreneurship', markers=True,
        color_discrete_map=COLOR_MAP_ENTREPRENEURSHIP,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Count': 'Count'},
        height=400, width=chart_width,
        title=f"{level} Level – Entrepreneurship by Age (Count)"
    )
    fig_area.update_traces(line=dict(width=2), marker=dict(size=8))
    fig_area.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90
    )
    fig_area.update_yaxes(title="Count")
    
    return fig_bar, fig_area

# --- Load Data ---
df = load_data()

# --- KPI Summary at top ---
st.title("📊 Education & Career Insights Dashboard")
st.markdown("---")
with st.container():
    st.subheader("📌 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    avg_salary = df['Starting_Salary'].mean()
    pct_entrepreneurs = (df['Entrepreneurship'] == 'Yes').mean() * 100
    avg_work_life = df['Work_Life_Balance'].mean()
    avg_years_promo = df['Years_to_Promotion'].mean()
    
    col1.metric("Avg Starting Salary (USD)", f"${avg_salary:,.0f}")
    col2.metric("% Entrepreneurs", f"{pct_entrepreneurs:.1f}%")
    col3.metric("Avg Work-Life Balance", f"{avg_work_life:.2f} / 5")
    col4.metric("Avg Years to Promotion", f"{avg_years_promo:.1f} years")

st.markdown("---")

# --- Sidebar Filters ---
with st.sidebar:
    st.header("🔎 Filters")
    
    st.subheader("Line Chart Filters")
    selected_levels_line = st.multiselect(
        "Select Job Levels (Line Chart)",
        JOB_LEVELS_ORDER,
        default=JOB_LEVELS_ORDER
    )
    
    st.subheader("Bar/Area Charts Filters")
    job_levels_all = sorted(df['Current_Job_Level'].unique())
    selected_bar_levels = st.multiselect(
        "Select Job Levels (Bar/Area Charts)",
        job_levels_all,
        default=job_levels_all
    )
    
    min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
    age_range = st.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))
    
    selected_statuses = st.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])

# --- 1. SUNBURST CHART ---
st.header("🌞 Career Path Sunburst")

sunburst_data, total_count = get_sunburst_data(df)

fig1 = px.sunburst(
    sunburst_data,
    path=['Ent_Label', 'Field_Label', 'Salary_Label'],
    values='Count',
    color='Ent_Field',
    color_discrete_map=COLOR_MAP_ENT,
    custom_data=['Percentage'],
    title='Career Path Insights: Education, Salary & Entrepreneurship',
    height=500
)
fig1.update_traces(
    insidetextorientation='radial',
    maxdepth=2,
    branchvalues="total",
    textinfo='label+text',
    hovertemplate="<b>%{label}</b><br>Value: %{value}<br>"
)
st.plotly_chart(fig1, use_container_width=True)

# --- 2. LINE CHART ---
st.header("📈 Work-Life Balance by Job Level and Promotion Timeline")

avg_balance = get_avg_work_life_balance(df)

# Filter line chart data by selected levels
filtered_line_data = avg_balance[avg_balance["Current_Job_Level"].isin(selected_levels_line)]

fig2 = go.Figure()
colors_line = {"Entry": "#1f77b4", "Mid": "#ff7f0e", "Senior": "#2ca02c", "Executive": "#d62728"}

for level in JOB_LEVELS_ORDER:
    if level in selected_levels_line:
        data_level = filtered_line_data[filtered_line_data["Current_Job_Level"] == level]
        fig2.add_trace(go.Scatter(
            x=data_level["Years_to_Promotion"],
            y=data_level["Work_Life_Balance"],
            mode="lines+markers",
            name=level,
            line=dict(color=colors_line[level]),
            hovertemplate=f"%{{y:.2f}}"
        ))

fig2.update_layout(
    title="Average Work-Life Balance by Years to Promotion",
    xaxis_title="Years to Promotion",
    yaxis_title="Average Work-Life Balance",
    height=600,
    title_x=0.5,
    legend_title_text="Job Level",
    hovermode="x unified",
    xaxis=dict(showspikes=True, spikemode="across", spikesnap="cursor"),
    yaxis=dict(range=[1, 5])
)
st.plotly_chart(fig2, use_container_width=True)

# --- 3. BAR & AREA CHARTS: Entrepreneurship by Age ---
st.header("📊 Entrepreneurship Distribution by Age and Job Level")

df_grouped = get_entrepreneurship_grouped(df)

# Filter based on user selections in sidebar
filtered = df_grouped[
    (df_grouped["Current_Job_Level"].isin(selected_bar_levels)) &
    (df_grouped["Age"].between(age_range[0], age_range[1])) &
    (df_grouped["Entrepreneurship"].isin(selected_statuses))
]

visible_levels = filtered["Current_Job_Level"].unique()

if len(visible_levels) == 0:
    st.warning("No data to display for selected filters.")
else:
    for level in visible_levels:
        data = filtered[filtered['Current_Job_Level'] == level]
        if data.empty:
            st.write(f"### {level} – No data available")
            continue
        
        chart_width = max(400, min(1200, 50 * len(sorted(data['Age'].unique())) + 100))
        font_size = get_font_size(len(sorted(data['Age'].unique())))
        
        fig_bar, fig_area = plot_entrepreneurship_charts(data, level, chart_width, font_size)
        
        st.subheader(f"Level: {level}")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.plotly_chart(fig_area, use_container_width=True)
        st.markdown("---")
