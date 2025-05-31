import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from PIL import Image

# === SETUP PAGE === (⚠️ dòng này phải đứng đầu!)
st.set_page_config(page_title="Education Career App", layout="wide")

# === CSS for full-page background ===
page_bg_img = '''
<style>
.stApp {
    background-image: url("images/homepage_bg.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# === NAVIGATION BAR ===
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

# === HOMEPAGE SECTION ===
st.markdown('<a name="home"></a>', unsafe_allow_html=True)

st.markdown("""
    <div style="background: linear-gradient(to right, #8a4b36, #6f3a2b); 
                color: white; 
                text-align: center; 
                padding: 50px 20px; 
                border-radius: 12px;">
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

# === ABOUT OUR TEAM SECTION ===
st.markdown('<a name="team"></a>', unsafe_allow_html=True)
st.subheader("Our Team ✨")

if "team_page" not in st.session_state:
    st.session_state.team_page = 1

def show_team(page):
    members = [
        ("Kiều Anh", "images/kieu_anh_1.png"),
        ("Kiều Anh", "images/kieu_anh_2.png"),
        ("Kiều Anh", "images/kieu_anh_3.png"),
        ("Kiều Anh", "images/kieu_anh_4.png"),
        ("Kiều Anh", "images/kieu_anh_5.png"),
        ("Kiều Anh", "images/kieu_anh_6.png"),
        ("Kiều Anh", "images/kieu_anh_7.png"),
    ]

    col1, col2, col3, col4 = st.columns(4)

    start = 0 if page == 1 else 4
    end = 4 if page == 1 else 7
    chunk = members[start:end]
    cols = [col1, col2, col3, col4] if page == 1 else [col1, col2, col3]

    for i, (name, img_path) in enumerate(chunk):
        with cols[i]:
            st.image(img_path, width=150)
            st.write(f"**{name}**")

    # Navigation buttons
    colL, colR = st.columns([1, 9])
    with colL:
        if st.button("⬅️", key="prev") and st.session_state.team_page == 2:
            st.session_state.team_page = 1
    with colR:
        if st.button("➡️", key="next") and st.session_state.team_page == 1:
            st.session_state.team_page = 2

show_team(st.session_state.team_page)
