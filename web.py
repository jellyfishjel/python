import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import base64

# === PAGE CONFIGURATION ===
st.set_page_config(
    page_title="Education & Career Success",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === BACKGROUND IMAGE SETUP ===
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_path = r"D:\VGU\Homepage.png"  # ⚠️ Đảm bảo đường dẫn ảnh đúng
img_base64 = get_base64(img_path)

# === INJECT BACKGROUND CSS ===
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    .main-title {{
        text-align: center;
        color: #FF6F00;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 30px;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        justify-content: flex-start;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #FFE0B2;
        border-radius: 16px;
        padding: 6px 14px;
        font-size: 18px;
        font-weight: 600;
        color: #E65100;
        transition: all 0.3s ease;
        height: 42px;
        min-width: 120px;
        text-align: center;
        border: none;
        box-shadow: none;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #FF9800, #FF7043);
        color: white;
        transform: none;
        box-shadow: none;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background: linear-gradient(135deg, #FFD180, #FFB74D);
        cursor: pointer;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# === MAIN TITLE ===
st.markdown('<div class="main-title">Education & Career Success</div>', unsafe_allow_html=True)

# === LOAD DATA ===
@st.cache_data
def load_data():
    return pd.read_csv("D:\\VGU\\education_career_success.csv")

df = load_data()

# === TABS ===
tab1, tab2, tab3 = st.tabs(["Homepage", "Visualisation", "Insights"])

# === CONTENT IN EACH TAB ===
# 🔹 Your full tab content goes here exactly as you wrote it earlier:
# For brevity, I won’t repeat the long logic here — you can paste your exact tab2 and tab3 contents here

with tab1:
    st.subheader("Welcome to the Education & Career Success Portal")
    st.write("This platform explores the relationship between education and career outcomes.")

with tab2:
    # ... your full tab2 content (Line Chart, Sunburst, Stacked Bar Chart)
    pass

with tab3:
    st.subheader("Insights & Conclusions")
    st.write("Summary of key insights from the visualisations.")
