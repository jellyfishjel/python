import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Career Path Sunburst",
    layout="wide",
    page_icon="🌞"
)

st.title("Career Path Sunburst")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

df = load_data()

# Categorize starting salary into ranges
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

# Group data for sunburst chart
sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')

# Create combined label for color mapping
sunburst_data['Ent_Field'] = sunburst_data['Entrepreneurship'] + " - " + sunburst_data['Field_of_Study']

# Define color maps
yes_colors = {
    'Engineering': '#d2a56d',
    'Business': '#ce8b54',
    'Arts': '#bd7e4a',
    'Computer Science': '#ccaa87',
    'Medicine': '#83502e',
    'Law': '#96613d',
    'Mathematics': '#bd9c7b'
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

# Build the color map
color_map = {}
for ent in ['Yes', 'No']:
    for field in df['Field_of_Study'].unique():
        key = f"{ent} - {field}"
        if ent == 'Yes':
            color_map[key] = yes_colors.get(field, '#d49c6c')  # fallback color
        else:
            color_map[key] = no_colors.get(field, '#78c2d8')  # fallback color

# Add base colors for inner circle 
color_map['Yes'] = '#d49c6c'
color_map['No'] = '#78c2d8'

# Create the sunburst chart
fig = px.sunburst(
    sunburst_data,
    path=['Entrepreneurship', 'Field_of_Study', 'Salary_Group'],
    values='Count',
    color='Ent_Field',
    color_discrete_map=color_map,
    title='Career Path Insights: Education, Salary & Entrepreneurship'
)

fig.update_traces(
    textinfo='label+percent entry',
    insidetextorientation='radial',
    maxdepth=2,
    branchvalues="total"
)

# Layout with columns
col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 💡 How to use")
    st.markdown(
        """  
    - The chart displays all three levels:
      - **Entrepreneurship** (inner ring)  
      - **Field of Study** (middle ring)  
      - **Salary Group** (outer ring)
    - To focus on specific salary details, click on a segment (e.g., Arts) to **zoom in** and explore the salary distribution for that group.
    """
    )
