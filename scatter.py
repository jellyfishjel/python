import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="GPA vs Salary", layout="centered")
st.title("🎓 University GPA vs. Starting Salary")

# Upload file
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

# Load Excel
df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # Group GPA into categories
    gpa_bins = [2.0, 2.5, 3.0, 3.5, 4.0]
    gpa_labels = ["2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"]
    df["GPA_Group"] = pd.cut(df["University_GPA"], bins=gpa_bins, labels=gpa_labels, include_lowest=True)

    # GPA filter with "All"
    gpa_filter_options = ["All"] + gpa_labels
    selected_gpa_group = st.selectbox("🎯 Select GPA Group", options=gpa_filter_options)

    # Salary slider
    min_salary = int(df["Starting_Salary"].min())
    max_salary = int(df["Starting_Salary"].max())
    salary_range = st.slider("💰 Select Starting Salary Range", min_value=min_salary, max_value=max_salary,
                             value=(min_salary, max_salary), step=1000)

    # Filter data
    filtered_df = df[(df["Starting_Salary"] >= salary_range[0]) & (df["Starting_Salary"] <= salary_range[1])]
    if selected_gpa_group != "All":
        filtered_df = filtered_df[filtered_df["GPA_Group"] == selected_gpa_group]

    # Plot
    st.subheader("📈 Scatter Chart")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(x='University_GPA', y='Starting_Salary', data=filtered_df, ax=ax, scatter_kws={'alpha': 0.7})
    ax.set_title('University GPA vs. Starting Salary')
    ax.set_xlabel('University GPA')
    ax.set_ylabel('Starting Salary')
    ax.grid(True)
    st.pyplot(fig)

else:
    st.warning("⚠️ Please upload a valid Excel file with a sheet named 'education_career_success'.")

