import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Career Insights by Job Level",
    layout="wide",
    page_icon="🍩"
)

st.title("🍩 Career Insights by Job Level")

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name='education_career_success')

df = load_data()

# Sidebar: Job Level Selection (single choice)
st.sidebar.header("🎯 Filter by Job Level")
job_levels = sorted(df['Current_Job_Level'].dropna().unique().tolist())
selected_level = st.sidebar.selectbox("Select one Job Level:", job_levels)

# Filter data based on selection
filtered_df = df[df['Current_Job_Level'] == selected_level]

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

# Layout: 3 donut charts
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(plot_donut(filtered_df, 'Gender', 'Gender Distribution'), use_container_width=True)

with col2:
    st.plotly_chart(plot_donut(filtered_df, 'Years_to_Promotion', 'Years to Promotion'), use_container_width=True)

with col3:
    st.plotly_chart(plot_donut(filtered_df, 'Field_of_Study', 'Field of Study'), use_container_width=True)

# Display number of records
st.markdown(f"### 👥 Total Records for '{selected_level}': {len(filtered_df)}")

# === Stacked Bar Chart for Years to Promotion by Age ===

# Nhóm dữ liệu theo Age và Years_to_Promotion
promotion_grouped = filtered_df.groupby(['Age', 'Years_to_Promotion']).size().reset_index(name='Count')
promotion_grouped['Percentage'] = promotion_grouped.groupby('Age')['Count'].transform(lambda x: x / x.sum())

# Chuyển giá trị sang chuỗi để biểu diễn rõ hơn
promotion_grouped['Years_to_Promotion'] = promotion_grouped['Years_to_Promotion'].astype(str)

# Đảm bảo thứ tự hợp lý cho Years_to_Promotion
promotion_order = sorted(
    promotion_grouped['Years_to_Promotion'].unique(),
    key=lambda x: float(x) if x.replace('.', '', 1).isdigit() else 999
)
promotion_grouped['Years_to_Promotion'] = pd.Categorical(promotion_grouped['Years_to_Promotion'], categories=promotion_order, ordered=True)
promotion_grouped = promotion_grouped.sort_values(['Age', 'Years_to_Promotion'])

# Biểu đồ stacked bar
# Tạo biến tuổi và chiều rộng riêng cho biểu đồ promotion
ages_promo = sorted(promotion_grouped['Age'].unique())
chart_width_promo = max(400, min(1200, 50 * len(ages_promo) + 100))

# Biểu đồ stacked bar
# Tạo biến tuổi và chiều rộng riêng cho biểu đồ promotion
ages_promo = sorted(promotion_grouped['Age'].unique())
chart_width_promo = max(400, min(1200, 50 * len(ages_promo) + 100))

# Biểu đồ stacked bar
fig_promo = px.bar(
    promotion_grouped,
    x='Age',
    y='Percentage',
    color='Entrepreneurship',
    barmode='stack',
    category_orders={'Entrepreneurship': promotion_order, 'Age': ages_promo},
    labels={'Age': 'Age', 'Percentage': 'Percentage'},
    height=400,
    width=chart_width_promo,
    title="📈 Years to Promotion Distribution by Age (%)"
)


fig_promo.update_layout(
    margin=dict(t=40, l=40, r=40, b=40),
    legend_title_text='Years to Promotion',
    xaxis_tickangle=90,
    bargap=0.1
)
fig_promo.update_yaxes(tickformat=".0%", title="Percentage")

# Hiển thị stacked bar
st.plotly_chart(fig_promo, use_container_width=True)
