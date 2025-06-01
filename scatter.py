import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("🎓 University GPA vs. Starting Salary")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

df = load_data()

df["GPA_Group"] = pd.cut(
    df["University_GPA"],
    bins=[2.0, 2.5, 3.0, 3.5, 4.0],
    labels=["2.0–2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"],
    include_lowest=True
)

selected_gpa = st.selectbox("Select GPA Group", ["All"] + df["GPA_Group"].cat.categories.tolist())
salary_min, salary_max = int(df["Starting_Salary"].min()), int(df["Starting_Salary"].max())
salary_range = st.slider("Select Starting Salary Range", salary_min, salary_max, (salary_min, salary_max), 1000)

# Filter
mask = (df["Starting_Salary"].between(*salary_range))
if selected_gpa != "All":
    mask &= (df["GPA_Group"] == selected_gpa)
filtered_df = df[mask]

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
sns.regplot(x='University_GPA', y='Starting_Salary', data=filtered_df, ax=ax, scatter_kws={'alpha': 0.7})
ax.set_xlabel('University GPA')
ax.set_ylabel('Starting Salary')
ax.grid(True)
st.pyplot(fig)

