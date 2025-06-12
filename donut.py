import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

# Load and preprocess data
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

df = load_data()
fig_combined = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "xy"}, {"type": "domain"}]],  # domain cho pie chart
    subplot_titles=("Age Distribution by Gender", "Gender Distribution")
)

# Density chart (area)
for gender in genders:
    gender_ages = filtered_df[filtered_df['Gender'] == gender]['Age']
    if len(gender_ages) > 1:
        kde = gaussian_kde(gender_ages)
        x_vals = np.linspace(age_range[0], age_range[1], 100)
        y_vals = kde(x_vals)

        fig_combined.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines',
                name=gender,
                fill='tozeroy'
            ),
            row=1, col=1
        )

# Donut chart
fig_combined.add_trace(
    go.Pie(
        labels=gender_counts['Gender'],
        values=gender_counts['Count'],
        hole=0.5,
        name="Gender",
        showlegend=True  # Legend gộp
    ),
    row=1, col=2
)

fig_combined.update_layout(
    title_text="Combined View: Age & Gender Distribution",
    height=500,
    showlegend=True,
    legend=dict(orientation="h", y=-0.2),
    margin=dict(t=60, l=40, r=40, b=60)
)

st.plotly_chart(fig_combined, use_container_width=True)




