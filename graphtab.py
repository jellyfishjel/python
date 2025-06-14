import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np

st.set_page_config(page_title="Entrepreneurship Insights", layout="wide")

@st.cache_data

def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# Sidebar Filters
st.sidebar.title("Global Filters")

# Gender Filter - Multiselect with auto-deselect logic
gender_options = ['All'] + sorted(df['Gender'].dropna().unique())

# Khởi tạo session state nếu chưa có
if "gender_filter" not in st.session_state:
    st.session_state.gender_filter = ['All']

# Hàm xử lý thay đổi lựa chọn
def update_gender_selection():
    current_selection = st.session_state.gender_filter.copy()

    if 'All' in current_selection:
        # Nếu chọn All cùng lúc với giới tính khác → chỉ giữ All
        st.session_state.gender_filter = ['All']
    elif len(current_selection) == 0:
        # Không chọn gì → mặc định chọn All
        st.session_state.gender_filter = ['All']
    else:
        # Chọn riêng từng gender → giữ nguyên (và bỏ All nếu có)
        st.session_state.gender_filter = [g for g in current_selection if g != 'All']

# Multiselect với callback
st.sidebar.multiselect(
    "Select Gender(s)",
    gender_options,
    default=st.session_state.gender_filter,
    key="gender_filter",
    on_change=update_gender_selection
)

# Lọc dữ liệu
selected_genders = st.session_state.gender_filter
if 'All' not in selected_genders:
    df = df[df['Gender'].isin(selected_genders)]

# Job Level Filter
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Age Filter
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Entrepreneurship Status Filter - Individual Checkboxes
st.sidebar.markdown("**Select Entrepreneurship Status**")
show_yes = st.sidebar.checkbox("Yes", value=True)
show_no = st.sidebar.checkbox("No", value=True)

selected_statuses = []
if show_yes:
    selected_statuses.append("Yes")
if show_no:
    selected_statuses.append("No")

# Nếu không chọn gì, mặc định chọn cả 2 để tránh lỗi dữ liệu rỗng
if not selected_statuses:
    selected_statuses = ['Yes', 'No']
    
# Color mapping
color_map = {'Yes': '#FFD700', 'No': '#004080'}

# --- Main Tabs ---
graph_tab = st.tabs(["📊 Age & Job Offers", "📈 Age & Demographics"])

# === TAB 1 ===
with graph_tab[0]:
    st.title("Entrepreneurship and Job Offers by Age")
    st.markdown("Analyze the relationship between entrepreneurship status, job level, and job offers across age groups.")

    # Filtered data
    df_filtered = df[(df['Current_Job_Level'] == selected_level) &
                     (df['Age'].between(age_range[0], age_range[1])) &
                     (df['Entrepreneurship'].isin(selected_statuses))]

    # Grouped data for bar chart
    df_grouped = (
        df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
        .size()
        .reset_index(name='Count')
    )
    df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

    df_bar = df_grouped[
        (df_grouped['Current_Job_Level'] == selected_level) &
        (df_grouped['Age'].between(age_range[0], age_range[1])) &
        (df_grouped['Entrepreneurship'].isin(selected_statuses))
    ]

    even_ages = sorted(df_bar['Age'].unique())
    even_ages = [age for age in even_ages if age % 2 == 0]

    fig_bar = px.bar(
        df_bar,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes']},
        labels={'Age': 'Age', 'Percentage': 'Percentage'},
        height=450,
        width=1250,
        title=f"Entrepreneurship Distribution by Age – {selected_level} Level"
    )

    fig_bar.update_traces(
        hovertemplate="Entrepreneurship=%{customdata[0]}<br>Age=%{x}<br>Percentage=%{y:.0%}<extra></extra>",
        customdata=df_bar[['Entrepreneurship']].values,
        hoverinfo="skip"
    )

    fig_bar.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=0,
        bargap=0.1,
        xaxis=dict(tickvals=even_ages),
        yaxis=dict(title="Percentage", range=[0, 1], tickformat=".0%"),
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
    )

    df_avg_offers = (
        df_filtered
        .groupby(['Age', 'Entrepreneurship'])['Job_Offers']
        .mean()
        .reset_index()
    )

    fig_line = go.Figure()
    for status in selected_statuses:
        data_status = df_avg_offers[df_avg_offers["Entrepreneurship"] == status]
        fig_line.add_trace(go.Scatter(
            x=data_status["Age"],
            y=data_status["Job_Offers"],
            mode="lines+markers",
            name=status,
            line=dict(color=color_map[status], width=2),
            marker=dict(size=6),
            hovertemplate="%{y:.2f}"
        ))

    fig_line.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=0,
        hovermode="x unified",
        width=1250,
        xaxis=dict(
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikethickness=1.2,
            spikedash='dot',
            tickvals=even_ages
        ),
        yaxis=dict(
            title="Average Job Offers",
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikethickness=1.2,
            spikedash='dot'
        ),
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_line, use_container_width=True)

# === TAB 2 ===
with graph_tab[1]:
    st.title("Demographics by Age")

    chart_option = st.selectbox("Select Variable for Visualization", ['Gender', 'Field of Study'])

    df_demo = df[(df['Current_Job_Level'] == selected_level) &
                 (df['Age'].between(age_range[0], age_range[1])) &
                 (df['Entrepreneurship'].isin(selected_statuses))]

    if df_demo.empty:
        st.warning("Not enough data to display charts.")
    else:
        col1, col2 = st.columns([1, 1])

        # Density Area Chart
        with col1:
            fig_density = go.Figure()
            group_col = 'Gender' if chart_option == 'Gender' else 'Field_of_Study'
            title = f"Age Distribution by {group_col.replace('_', ' ')}"
            categories = df_demo[group_col].dropna().unique()

            for cat in categories:
                age_data = df_demo[df_demo[group_col] == cat]['Age']
                if len(age_data) > 1:
                    kde = gaussian_kde(age_data)
                    x_vals = np.linspace(age_range[0], age_range[1], 100)
                    y_vals = kde(x_vals)
                    fig_density.add_trace(go.Scatter(
                        x=x_vals,
                        y=y_vals,
                        mode='lines',
                        name=str(cat),
                        fill='tozeroy'
                    ))

            fig_density.update_layout(
                title=title,
                xaxis_title="Age",
                yaxis_title="Density",
                height=500,
                margin=dict(t=40, l=40, r=40, b=80),
                legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_density, use_container_width=True)

        # Donut Chart
        with col2:
            if chart_option == 'Gender':
                counts = df_demo['Gender'].value_counts().reset_index()
                counts.columns = ['Gender', 'Count']
                labels, values = counts['Gender'], counts['Count']
            else:
                counts = df_demo['Field_of_Study'].value_counts().reset_index()
                counts.columns = ['Field of Study', 'Count']
                labels, values = counts['Field of Study'], counts['Count']

            fig_donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
            fig_donut.update_layout(
                title=f"{chart_option} Distribution (Donut Chart)",
                height=350,
                margin=dict(t=40, l=40, r=40, b=40),
                showlegend=True
            )
            st.plotly_chart(fig_donut, use_container_width=True)
