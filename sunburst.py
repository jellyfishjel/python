import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Career Insights Dashboard",
    layout="wide",
    page_icon="🍩"
)

st.title("🍩 Career Insights Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name='education_career_success')

df = load_data()
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]  # Ensure clean binary values

# Sidebar filters
st.sidebar.title("🎯 Filter Options")

# Gender filter
genders = sorted(df['Gender'].dropna().unique())
selected_genders = st.sidebar.selectbox("Select Gender", genders, default=genders)

# Job level filter
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Filtered base dataframe
df_filtered = df[
    (df['Gender'].isin(selected_genders)) &
    (df['Current_Job_Level'] == selected_level)
]

# Age filter (based on filtered data)
min_age, max_age = int(df_filtered['Age'].min()), int(df_filtered['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Entrepreneurship filter
selected_statuses = st.sidebar.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])

# Function to generate donut chart without legend
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
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    return fig

# Display 3 donut charts
st.subheader("📊 Donut Charts Overview")
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(plot_donut(df_filtered, 'Entrepreneurship', 'Entrepreneurship'), use_container_width=True)
with col2:
    st.plotly_chart(plot_donut(df_filtered, 'Years_to_Promotion', 'Years to Promotion'), use_container_width=True)
with col3:
    st.plotly_chart(plot_donut(df_filtered, 'Field_of_Study', 'Field of Study'), use_container_width=True)

st.markdown(f"### 👥 Total Records for '{selected_level}' and selected gender(s): {len(df_filtered)}")

# Bar + Area Chart Section
df_grouped = (
    df_filtered.groupby(['Age', 'Entrepreneurship'])
      .size()
      .reset_index(name='Count')
)
df_grouped['Percentage'] = df_grouped.groupby('Age')['Count'].transform(lambda x: x / x.sum())


# Font size utility
def font_size_by_count(n):
    return {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8, 10: 7}.get(n, 6)

color_map = {'Yes': '#FFD700', 'No': '#004080'}

# Display charts if data is available
if filtered.empty:
    st.write(f"### ⚠️ No data available for selected filters.")
else:
    st.subheader("📈 Entrepreneurship by Age – Detailed Charts")
    ages = sorted(filtered['Age'].unique())
    font_size = font_size_by_count(len(ages))
    chart_width = max(400, min(1200, 50 * len(ages) + 100))

    # Bar Chart
    fig_bar = px.bar(
        filtered,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Percentage': 'Percentage'},
        height=400,
        width=chart_width,
        title=f"{selected_level} Level – Entrepreneurship by Age (%)"
    )

    for status in ['No', 'Yes']:
        for _, row in filtered[filtered['Entrepreneurship'] == status].iterrows():
            if row['Percentage'] > 0:
                y_pos = 0.2 if status == 'No' else 0.9
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
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90,
        bargap=0.1
    )
    fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

    # Area Chart
    fig_area = px.area(
        filtered,
        x='Age',
        y='Count',
        color='Entrepreneurship',
        markers=True,
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Count': 'Count'},
        height=400,
        width=chart_width,
        title=f"{selected_level} Level – Entrepreneurship by Age (Count)"
    )
    fig_area.update_traces(line=dict(width=2), marker=dict(size=8))
    fig_area.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90
    )
    fig_area.update_yaxes(title="Count")

    # Display side by side
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_area, use_container_width=True)
