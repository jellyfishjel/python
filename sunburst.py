import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sunburst Chart", layout="wide")
st.title("🌞 Sunburst Chart – Salary, Field, and Entrepreneurship")

@st.cache_data
def load_data():
    df = pd.read_excel("education_career_success.xlsx")
    return df

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
        total = sunburst_data['Count'].sum()
        sunburst_data['Percentage'] = (sunburst_data['Count'] / total * 100).round(2)

        sunburst_data['Entrepreneurship_Label'] = sunburst_data['Entrepreneurship'] + ' (' + (
            sunburst_data.groupby('Entrepreneurship')['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
        ) + '%)'

        sunburst_data['Field_Label'] = sunburst_data['Field_of_Study'] + '\n' + (
            sunburst_data.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].transform(lambda x: round(x.sum() / total * 100, 1)).astype(str)
        ) + '%'

        sunburst_data['Salary_Label'] = sunburst_data['Salary_Group'] + '\n' + sunburst_data['Percentage'].astype(str) + '%'

        if color_mode == "Color by Salary Group":
            label_yes = sunburst_data[sunburst_data['Entrepreneurship'] == 'Yes']['Entrepreneurship_Label'].iloc[0]
            label_no = sunburst_data[sunburst_data['Entrepreneurship'] == 'No']['Entrepreneurship_Label'].iloc[0]

            color_discrete_map = {
                label_yes: "#2ECC71",
                label_no: "#E74C3C",
            }

            fig = px.sunburst(
                sunburst_data,
                path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
                values='Percentage',
                color='Entrepreneurship_Label',
                color_discrete_map=color_discrete_map,
                title='🎯 Sunburst Chart Colored by Entrepreneurship (Yes=Green, No=Red)'
            )

        else:
            fig = px.sunburst(
                sunburst_data,
                path=['Entrepreneurship_Label', 'Field_Label', 'Salary_Label'],
                values='Percentage',
                color='Percentage',
                color_continuous_scale='Turbo',
                title='🌈 Color by Percentage of Total'
            )
            fig.update_coloraxes(cmin=0, cmax=100, colorbar_title="Percentage (%)")

        fig.update_traces(maxdepth=2, branchvalues="total")
        st.plotly_chart(fig, use_container_width=True)
