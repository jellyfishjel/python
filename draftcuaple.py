import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title="📊 Education & Career Insights", layout="wide")


# Title
st.title("📊 Education & Career Insights Dashboard")

df = load_data()
# ------------------------ KEY INDICATORS ------------------------
st.markdown("## 📌 Key Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_salary = df['Starting_Salary'].mean()
    st.metric("💰 Avg Starting Salary", f"${avg_salary:,.0f}")

with col2:
    entrepreneur_pct = (df['Entrepreneurship'].value_counts(normalize=True).get('Yes', 0)) * 100
    st.metric("🚀 Entrepreneurs (%)", f"{entrepreneur_pct:.1f}%")

with col3:
    most_common_field = df['Field_of_Study'].mode()[0]
    st.metric("🎓 Top Field of Study", most_common_field)

with col4:
    avg_wlb = df['Work_Life_Balance'].mean()
    st.metric("⚖️ Avg Work-Life Balance", f"{avg_wlb:.2f}")

# Load Excel data (assumes all data is in the same file)
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)


# ------------------------ 1. SUNBURST CHART ------------------------
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
color_map = {f"Yes - {k}": v for k, v in yes_colors.items()}
color_map.update({f"No - {k}": v for k, v in no_colors.items()})
color_map.update({'Yes': '#ffd16a', 'No': '#ffd16a'})


fig1 = px.sunburst(
    sunburst_data,
    path=['Ent_Label', 'Field_Label', 'Salary_Label'],
    values='Count',
    color='Ent_Field',
    color_discrete_map=color_map,
    custom_data=['Percentage'],
    title='Career Path Insights: Education, Salary & Entrepreneurship',
    height = 500
)
fig1.update_traces(
    insidetextorientation='radial',
    maxdepth=2,
    branchvalues="total",
    textinfo='label+text',
    hovertemplate="<b>%{label}</b><br>Value: %{value}<br>"
)
st.plotly_chart(fig1, use_container_width=True)


# ------------------------ 2. LINE CHART ------------------------
st.header("📈 Work-Life Balance by Job Level and Promotion Timeline")


avg_balance = (
    df.groupby(['Current_Job_Level', 'Years_to_Promotion'])['Work_Life_Balance']
    .mean().reset_index()
)


job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
avg_balance['Current_Job_Level'] = pd.Categorical(avg_balance['Current_Job_Level'],
                                                  categories=job_levels_order, ordered=True)


selected_levels = st.sidebar.multiselect("Select Job Levels (Line Chart)", job_levels_order + ["All"], default=["All"])
filtered_line_data = avg_balance if "All" in selected_levels or not selected_levels else \
    avg_balance[avg_balance["Current_Job_Level"].isin(selected_levels)]


fig2 = go.Figure()
colors = {"Entry": "#1f77b4", "Mid": "#ff7f0e", "Senior": "#2ca02c", "Executive": "#d62728"}


for level in job_levels_order:
    if "All" in selected_levels or level in selected_levels:
        data_level = filtered_line_data[filtered_line_data["Current_Job_Level"] == level]
        fig2.add_trace(go.Scatter(
            x=data_level["Years_to_Promotion"],
            y=data_level["Work_Life_Balance"],
            mode="lines+markers",
            name=level,
            line=dict(color=colors[level]),
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
    xaxis=dict(showspikes=True, spikemode="across", spikesnap="cursor", spikedash="dot", spikecolor="gray"),
    yaxis=dict(showspikes=True, spikemode="across", spikesnap="cursor", spikedash="dot", spikecolor="gray")
)
st.plotly_chart(fig2, use_container_width=True)
with st.expander("📌 Click to read chart interpretation note"):
    st.markdown("""
    <style>
    @keyframes fadeSlideIn {
        0% {
            opacity: 0;
            transform: translateY(20px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .animated-box {
        animation: fadeSlideIn 0.8s ease-in-out;
        background-color: #f0f2f6;
        border-left: 6px solid #4b6cb7;
        padding: 16px;
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 30px;  /* 👈 Add space to bottom */
    }
    </style>

    <div class="animated-box">
        <strong>Note:</strong><br>
        The given line graph shows the connection between average work-life balance and years to promotion of 4 job levels, including <em>Entry</em>, <em>Mid</em>, <em>Senior</em>, and <em>Executive</em>, to answer whether the time taken to receive the first promotion and work-life balance skills affect the current job level.
        <br><br>
        <strong>Insight:</strong> The <em>Mid</em> and <em>Senior</em> groups record an upward trajectory, while the others follow a contrasting pattern. The <em>Executive</em> level undergoes the most dramatic downfall among the four.
    </div>
    """, unsafe_allow_html=True)

# ------------------------ 3 & 4. BAR + AREA ------------------------
st.header("📊 Entrepreneurship by Age and Job Level")


df_filtered = df[df['Entrepreneurship'].isin(['Yes', 'No'])]
df_grouped = df_filtered.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())


job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_bar_levels = st.sidebar.multiselect("Select Job Levels (Bar/Area Charts)", job_levels, default=job_levels)
min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))
selected_statuses = st.sidebar.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])


filtered = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_bar_levels)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]


def get_font_size(n): return {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8, 10: 7}.get(n, 6)


color_map = {'Yes': '#FFD700', 'No': '#004080'}
level_order = ['Entry', 'Executive', 'Mid', 'Senior']
visible_levels = [lvl for lvl in level_order if lvl in selected_bar_levels]


for level in visible_levels:
    data = filtered[filtered['Current_Job_Level'] == level]
    if data.empty:
        st.write(f"### {level} – No data available")
        continue


    ages = sorted(data['Age'].unique())
    font_size = get_font_size(len(ages))
    chart_width = max(400, min(1200, 50 * len(ages) + 100))


    fig_bar = px.bar(
        data, x='Age', y='Percentage', color='Entrepreneurship', barmode='stack',
        color_discrete_map=color_map, category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Percentage': 'Percentage'}, height=400, width=chart_width,
        title=f"{level} Level – Entrepreneurship by Age (%)"
    )


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


    fig_area = px.area(
        data, x='Age', y='Count', color='Entrepreneurship', markers=True,
        color_discrete_map=color_map, category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Count': 'Count'}, height=400, width=chart_width,
        title=f"{level} Level – Entrepreneurship by Age (Count)"
    )
    fig_area.update_traces(line=dict(width=2), marker=dict(size=8))
    fig_area.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90
    )
    fig_area.update_yaxes(title="Count")


    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_area, use_container_width=True)
