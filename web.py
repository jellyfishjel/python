import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Education & Career Success",
    layout="wide"
)

# Custom CSS for styling tabs and title
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #FF6F00;
            font-size: 40px;
            font-weight: bold;
            margin-bottom: 30px;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            justify-content: flex-start; /* Align tabs left */
        }
        .stTabs [data-baseweb="tab"] {
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
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #FF9800, #FF7043);
            color: white;
            transform: none;
            box-shadow: none;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background: linear-gradient(135deg, #FFD180, #FFB74D);
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.markdown('<div class="main-title">Education & Career Success</div>', unsafe_allow_html=True)

# Load data function (csv, fixed path)
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# Create Tabs
tab1, tab2, tab3 = st.tabs(["Homepage", "Visualisation", "Insights"])

with tab1:
    st.subheader("Welcome to the Education & Career Success Portal")
    st.write("This platform explores the relationship between education and career outcomes.")

with tab2:
    st.subheader("Data Visualisation")

    # ===== Line Chart =====
    df_line = df.pivot_table(
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
        template="plotly_dark"
    )

    st.plotly_chart(fig_line, use_container_width=True)

    # Line chart description inside expander with black text and no bold first line
    with st.expander("📈 **Line Chart Description: Work-Life Balance & Years to Promotion**"):
        st.markdown("""
        <div style="
            padding: 20px; 
            border-radius: 16px; 
            color: black; 
            font-size: 16px; 
            margin-top: 10px;
            line-height: 1.5;
            border: none;
            box-shadow: none;
        ">
        The given line graph shows the connection between average work-life balance and years to promotion of 4 job levels,
        including Entry, Mid, Senior, and Executive, to answer whether the time taken to receive the first promotion and work-life balance skills affect the current job level. Overall, the Mid and Senior groups record an upward trajectory, while the
        others follow a contrasting pattern. The level Executive undergoes the most dramatic downfall among the four.<br><br>
        In detail, the data for Entry witnessed a steady collapse, indicating that stronger work-life balance skills result in
        quicker promotion for new employees. Following the same pattern, the longer the time before the first promotion is,
        the deeper the balance score of the Executive level drops. It implies that in challenging positions like executives,
        people whose first promotion comes earlier may stand out in balancing life compared to others.<br><br>
        In contrast, the group Mid and Senior see a slight increase in the balance score when the period before the first
        promotion lasts longer. This may be explained by the experience gained over a longer time.<br><br>
        In conclusion, the line graph proves that the better work-life balance skills are, the shorter the time to first promotion.
        People with an early first promotion tend to have better work-life balance skills at all job levels. In contrast, people
        who received the first promotion later tend to have worse work-life balance skills when coming to higher positions.
        </div>
        """, unsafe_allow_html=True)

    # ===== Sunburst Chart =====
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
        hovertemplate=
            "<b>%{label}</b><br>" +
            "Value: %{value}<br>"
    )

    fig_sunburst.update_layout(
        width=500,
        height=500,
        margin=dict(t=50, l=0, r=0, b=0)
    )

    st.plotly_chart(fig_sunburst, use_container_width=True)

    # ===== Sidebar filters for stacked bar chart =====
    st.sidebar.title("Filters for Stacked Bar Chart")

    df_bar = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

    # Job levels sorted + sidebar multi-select
    job_levels = sorted(df_bar['Current_Job_Level'].unique())
    selected_levels = st.sidebar.multiselect("Job Levels", job_levels, default=job_levels)

    # Ages sorted + sidebar multi-select with 'ALL' option
    ages = sorted(df_bar['Age'].unique())
    ages_all = ['ALL'] + [str(a) for a in ages]
    selected_ages = st.sidebar.multiselect("Ages", ages_all, default=['ALL'])

    # Entrepreneurship status multi-select
    statuses = ['Yes', 'No']
    selected_statuses = st.sidebar.multiselect("Entrepreneurship", statuses, default=statuses)

    # Show mode radio
    mode = st.sidebar.radio("Show as:", ["Percentage (%)", "Count"], index=0)

    # Filter data based on sidebar
    df_grouped = df_bar.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
    df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

    if 'ALL' in selected_ages:
        filtered = df_grouped[
            (df_grouped['Current_Job_Level'].isin(selected_levels)) &
            (df_grouped['Entrepreneurship'].isin(selected_statuses))
        ]
    else:
        selected_ages_int = [int(a) for a in selected_ages]
        filtered = df_grouped[
            (df_grouped['Current_Job_Level'].isin(selected_levels)) &
            (df_grouped['Age'].isin(selected_ages_int)) &
            (df_grouped['Entrepreneurship'].isin(selected_statuses))
        ]

    colors = {'Yes': '#FFD700', 'No': '#004080'}
    order_levels = ['Entry', 'Mid', 'Senior', 'Executive']
    levels_to_show = [lvl for lvl in order_levels if lvl in selected_levels]

    cols = st.columns(2)

    for i, lvl in enumerate(levels_to_show):
        data_lvl = filtered[filtered['Current_Job_Level'] == lvl]
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
            legend_title_text="Entrepreneurship"
        )

        with cols[i % 2]:
            st.plotly_chart(fig_bar, use_container_width=True)

    # Stacked bar chart description inside expander with black text and no bold first line
    with st.expander("📊 **Stacked Bar Chart Description: Entrepreneurship by Job Level & Age**"):
        st.markdown("""
        <div style="
            padding: 20px; 
            border-radius: 16px; 
            color: black; 
            font-size: 16px; 
            margin-top: 10px;
            line-height: 1.5;
            border: none;
            box-shadow: none;
        ">
        This bar chart displays the distribution of entrepreneurship status (Yes or No) among employees at different job levels
        and ages. It helps illustrate how entrepreneurship varies by age and position within a company.<br><br>
        Users can filter by job level, age groups, and entrepreneurship status using the sidebar selectors. The chart can be
        shown in either percentage or count mode, providing flexibility for analysis.<br><br>
        The colors indicate entrepreneurship status: gold for Yes, and dark blue for No.<br><br>
        This visualization aids in understanding how entrepreneurship engagement differs across career stages.
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("Insights & Conclusions")
    st.write("Summary of key insights from the visualisations.")
