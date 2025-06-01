import streamlit as st
from PIL import Image

# ===== SETUP PAGE =====
st.set_page_config(page_title="Education Career App", layout="wide")

# ===== CSS: Set background image =====
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("images/homepage_bg.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===== NAVIGATION BAR =====
st.markdown("""
    <style>
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
    </style>
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
                text-align: center; 
                padding: 60px 20px; 
                border-radius: 15px;">
        <h1 style="font-size: 64px;">EDUCATION<br>CAREER<br>SUCCESS</h1>
        <br><br>
        <a href="#dataset">
            <button style="margin: 10px; padding: 12px 24px; font-size: 18px; border-radius: 12px;">Read the report</button>
        </a>
        <a href="#team">
            <button style="margin: 10px; padding: 12px 24px; font-size: 18px; border-radius: 12px;">Learn about us</button>
        </a>
    </div>
""", unsafe_allow_html=True)

# ===== TEAM SECTION =====
st.markdown('<a name="team"></a>', unsafe_allow_html=True)
st.subheader("Our Team ✨")

# Save team data
team_members = [
    {"name": "Nguyễn Kiều Anh", "image": "team/Nguyễn Kiều Anh.png"},
    {"name": "Lê Nguyễn Khánh Phương", "image": "team/Lê Nguyễn Khánh Phương.png"},
    {"name": "Nguyễn Bảo Ngọc", "image": "team/Nguyễn Bảo Ngọc.png"},
    {"name": "Nguyễn Trần Khánh Linh", "image": "team/Nguyễn Trần Khánh Linh.png"},
    {"name": "Nguyễn Huỳnh Bảo Nguyên", "image": "team/Nguyễn Huỳnh Bảo Nguyên.png"},
    {"name": "Vũ Thị Thu Thảo", "image": "team/Vũ Thị Thu Thảo.png"},
    {"name": "Sazahng", "image": "team/Sazahng.png"},
]

# Chia nhóm thành 2 trang hiển thị
if "team_page" not in st.session_state:
    st.session_state.team_page = 1

def show_team(page):
    start = 0 if page == 1 else 4
    end = 4 if page == 1 else len(team_members)
    members = team_members[start:end]

    cols = st.columns(len(members))
    for col, member in zip(cols, members):
        with col:
            st.image(member["image"], width=150)
            st.markdown(f"**{member['name']}**")

    col1, col2 = st.columns([1, 9])
    with col1:
        if st.session_state.team_page == 2:
            if st.button("⬅️", key="prev"):
                st.session_state.team_page = 1
    with col2:
        if st.session_state.team_page == 1:
            if st.button("➡️", key="next"):
                st.session_state.team_page = 2

show_team(st.session_state.team_page)
