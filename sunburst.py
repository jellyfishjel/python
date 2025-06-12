import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Career Path Sunburst",
    layout="wide",
    page_icon="🌞"
)
st.title("🌞 Career Path Sunburst")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

df = load_data()

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

sunburst_data['Salary_Label'] = sunburst_data['Salary]()]()_
