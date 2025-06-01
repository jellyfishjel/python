import streamlit as st
from PIL import Image
import base64

# ===== SETUP PAGE =====
st.set_page_config(page_title="Education Career App", layout="wide")

# ===== EMBED BACKGROUND IMAGE IN BASE64 =====
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = get_base64("homepage/images/homepage_bg.png")

# ===== CSS STYLES =====
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    header {{
        background-color: transparent;
    }}
    .navbar {{
        display: flex;
        justify-content: center;
        gap: 40px;
        font-size: 18px;
        margin-bottom: 30px;
    }}
    .navbar a {{
        color: white;
        text-decoration: none;
        font-weight: bold;
    }}
    .homepage-box {{
        background: rgba(0, 0, 0, 0.5);
        color: white;
        text-align: center;
        padding: 60px 20px;
        border-radius: 15px;
    }}
    .homepage-box h1 {{
        font-size: 64px;
    }}
    .homepage-box button {{
        margin: 10px;
        padding: 12px 24px;
        font-size: 18px;
        border-radius: 12px;
        cursor: pointer;
    }}
    .team-img {{
        border-radius: 8px;
        width: 180px;
        height: 180px;
        object-fit: cover;
        display: block;
        margin: 0 auto 8px auto;
    }}
    </style>
""", unsafe_allow_html=True)

# ===== HOMEPAGE SECTION =====
st.markdown('<a name="home"></a>', unsafe_allow_html=True)
st.markdown("""
    <div class="homepage-box">
        <h1>EDUCATION<br>CAREER<br>SUCCESS</h1>
        <br><br>
        <a href="#team">
            <button>Learn about us</button>
        </a>
    </div>
""", unsafe_allow_html=True)

# ===== TEAM SECTION =====
st.markdown('<a name="team"></a>', unsafe_allow_html=True)
st.subheader("Our Team")

# ===== TEAM DATA =====
team_members = [
    {"name": "Kiều Anh", "image": "homepage/team/Nguyen Kieu Anh.png"},
    {"name": "Khánh Phương", "image": "homepage/team/Le Nguyen Khanh Phuong.png"},
    {"name": "Bảo Ngọc", "image": "homepage/team/Nguyen Bao Ngoc.png"},
    {"name": "Khánh Linh", "image": "homepage/team/Nguyen Tran Khanh Linh.png"},
    {"name": "Bảo Nguyên", "image": "homepage/team/Nguyen Huynh Bao Nguyen.png"},
    {"name": "Thu Thảo", "image": "homepage/team/Vu Thi Thu Thao.png"},
    {"name": "Bội Ngọc", "image": "homepage/team/Nguyen Boi Ngoc.png"},
]

# ===== PAGINATION STATE =====
if "team_page" not in st.session_state:
    st.session_state.team_page = 1

# ===== SHOW TEAM MEMBERS =====
def show_team(page):
    start = 0 if page == 1 else 4
    end = 4 if page == 1 else len(team_members)
    members = team_members[start:end]

    cols = st.columns(len(members))
    for col, member in zip(cols, members):
        with col:
            try:
                with open(member["image"], "rb") as f:
                    data = f.read()
                b64_img = base64.b64encode(data).decode()
                st.markdown(
                    f'<img class="team-img" src="data:image/png;base64,{b64_img}"/>',
                    unsafe_allow_html=True,
                )
            except FileNotFoundError:
                st.warning(f"Không tìm thấy ảnh: {member['image']}")
            st.markdown(
                f"""
                <div style='text-align: center; margin-top: 4px; font-weight: bold;'>
                {member['name']}
                </div>
                """,
                unsafe_allow_html=True
            )

    col1, col2 = st.columns([1, 9])
    with col1:
        if page == 2 and st.button("⬅️", key="prev"):
            st.session_state.team_page = 1
    with col2:
        if page == 1 and st.button("➡️", key="next"):
            st.session_state.team_page = 2

show_team(st.session_state.team_page)
