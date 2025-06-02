import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import base64

# === PAGE CONFIGURATION ===
st.set_page_config(
    page_title="Education & Career Success",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === BACKGROUND IMAGE SETUP ===
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_path = r"D:\bg.png"
img_base64 = get_base64(img_path)

# === INJECT BACKGROUND CSS ===
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    .main-title {{
        text-align: center;
        color: #FF6F00;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 30px;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        justify-content: flex-start;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #FFE0B2;
        border-radius: 16px;
        padding: 6px 14px;
        font-size: 18px;
        font-weight: 600;
        color: #E65100;
        transition: all 0.3s ease;
        height: 42px;
        min-width: 120px;
        text-align: center;
        border: none;
        box-shadow: none;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #FF9800, #FF7043);
        color: white;
        transform: none;
        box-shadow: none;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background: linear-gradient(135deg, #FFD180, #FFB74D);
        cursor: pointer;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# === MAIN TITLE ===
st.markdown('<div class="main-title">Education & Career Success</div>', unsafe_allow_html=True)

# === LOAD DATA ===
@st.cache_data
def load_data():
    return pd.read_csv("D:\\VGU\\education_career_success.csv")

df = load_data()

# === SIDEBAR FILTERS ===
st.sidebar.title("Filters")

# Job Levels
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_levels = st.sidebar.multiselect("Job Levels", job_levels, default=job_levels)

# Ages
ages = sorted(df['Age'].dropna().unique())
ages_all = ['ALL'] + [str(a) for a in ages]
selected_ages = st.sidebar.multiselect("Ages", ages_all, default=['ALL'])

# Entrepreneurship
statuses = ['Yes', 'No']
selected_statuses = st.sidebar.multiselect("Entrepreneurship", statuses, default=statuses)

# Mode
mode = st.sidebar.radio("Show as:", ["Percentage (%)", "Count"], index=0)

# Filtered Data
df_filtered = df[
    df['Current_Job_Level'].isin(selected_levels) &
    df['Entrepreneurship'].isin(selected_statuses)
]

if 'ALL' not in selected_ages:
    selected_ages_int = [int(a) for a in selected_ages]
    df_filtered = df_filtered[df_filtered['Age'].isin(selected_ages_int)]

# === TABS ===
tab1, tab2, tab3 = st.tabs(["Homepage", "Visualisation", "Insights"])

with tab1:
    st.subheader("Welcome to the Education & Career Success Portal")
    st.write("This platform explores the relationship between education and career outcomes.")

with tab2:
    st.subheader("Data Visualisation")

    # === LINE CHART ===
    df_line = df_filtered.pivot_table(
        index='Years_to_Promotion',
        columns='Current_Job_Level',
        values='Work_Life_Balance'
    ).reset_index()
    df_line.columns.name = None

    fig_line = go.Figure()
    levels = {
        "Entry": "blue",
        "Mid": "orange",
        "Senior": "green",
        "Executive": "red"
    }

    for level, color in levels.items():
        if level in df_line.columns:
            fig_line.add_trace(go.Scatter(
                x=df_line["Years_to_Promotion"],
                y=df_line[level],
                mode="lines+markers",
                name=level,
                line=dict(color=color),
                hovertemplate=f"%{{y:.2f}}"
            ))

    fig_line.update_layout(
        title="Average Work-Life Balance by Years to Promotion",
        xaxis_title="Years to Promotion",
        yaxis_title="Average Work-Life Balance",
        hovermode="x unified",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_line, use_container_width=True)

    with st.expander("📈 **Line Chart Description**"):
        st.markdown("""<div style="background-color: #FFFFFF; padding: 25px; border-radius: 20px; color: #5D4037; font-size: 16px; line-height: 1.6; font-weight: 500;">
        The given line graph shows the connection between average work-life balance and years to promotion of 4 job levels... [Cắt ngắn phần mô tả nếu cần]
        </div>""", unsafe_allow_html=True)

    # === SUNBURST CHART ===
    def categorize_salary(salary):
        if salary < 30000:
            return '<30K'
        elif salary < 50000:
            return '30K–50K'
        elif salary < 70000:
            return '50K–70K'
        else:
            return '70K+'

    df_filtered['Salary_Group'] = df_filtered['Starting_Salary'].apply(categorize_salary)

    sunburst_data = df_filtered.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')
    total_count = sunburst_data['Count'].sum()
    sunburst_data['Percentage'] = (sunburst_data['Count'] / total_count * 100).round(2)

    ent_totals = sunburst_data.groupby('Entrepreneurship')['Count'].sum()
    sunburst_data['Ent_Label'] = sunburst_data['Entrepreneurship'].map(lambda x: f"{x}<br>{round(ent_totals[x] / total_count * 100, 2)}%")

    field_totals = sunburst_data.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].sum()
    sunburst_data['Field_Label'] = sunburst_data.apply(
        lambda row: f"{row['Field_of_Study']}<br>{round(field_totals[(row['Entrepreneurship'], row['Field_of_Study'])] / total_count * 100, 2)}%", axis=1)

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

    color_map = {}
    for field, color in yes_colors.items():
        color_map[f"Yes - {field}"] = color
    for field, color in no_colors.items():
        color_map[f"No - {field}"] = color
    color_map['Yes'] = '#ffd16a'
    color_map['No'] = '#ffd16a'

    fig_sunburst = px.sunburst(
        sunburst_data,
        path=['Ent_Label', 'Field_Label', 'Salary_Label'],
        values='Count',
        color='Ent_Field',
        color_discrete_map=color_map,
        custom_data=['Percentage'],
        title='Career Path Insights: Education, Salary & Entrepreneurship'
    )

    fig_sunburst.update_traces(
        insidetextorientation='radial',
        maxdepth=2,
        branchvalues="total",
        textinfo='label+text',
        hovertemplate="<b>%{label}</b><br>Value: %{value}<br>"
    )

    fig_sunburst.update_layout(
        width=500,
        height=500,
        margin=dict(t=50, l=0, r=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_sunburst, use_container_width=True)

    # === STACKED BAR CHART ===
    df_grouped = df_filtered.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
    df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

    colors = {'Yes': '#FFD700', 'No': '#004080'}
    order_levels = ['Entry', 'Mid', 'Senior', 'Executive']
    levels_to_show = [lvl for lvl in order_levels if lvl in selected_levels]

    cols = st.columns(2)

    for i, lvl in enumerate(levels_to_show):
        data_lvl = df_grouped[df_grouped['Current_Job_Level'] == lvl]
        if data_lvl.empty:
            with cols[i % 2]:
                st.write(f"### {lvl} — No data")
            continue

        y_col = 'Percentage' if mode == "Percentage (%)" else 'Count'
        fmt = (lambda x: f"{x:.0%}") if mode == "Percentage (%)" else (lambda x: str(x))
        y_axis_title = "Percentage" if mode == "Percentage (%)" else "Count"
        y_tick_format = ".0%" if mode == "Percentage (%)" else ""

        fig_bar = go.Figure()

        for status in selected_statuses:
            filtered_status = data_lvl[data_lvl['Entrepreneurship'] == status]
            fig_bar.add_trace(go.Bar(
                x=filtered_status['Age'].astype(str),
                y=filtered_status[y_col],
                name=status,
                marker_color=colors.get(status, '#CCCCCC'),
                text=filtered_status[y_col].apply(fmt),
                textposition='inside'
            ))

        fig_bar.update_layout(
            title=f"Entrepreneurship Distribution — {lvl}",
            barmode='stack',
            xaxis_title="Age",
            yaxis_title=y_axis_title,
            yaxis_tickformat=y_tick_format,
            yaxis_range=[0, 1] if mode == "Percentage (%)" else None,
            template="plotly_white",
            legend_title_text="Entrepreneurship",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        with cols[i % 2]:
            st.plotly_chart(fig_bar, use_container_width=True)

    with st.expander("📊 **Stacked Bar Chart Description**"):
        st.markdown("""<div style="background-color: #FFFFFF; padding: 25px; border-radius: 20px; color: #5D4037; font-size: 16px; line-height: 1.6; font-weight: 500;">
        The plot provides a visual representation of the proportion of entrepreneurship across different job levels and age groups... [Cắt ngắn phần mô tả nếu cần]
        </div>""", unsafe_allow_html=True)

with tab3:
    st.subheader("Insights & Conclusions")
    st.write("Summary of key insights from the visualisations.")
