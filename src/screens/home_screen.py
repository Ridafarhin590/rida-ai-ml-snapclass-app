import streamlit as st

from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import (
    style_base_layout,
    style_background_home
)
from src.components.chatbot import chatbot


def home_screen():

    # ==========================================
    # PAGE STYLING
    # ==========================================

    style_background_home()
    style_base_layout()

    # ==========================================
    # HEADER
    # ==========================================

    header_home()

    # ==========================================
    # MAIN TITLE
    # ==========================================

    st.html(
        """
        <div style="
            width: 100%;
            text-align: center;
            margin-top: 10px;
            background: transparent;
        ">

            <h2 style="
                color: white;
                font-family: 'Outfit', sans-serif;
                font-size: 42px;
                font-weight: 700;
                line-height: 1.2;
                margin: 0;
                padding: 0;
                background: transparent;
                text-shadow: 0px 2px 8px rgba(0,0,0,0.7);
            ">
                AI & Machine Learning<br>
                Based Presence Detection
            </h2>

            <p style="
                color: #D6D6D6;
                font-family: 'Outfit', sans-serif;
                font-size: 18px;
                font-weight: 400;
                margin-top: 12px;
                margin-bottom: 0;
                background: transparent;
                text-shadow: 0px 2px 8px rgba(0,0,0,0.7);
            ">
                For Teachers. For Students. For Everyone.
            </p>

        </div>
        """
    )

    # ==========================================
    # HOME BUTTON CSS ONLY
    # ==========================================

    st.html(
        """
        <style>

        /* =========================================
           HOME PORTAL BUTTON CONTAINER
           ========================================= */

        .st-key-home_portal_buttons {

            width: 100% !important;

            max-width: 100% !important;

            margin-left: auto !important;
            margin-right: auto !important;

            padding: 0 !important;

            display: flex !important;

            flex-direction: column !important;

            align-items: center !important;

            justify-content: center !important;

            box-sizing: border-box !important;
        }


        /* =========================================
           STREAMLIT BUTTON BLOCK
           ========================================= */

        .st-key-home_portal_buttons
        div.stButton {

            width: 100% !important;

            max-width: 100% !important;

            margin-left: auto !important;
            margin-right: auto !important;

            padding: 0 !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            box-sizing: border-box !important;
        }


        /* =========================================
           STUDENT / TEACHER BUTTON
           ========================================= */

        .st-key-home_portal_buttons
        div.stButton > button {

            width: 500px !important;

            min-width: 500px !important;

            max-width: 500px !important;

            height: 52px !important;

            min-height: 52px !important;

            max-height: 52px !important;

            margin-left: auto !important;

            margin-right: auto !important;

            padding: 0 !important;

            border: none !important;

            border-radius: 28px !important;

            background:
                linear-gradient(
                    90deg,
                    #D946EF 0%,
                    #A855F7 35%,
                    #6366F1 70%,
                    #3B82F6 100%
                ) !important;

            color: white !important;

            font-family:
                'Outfit',
                sans-serif !important;

            font-size: 16px !important;

            font-weight: 600 !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            text-align: center !important;

            box-sizing: border-box !important;

            transition:
                transform 0.2s ease-in-out,
                box-shadow 0.2s ease-in-out !important;
        }


        /* =========================================
           HOVER
           ========================================= */

        .st-key-home_portal_buttons
        div.stButton > button:hover {

            transform: scale(1.03) !important;

            box-shadow:
                0 6px 20px
                rgba(0, 0, 0, 0.25) !important;
        }


        /* =========================================
           MOBILE
           ========================================= */

        @media (max-width: 600px) {

            .st-key-home_portal_buttons {

                width: 100% !important;

                max-width: 100% !important;

                padding-left: 0 !important;

                padding-right: 0 !important;

                margin-left: auto !important;

                margin-right: auto !important;
            }


            .st-key-home_portal_buttons
            div.stButton {

                width: 100% !important;

                max-width: 100% !important;

                margin-left: auto !important;

                margin-right: auto !important;
            }


            .st-key-home_portal_buttons
            div.stButton > button {

                width: 90% !important;

                min-width: 0 !important;

                max-width: 360px !important;

                height: 48px !important;

                min-height: 48px !important;

                max-height: 48px !important;

                margin-left: auto !important;

                margin-right: auto !important;

                border-radius: 25px !important;

                font-size: 15px !important;
            }

        }

        </style>
        """
    )

    # ==========================================
    # HOME PORTAL BUTTONS
    # ==========================================

    with st.container(key="home_portal_buttons"):

        # ======================================
        # STUDENT PORTAL
        # ======================================

        if st.button(
            "Student Portal",
            type="primary",
            key="home_student_button"
        ):

            st.session_state["login_type"] = "student"

            st.rerun()


        # ======================================
        # SPACE
        # ======================================

        st.write("")


        # ======================================
        # TEACHER PORTAL
        # ======================================

        if st.button(
            "Teacher Portal",
            type="secondary",
            key="home_teacher_button"
        ):

            st.session_state["login_type"] = "teacher"

            st.rerun()


    # ==========================================
    # CHATBOT
    # ==========================================

    st.write("")
    st.write("")

    chatbot()

    # ==========================================
    # FOOTER
    # ==========================================

    footer_home()