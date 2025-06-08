import pandas as pd
import streamlit as st

# Load dataset
df = pd.read_excel("education_career_success.xlsx")

# Set page configuration
st.set_page_config(page_title="Dataset Overview", layout="wide")

# --- Section 1: Introduction ---
st.header("Introduction")
st.markdown("""
The “Education and Career Success” dataset provides valuable insights into the relationship
between academic background, career progression, and financial outcomes. By delving into various
categories of this dataset, we can uncover valuable insights into how different fields of study,
academic performance, and practical experiences impact career satisfaction, work-life balance, and
long-term professional achievements.

This report is our project for **R for Data Science** course. The report contains plots that are created
by using **RStudio** to visualize information from the dataset in a more accessible way. Each diagram
is followed by a detailed description and code from RStudio to provide readers with clear
explanation on statistical data and how RStudio is used in practical data analysis.
""")

# --- Section 2: Dataset Overview ---
st.header("Dataset Overview")
st.markdown("""
This dataset has **20 columns** and **5000 rows**, exploring the relationship
between academic performance and career success.  
It includes students' educational backgrounds, skills, and career outcomes.  
The dataset can be used for:
- Predicting job success based on education
- Identifying key factors influencing salaries
- Understanding the role of networking and internships in career growth
""")

st.subheader("Preview of Dataset")
st.dataframe(df.head(), use_container_width=True)

# --- Section 3: Variable Explanation ---
st.header("Variable Explanation")

## 1. Student Information
st.subheader("1. Student Information")
st.markdown("""
- `Student_ID`: Order number to identify each student  
- `Age`: Age of student (18–30 years old)  
- `Gender`: Male, Female, or Others  
- `High_School_GPA`: GPA in high school (2.0–4.0 scale)  
- `SAT_score`: Standardized SAT test score (900–1600)  
- `University_Ranking`: Rank of the university attended (1–1000)  
- `University_GPA`: GPA in university (2.0–4.0 scale)  
- `Field_of_Study`: Student’s major (Arts, Law, Business, Medicine, CS, Engineering, Math)
""")

## 2. Academic Performance
st.subheader("2. Academic Performance")
st.markdown("""
- `Internships_Completed`: Number of internships (0–4)  
- `Projects_Completed`: Number of academic/personal projects (0–9)  
- `Certifications`: Number of additional certifications earned (0–5)  
- `Soft_Skills_Score`: Soft skills rating (1–10)  
- `Networking_Score`: Networking and connections score (1–10)
""")

## 3. Career Outcomes
st.subheader("3. Career Outcomes")
st.markdown("""
- `Job_Offers`: Number of job offers post-graduation (0–5)  
- `Starting_Salary`: First job salary in USD ($25,000–$150,000)
""")
