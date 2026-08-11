import streamlit as st
from pathlib import Path
import base64

from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout
from src.components.chatbot import chatbot


def get_background_image():

    image_path = (
        Path(__file__).resolve().parents[2]
        / "assets"
        / "ai_background.png"
    )

    if not image_path.exists():
        st.error(
            f"Background image not found:\n{image_path}"
        )
        return None

    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(
            image_file.read()
        ).decode()

    return encoded


def home_screen():

    # ==========================================
    # BACKGROUND IMAGE
    # ==========================================

    encoded_image = get_background_image()

    if encoded_image:

        st.markdown(
            f"""
            <style>

            /* ======================================
               FULL SCREEN HOME BACKGROUND
            ====================================== */

            .stApp {{
                background-image:
                    url("data:image/png;base64,{encoded_image}") !important;

                background-size: cover !important;

                background-position: center center !important;

                background-repeat: no-repeat !important;

                background-attachment: fixed !important;

                min-height: 100vh !important;
            }}


            [data-testid="stAppViewContainer"] {{
                background: transparent !important;
            }}


            [data-testid="stAppViewContainer"] > .main {{
                background: transparent !important;
            }}


            [data-testid="stHeader"] {{
                background: transparent !important;
            }}


            /* Remove white content background */

            .block-container {{
                background: transparent !important;

                max-width: 100% !important;

                padding-top: 0rem !important;

                padding-bottom: 0rem !important;
            }}


            /* Make vertical scrolling background consistent */

            html,
            body {{
                background: transparent !important;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    # ==========================================
    # COMMON STYLE
    # ==========================================

    style_base_layout()


    # ==========================================
    # HOME CONTENT
    # ==========================================

    st.markdown(
        """
        <div style="
            min-height: 100vh;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            padding-top: 40px;
            box-sizing: border-box;
        ">
        """,
        unsafe_allow_html=True
    )


    # ==========================================
    # HEADER / LOGO
    # ==========================================

    header_home()


    # ==========================================
    # MAIN HEADING
    # ==========================================

    st.markdown(
        """
        <div style="
            text-align: center;
            margin-top: 25px;
            width: 100%;
        ">

            <h2 style="
                color: white;
                font-family: 'Outfit', sans-serif;
                font-size: 42px;
                font-weight: 800;
                line-height: 1.15;
                margin: 0;
                text-shadow:
                    0 2px 8px rgba(0,0,0,0.6);
            ">
                AI & Machine Learning<br>
                Based Presence Detection
            </h2>

            <p style="
                color: #FFFFFF;
                font-family: 'Outfit', sans-serif;
                font-size: 19px;
                font-weight: 400;
                margin-top: 18px;
                text-shadow:
                    0 2px 6px rgba(0,0,0,0.7);
            ">
                For Teachers. For Students. For Everyone.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ==========================================
    # BUTTON AREA
    # ==========================================

    st.markdown(
        """
        <div style="
            height: 25px;
        "></div>
        """,
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(
        [1, 2, 1],
        gap="small"
    )


    with col2:

        # ======================================
        # STUDENT
        # ======================================

        if st.button(
            "👨‍🎓  I'm a Student",
            type="primary",
            use_container_width=True,
            key="home_student_button"
        ):

            st.session_state["login_type"] = "student"

            st.rerun()


        st.markdown(
            """
            <div style="height: 18px;"></div>
            """,
            unsafe_allow_html=True
        )


        # ======================================
        # TEACHER
        # ======================================

        if st.button(
            "👨‍🏫  I'm a Teacher",
            type="secondary",
            use_container_width=True,
            key="home_teacher_button"
        ):

            st.session_state["login_type"] = "teacher"

            st.rerun()


    # ==========================================
    # SPACE
    # ==========================================

    st.markdown(
        """
        <div style="
            height: 55px;
        "></div>
        """,
        unsafe_allow_html=True
    )


    # ==========================================
    # AI CHATBOT
    # ==========================================

    chatbot()


    # ==========================================
    # FOOTER
    # ==========================================

    footer_home()


    # ==========================================
    # CLOSE MAIN CONTAINER
    # ==========================================

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
    )
