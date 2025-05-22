import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = pd.DataFrame({
    "Years_to_Promotion": [1, 2, 3, 4],
    "Entry": [5.4, 5.3, 5.6, 5.25],
    "Mid": [5.7, 5.5, 5.7, 5.85],
})

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Years_to_Promotion"], y=df["Entry"],
    mode="lines+markers", name="Entry",
    line=dict(color="blue")
))
fig.add_trace(go.Scatter(
    x=df["Years_to_Promotion"], y=df["Mid"],
    mode="lines+markers", name="Mid",
    line=dict(color="orange")
))

fig.update_layout(
    title="Average Work-Life Balance by Years to Promotion",
    xaxis_title="Years to Promotion",
    yaxis_title="Average Work-Life Balance",
    hovermode="x unified"  # rất quan trọng!
)

st.plotly_chart(fig)
