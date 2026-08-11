import streamlit as st
import base64
from pathlib import Path

from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout
from src.components.chatbot import chatbot


def home_screen():

    # =========================================================
    # LOAD LOCAL BACKGROUND IMAGE
    # =========================================================

    project_root = Path(__file__).resolve().parents[2]

    image_path = project_root / "assets" / "ai_background.png"

    if not image_path.exists():
        st.error(f"❌ Background image not found: {image_path}")
        return

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # =========================================================
    # FULL SCREEN BACKGROUND
    # =========================================================

    st.markdown(
        f"""
        <style>

        html,
        body,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main {{
            background: transparent !important;
            background-color: transparent !important;
        }}

        /* Full-screen background image */
        #snapclass-home-background {{
            position: fixed !important;

            top: 0 !important;
            left: 0 !important;

            width: 100vw !important;
            height: 100vh !important;

            object-fit: cover !important;
            object-position: center center !important;

            z-index: 0 !important;

            pointer-events: none !important;
        }}

        /* Streamlit content above background */
        [data-testid="stAppViewContainer"] {{
            position: relative !important;
            z-index: 1 !important;
        }}

        [data-testid="stAppViewContainer"] > .main {{
            position: relative !important;
            z-index: 2 !important;
            background: transparent !important;
        }}

        .block-container {{
            position: relative !important;
            z-index: 3 !important;
            background: transparent !important;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        </style>

        <img
            id="snapclass-home-background"
            src="data:image/png;base64,{image_base64}"
        />
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    <div style="text-align:center; margin-top:8px;">

    <h2 style="
    color:white;
    font-family:Outfit;
    font-size:42px;
    font-weight:700;
    line-height:1.3;
    ">
    AI & Machine Learning<br>
    Based Presence Detection
    </h2>

    <p style="
    color:#D6D6D6;
    font-size:18px;
    ">
    For Teachers. For Students. For Everyone.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "👨‍🎓 I'm a Student",
            type="primary",
            use_container_width=True
        ):
            st.session_state["login_type"] = "student"
            st.rerun()
    
        st.write("")

        if st.button(
            "👨‍🏫 I'm a Teacher",
            type="secondary",
            use_container_width=True
        ):
            st.session_state["login_type"] = "teacher"
            st.rerun()

    st.write("")

    chatbot()

    footer_home()
