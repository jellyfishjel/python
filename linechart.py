import streamlit as st
import plotly.graph_objects as go
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

df = df.pivot_table(
    index='Years_to_Promotion',
    columns='Current_Job_Level',
    values='Work_Life_Balance'
).reset_index()
df.columns.name = None


fig = go.Figure()
levels = {
    "Entry": "blue",
    "Mid": "orange",
    "Senior": "green",
    "Executive": "red"
}

for level, color in levels.items():
    if level in df.columns:
        fig.add_trace(go.Scatter(
            x=df["Years_to_Promotion"],
            y=df[level],
            mode="lines+markers",
            name=level,
            line=dict(color=color),
            hovertemplate=f"%{{y:.2f}}"
        ))

fig.update_layout(
    title="Average Work-Life Balance by Years to Promotion",
    xaxis_title="Years to Promotion",
    yaxis_title="Average Work-Life Balance",
    hovermode="x unified",
    template="plotly_dark"
)

st.plotly_chart(fig)
