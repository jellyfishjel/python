import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Education & Career Insights", layout="wide", page_icon="📊")
st.title("📊 Education & Career Insights Dashboard")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🌞 Career Path Sunburst",
    "📈 Work-Life Balance vs Promotion",
    "🚀 Entrepreneurship by Age",
    "🎓 GPA vs Salary"
])

# ---------- TAB 1 ----------
with tab1:
    st.subheader("🧑‍🎓 Career Path Sunburst")

    @st.cache_data
    def load_data():
        return pd.read_excel("education_career_success.xlsx")

    df = load_data()

    df1 = load_sunburst_data()


    def categorize_salary(salary):
        if salary < 30000: return '<30K'
        elif salary < 50000: return '30K–50K'
        elif salary < 70000: return '50K–70K'
        else: return '70K+'

    df1['Salary_Group'] = df1['Starting_Salary'].apply(categorize_salary)
    sb = df1.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')
    total = sb['Count'].sum()
    sb['Percentage'] = (sb['Count'] / total * 100).round(2)
    ent_totals = sb.groupby('Entrepreneurship')['Count'].sum()
    sb['Ent_Label'] = sb['Entrepreneurship'].map(lambda x: f"{x}<br>{round(ent_totals[x]/total*100,2)}%")
    field_totals = sb.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].sum()
    sb['Field_Label'] = sb.apply(lambda row: f"{row['Field_of_Study']}<br>{round(field_totals[(row['Entrepreneurship'], row['Field_of_Study'])]/total*100,2)}%", axis=1)
    sb['Salary_Label'] = sb['Salary_Group'] + '<br>' + sb['Percentage'].astype(str) + '%'
    sb['Ent_Field'] = sb['Entrepreneurship'] + " - " + sb['Field_of_Study']

    yes_colors = {'Engineering': '#aedea7', 'Business': '#dbf1d5', 'Arts': '#0c7734',
                  'Computer Science': '#73c375', 'Medicine': '#00441b', 'Law': '#f7fcf5', 'Mathematics': '#37a055'}
    no_colors = {'Engineering': '#005b96', 'Business': '#03396c', 'Arts': '#009ac7',
                 'Computer Science': '#8ed2ed', 'Medicine': '#b3cde0', 'Law': '#5dc4e1', 'Mathematics': '#0a70a9'}
    color_map = {f"Yes - {k}": v for k, v in yes_colors.items()} | {f"No - {k}": v for k, v in no_colors.items()}
    color_map['Yes'] = '#ffd16a'
    color_map['No'] = '#ffd16a'

    fig1 = px.sunburst(sb, path=['Ent_Label', 'Field_Label', 'Salary_Label'], values='Count',
                       color='Ent_Field', color_discrete_map=color_map, title='Career Path: Education, Salary & Entrepreneurship')
    fig1.update_traces(insidetextorientation='radial', maxdepth=2, branchvalues="total", hovertemplate="<b>%{label}</b><br>Value: %{value}<br>")
    fig1.update_layout(margin=dict(t=30, l=0, r=0, b=0), height=500)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.markdown("### 💡 How to Use")
        st.markdown("""- Inner ring: Entrepreneurship  
- Middle ring: Field of Study  
- Outer ring: Salary Group  
- Hover or click to explore.""")

# ---------- TAB 2 ----------
with tab2:
    st.subheader("📈 Work-Life Balance by Promotion Timeline")
    @st.cache_data
    def load_line_data():
        return pd.read_csv("education_career_success.csv")
    df2 = load_line_data()

    avg_balance = df2.groupby(['Current_Job_Level', 'Years_to_Promotion'])['Work_Life_Balance'].mean().reset_index()
    job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
    avg_balance['Current_Job_Level'] = pd.Categorical(avg_balance['Current_Job_Level'], categories=job_levels_order, ordered=True)

    selected_levels = st.sidebar.multiselect("Select Job Levels", options=job_levels_order + ["All"], default=["All"])
    filtered_data = avg_balance if "All" in selected_levels or not selected_levels else avg_balance[avg_balance["Current_Job_Level"].isin(selected_levels)]

    fig2 = go.Figure()
    colors = {"Entry": "#1f77b4", "Mid": "#ff7f0e", "Senior": "#2ca02c", "Executive": "#d62728"}
    for level in job_levels_order:
        if "All" in selected_levels or level in selected_levels:
            data = filtered_data[filtered_data["Current_Job_Level"] == level]
            fig2.add_trace(go.Scatter(x=data["Years_to_Promotion"], y=data["Work_Life_Balance"],
                                      mode="lines+markers", name=level, line=dict(color=colors[level]),
                                      hovertemplate=f"%{{y:.2f}}"))

    fig2.update_layout(title="Work-Life Balance vs. Years to Promotion", xaxis_title="Years to Promotion",
                       yaxis_title="Average Work-Life Balance", hovermode="x unified", height=600, title_x=0.5)
    st.plotly_chart(fig2, use_container_width=True)

# ---------- TAB 3 ----------
with tab3:
    st.subheader("🚀 Entrepreneurship by Age and Job Level")
    df3 = pd.read_csv("education_career_success.csv")
    df3 = df3[df3['Entrepreneurship'].isin(['Yes', 'No'])]
    df_grouped = df3.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
    df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

    job_levels = sorted(df_grouped['Current_Job_Level'].unique())
    selected_levels = st.sidebar.multiselect("Job Levels", job_levels, default=job_levels)
    min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())
    age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))
    selected_statuses = st.sidebar.multiselect("Entrepreneurship", ['Yes', 'No'], default=['Yes', 'No'])

    filtered = df_grouped[
        df_grouped['Current_Job_Level'].isin(selected_levels) &
        df_grouped['Entrepreneurship'].isin(selected_statuses) &
        df_grouped['Age'].between(age_range[0], age_range[1])
    ]

    def get_font_size(n): return {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8, 10: 7}.get(n, 6)
    color_map = {'Yes': '#FFD700', 'No': '#004080'}
    level_order = ['Entry', 'Executive', 'Mid', 'Senior']
    visible_levels = [lvl for lvl in level_order if lvl in selected_levels]

    for level in visible_levels:
        data = filtered[filtered['Current_Job_Level'] == level]
        if data.empty:
            st.write(f"### {level} – No data available")
            continue

        ages = sorted(data['Age'].unique())
        font_size = get_font_size(len(ages))
        chart_width = max(400, min(1200, 50 * len(ages) + 100))

        fig_bar = px.bar(data, x='Age', y='Percentage', color='Entrepreneurship', barmode='stack',
                         color_discrete_map=color_map, height=400, width=chart_width,
                         title=f"{level} Level – Entrepreneurship by Age (%)")
        for status in ['No', 'Yes']:
            for _, row in data[data['Entrepreneurship'] == status].iterrows():
                if row['Percentage'] > 0:
                    y_pos = 0.20 if status == 'No' else 0.90
                    fig_bar.add_annotation(x=row['Age'], y=y_pos, text=f"{row['Percentage']:.0%}", showarrow=False,
                                           font=dict(color="white", size=font_size), xanchor="center", yanchor="middle")
        fig_bar.update_yaxes(tickformat=".0%", title="Percentage")
        fig_bar.update_layout(xaxis_tickangle=90, bargap=0.1)

        fig_area = px.area(data, x='Age', y='Count', color='Entrepreneurship', markers=True,
                           color_discrete_map=color_map, height=400, width=chart_width,
                           title=f"{level} Level – Entrepreneurship by Age (Count)")
        fig_area.update_layout(xaxis_tickangle=90)
        fig_area.update_yaxes(title="Count")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.plotly_chart(fig_area, use_container_width=True)

# ---------- TAB 4 ----------
with tab4:
    st.subheader("🎓 GPA vs Starting Salary")
    uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

    if uploaded_file:
        df4 = pd.read_excel(uploaded_file, sheet_name="education_career_success")
        gpa_bins = [2.0, 2.5, 3.0, 3.5, 4.0]
        gpa_labels = ["2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"]
        df4["GPA_Group"] = pd.cut(df4["University_GPA"], bins=gpa_bins, labels=gpa_labels, include_lowest=True)

        selected_gpa_group = st.selectbox("🎯 Select GPA Group", options=["All"] + gpa_labels)
        min_salary, max_salary = int(df4["Starting_Salary"].min()), int(df4["Starting_Salary"].max())
        salary_range = st.slider("💰 Salary Range", min_salary, max_salary, (min_salary, max_salary), step=1000)

        filtered_df = df4[(df4["Starting_Salary"] >= salary_range[0]) & (df4["Starting_Salary"] <= salary_range[1])]
        if selected_gpa_group != "All":
            filtered_df = filtered_df[filtered_df["GPA_Group"] == selected_gpa_group]

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.regplot(x='University_GPA', y='Starting_Salary', data=filtered_df, ax=ax, scatter_kws={'alpha': 0.7})
        ax.set_title('University GPA vs. Starting Salary')
        ax.set_xlabel('University GPA')
        ax.set_ylabel('Starting Salary')
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.warning("⚠️ Please upload an Excel file with a sheet named 'education_career_success'.")
