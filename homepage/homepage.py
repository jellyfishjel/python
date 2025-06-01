import streamlit as st
from PIL import Image

# ===== SETUP PAGE =====
st.set_page_config(page_title="Education Career App", layout="wide")

# ===== CSS: Custom Background + Navigation =====
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("images/homepage_bg.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .navbar {
        display: flex;
        justify-content: center;
        gap: 40px;
        font-size: 18px;
        margin-bottom: 30px;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        font-weight: bold;
    }
    .team-section {
        background-image: url("images/team_section_bg.png");
        background-size: cover;
        background-position: center;
        padding: 50px 30px;
        border-radius: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===== NAVIGATION BAR =====
st.markdown("""
<div class="navbar">
    <a href="#home">Homepage</a>
    <a href="#dataset">Dataset Overview</a>
    <a href="#plot">Plot</a>
    <a href="#code">Code</a>
</div>
""", unsafe_allow_html=True)

# ===== HOMEPAGE SECTION =====
st.markdown('<a name="home"></a>', unsafe_allow_html=True)

st.markdown("""
<div style="background: rgba(0, 0, 0, 0.5); 
            color: white; 
            text-align: left; 
            padding: 60px 20px; 
            border-radius: 15px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;">
    <div style="font-size: 64px; font-weight: bold;">
        EDUCATION<br>CAREER<br>SUCCESS
    </div>
    <div>
        <img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Example.svg" width="300">
    </div>
</div>
<br><br>
<a href="#team">
    <button style="margin: 10px; padding: 12px 24px; font-size: 18px; border-radius: 20px; background: linear-gradient(to right, #f3ccab, #e2dbc2); border: none;">
        Learn about us
    </button>
</a>
""", unsafe_allow_html=True)

# ===== TEAM SECTION =====
st.markdown('<a name="team"></a>', unsafe_allow_html=True)
st.markdown("<div class='team-section'>", unsafe_allow_html=True)
st.subheader("Our team ⭐")

# === Team Members List ===
team_members = [
    {"name": "Kiều Anh", "image": "images/team/Nguyễn Kiều Anh.png"},
    {"name": "Khánh Phương", "image": "images/team/Lê Nguyễn Khánh Phương.png"},
    {"name": "Bảo Ngọc", "image": "images/team/Nguyễn Bảo Ngọc.png"},
    {"name": "Khánh Linh", "image": "images/team/Nguyễn Trần Khánh Linh.png"},
    {"name": "Bảo Nguyên", "image": "images/team/Nguyễn Huỳnh Bảo Nguyên.png"},
    {"name": "Thu Thảo", "image": "images/team/Vũ Thị Thu Thảo.png"},
    {"name": "Bội Ngọc", "image": "images/team/Sazahng.png"},
]

# === Pagination State ===
if "team_page" not in st.session_state:
    st.session_state.team_page = 1

def show_team(page):
    start = 0 if page == 1 else 4
    end = 4 if page == 1 else len(team_members)
    members = team_members[start:end]

    cols = st.columns(len(members))
    for col, member in zip(cols, members):
        with col:
            st.image(member["image"], width=180)
            st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 18px'>{member['name']}</div>", unsafe_allow_html=True)

    # Navigation Buttons
    nav_col1, nav_col2 = st.columns([10, 1])
    with nav_col1:
        pass
    with nav_col2:
        left, right = st.columns(2)
        with left:
            if st.session_state.team_page == 2 and st.button("⬅️", key="prev"):
                st.session_state.team_page = 1
        with right:
            if st.session_state.team_page == 1 and st.button("➡️", key="next"):
                st.session_state.team_page = 2

show_team(st.session_state.team_page)

st.markdown("</div>", unsafe_allow_html=True)
