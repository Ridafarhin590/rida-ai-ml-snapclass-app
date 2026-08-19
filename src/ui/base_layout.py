import streamlit as st
from pathlib import Path
import base64


# ============================================================
# HOME PAGE BACKGROUND
# ============================================================

def style_background_home():

    project_root = Path(__file__).resolve().parents[2]

    image_path = project_root / "assets" / "ai_background.png"

    if not image_path.exists():

        st.error(
            f"Background image not found:\n{image_path}"
        )

        return

    image_bytes = image_path.read_bytes()

    image_base64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    st.markdown(
        f"""
        <style>

        /* ====================================================
           FULL HOME PAGE BACKGROUND
           ==================================================== */

        .stApp {{
            background: transparent !important;
            background-color: transparent !important;
        }}

        [data-testid="stAppViewContainer"] {{
            background: transparent !important;
        }}

        [data-testid="stAppViewContainer"] > .main {{
            background: transparent !important;
        }}

        [data-testid="stMain"] {{
            background: transparent !important;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        [data-testid="stToolbar"] {{
            background: transparent !important;
        }}

        .block-container {{
            background: transparent !important;
            position: relative !important;
            z-index: 1 !important;
        }}


        /* ====================================================
           FIXED FULL SCREEN IMAGE
           ==================================================== */

        [data-testid="stAppViewContainer"]::before {{

            content: "";

            position: fixed;

            top: 0;
            left: 0;

            width: 100vw;
            height: 100vh;

            background-image:
                url("data:image/png;base64,{image_base64}");

            background-size: cover;

            background-position: center center;

            background-repeat: no-repeat;

            z-index: -10;

            pointer-events: none;
        }}


        /* ====================================================
           STREAMLIT CONTAINERS TRANSPARENT
           ==================================================== */

        [data-testid="stVerticalBlock"] {{
            background: transparent !important;
        }}

        [data-testid="stHorizontalBlock"] {{
            background: transparent !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD BACKGROUND
# ============================================================

def style_background_dashboard():

    st.markdown(
        """
        <style>

        .stApp {

            background: #E0E3FF !important;

            background-color: #E0E3FF !important;
        }

        [data-testid="stAppViewContainer"] {

            background: #E0E3FF !important;
        }

        [data-testid="stAppViewContainer"] > .main {

            background: #E0E3FF !important;
        }

        [data-testid="stMain"] {

            background: #E0E3FF !important;
        }

        .block-container {

            background: transparent !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BASE LAYOUT
# ============================================================

def style_base_layout():

    st.markdown(
        """
        <style>

        /* ====================================================
           GOOGLE FONTS
           ==================================================== */

        @import url(
            'https://fonts.googleapis.com/css2?family=Climate+Crisis&display=swap'
        );

        @import url(
            'https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap'
        );


        /* ====================================================
           HIDE STREAMLIT DEFAULT UI
           ==================================================== */

        #MainMenu {
            visibility: hidden !important;
        }

        header {
            visibility: hidden !important;
        }

        footer {
            visibility: hidden !important;
        }


        /* ====================================================
           MAIN CONTAINER
           ==================================================== */

        .block-container {

            padding-top: 1.5rem !important;

            padding-bottom: 1rem !important;

            background: transparent !important;

            max-width: 1200px !important;

            margin: 0 auto !important;

            box-sizing: border-box !important;
        }


        /* ====================================================
           FONTS
           ==================================================== */

        h1 {

            font-family:
                'Climate Crisis',
                sans-serif !important;

            font-size: 3.5rem !important;
        }

        h2 {

            font-family:
                'Outfit',
                sans-serif !important;

            font-size: 2rem !important;
        }

        h3,
        h4,
        p,
        button,
        input,
        textarea {

            font-family:
                'Outfit',
                sans-serif !important;
        }


        /* ====================================================
           HOME PAGE BUTTONS
           ==================================================== */

        div.stButton > button {

            border: none !important;

            font-family:
                'Outfit',
                sans-serif !important;

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


        /* ====================================================
           HOME / GENERAL PRIMARY BUTTON
           ==================================================== */

        button[kind="primary"] {

            background:
                linear-gradient(
                    90deg,
                    #D946EF 0%,
                    #A855F7 35%,
                    #6366F1 70%,
                    #3B82F6 100%
                ) !important;

            color: white !important;

            border: none !important;
        }


        /* ====================================================
           HOME / GENERAL SECONDARY BUTTON
           ==================================================== */

        button[kind="secondary"] {

            background:
                linear-gradient(
                    90deg,
                    #D946EF 0%,
                    #A855F7 35%,
                    #6366F1 70%,
                    #3B82F6 100%
                ) !important;

            color: white !important;

            border: none !important;
        }


        /* ====================================================
           TERTIARY
           ==================================================== */

        button[kind="tertiary"] {

            background:
                linear-gradient(
                    90deg,
                    #D946EF 0%,
                    #A855F7 35%,
                    #6366F1 70%,
                    #3B82F6 100%
                ) !important;

            color: white !important;

            border: none !important;
        }


        /* ====================================================
           GENERAL HOVER
           ==================================================== */

        div.stButton > button:hover {

            transform: scale(1.03) !important;

            box-shadow:
                0 6px 20px
                rgba(0, 0, 0, 0.25) !important;
        }


        /* ====================================================
           DASHBOARD CENTER
           ==================================================== */

        .dashboard-center {

            width: 100% !important;

            max-width: 1000px !important;

            margin-left: auto !important;

            margin-right: auto !important;

            box-sizing: border-box !important;
        }


        /* ====================================================
           DASHBOARD HEADINGS
           ==================================================== */

        .dashboard-center h1,
        .dashboard-center h2,
        .dashboard-center h3,
        .dashboard-center h4,
        .dashboard-center p {

            text-align: center !important;
        }


        /* ====================================================
           DASHBOARD TABS
           ==================================================== */

        .dashboard-tabs {

            width: 100% !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            gap: 16px !important;

            margin: 20px auto !important;

            padding: 0 !important;

            box-sizing: border-box !important;
        }


        /* Dashboard tab button container */

        .dashboard-tabs div.stButton {

            width: 150px !important;

            min-width: 150px !important;

            max-width: 150px !important;

            margin: 0 !important;

            padding: 0 !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            box-sizing: border-box !important;
        }


        /* Dashboard tab button */

        .dashboard-tabs div.stButton > button {

            width: 150px !important;

            min-width: 150px !important;

            max-width: 150px !important;

            height: 48px !important;

            min-height: 48px !important;

            max-height: 48px !important;

            margin: 0 !important;

            padding: 0 !important;

            border-radius: 25px !important;

            background:
                linear-gradient(
                    90deg,
                    #D946EF 0%,
                    #A855F7 35%,
                    #6366F1 70%,
                    #3B82F6 100%
                ) !important;

            color: white !important;

            border: none !important;

            font-size: 15px !important;

            font-weight: 600 !important;

            box-sizing: border-box !important;
        }


        /* ====================================================
           DASHBOARD TAB HOVER
           ==================================================== */

        .dashboard-tabs div.stButton > button:hover {

            transform: scale(1.03) !important;

            box-shadow:
                0 6px 20px
                rgba(0, 0, 0, 0.22) !important;
        }


        /* ====================================================
           ENROLL BUTTON
           ==================================================== */

        .enroll-button {

            width: 100% !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            margin: 0 auto !important;

            padding: 0 !important;

            box-sizing: border-box !important;
        }


        .enroll-button div.stButton {

            width: 100% !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            margin: 0 !important;

            padding: 0 !important;
        }


        .enroll-button div.stButton > button {

            width: 460px !important;

            min-width: 460px !important;

            max-width: 460px !important;

            height: 48px !important;

            min-height: 48px !important;

            max-height: 48px !important;

            margin: 0 auto !important;

            padding: 0 !important;

            border-radius: 25px !important;

            background:
                linear-gradient(
                    90deg,
                    #D946EF 0%,
                    #A855F7 35%,
                    #6366F1 70%,
                    #3B82F6 100%
                ) !important;

            color: white !important;

            border: none !important;

            font-size: 15px !important;

            font-weight: 600 !important;

            box-sizing: border-box !important;
        }


        /* ====================================================
           ENROLL HOVER
           ==================================================== */

        .enroll-button div.stButton > button:hover {

            transform: scale(1.03) !important;

            box-shadow:
                0 6px 20px
                rgba(0, 0, 0, 0.22) !important;
        }


        /* ====================================================
           LOGOUT BUTTON
           ==================================================== */

        .logout-button {

            width: 100% !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            margin: 0 auto !important;
        }


        .logout-button div.stButton {

            width: 100% !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            margin: 0 !important;
        }


        .logout-button div.stButton > button {

            width: 460px !important;

            min-width: 460px !important;

            max-width: 460px !important;

            height: 48px !important;

            min-height: 48px !important;

            max-height: 48px !important;

            margin: 0 auto !important;

            padding: 0 !important;

            border-radius: 25px !important;

            background:
                linear-gradient(
                    90deg,
                    #D946EF 0%,
                    #A855F7 35%,
                    #6366F1 70%,
                    #3B82F6 100%
                ) !important;

            color: white !important;

            border: none !important;

            font-size: 15px !important;

            font-weight: 600 !important;
        }


        /* ====================================================
           UNENROLL BUTTON
           ==================================================== */

        .unenroll-button {

            width: 100% !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            margin: 15px auto !important;

            padding: 0 !important;
        }


        .unenroll-button div.stButton {

            width: 100% !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            margin: 0 !important;
        }


        .unenroll-button div.stButton > button {

            width: 460px !important;

            min-width: 460px !important;

            max-width: 460px !important;

            height: 48px !important;

            min-height: 48px !important;

            max-height: 48px !important;

            margin: 0 auto !important;

            padding: 0 !important;

            border-radius: 25px !important;

            background:
                linear-gradient(
                    90deg,
                    #D946EF 0%,
                    #A855F7 35%,
                    #6366F1 70%,
                    #3B82F6 100%
                ) !important;

            color: white !important;

            border: none !important;

            font-size: 15px !important;

            font-weight: 600 !important;
        }


        /* ====================================================
           UNENROLL HOVER
           ==================================================== */

        .unenroll-button div.stButton > button:hover {

            transform: scale(1.03) !important;

            box-shadow:
                0 6px 20px
                rgba(0, 0, 0, 0.22) !important;
        }


        /* ====================================================
           AI ASSISTANT CHAT INPUT
           ==================================================== */

        div[data-testid="stChatInput"] {

            width: 500px !important;

            max-width: 500px !important;

            min-width: 500px !important;

            margin-left: auto !important;

            margin-right: auto !important;

            box-sizing: border-box !important;
        }


        div[data-testid="stChatInput"] textarea {

            width: 100% !important;

            min-height: 48px !important;

            max-height: 48px !important;

            border-radius: 25px !important;

            font-family:
                'Outfit',
                sans-serif !important;

            font-size: 15px !important;

            box-sizing: border-box !important;
        }


        /* ====================================================
           CAMERA SCANNER
           ==================================================== */

        [data-testid="stCameraInput"] {

            width: 500px !important;

            max-width: 90vw !important;

            margin-left: auto !important;

            margin-right: auto !important;

            box-sizing: border-box !important;
        }


        [data-testid="stCameraInput"] video {

            width: 500px !important;

            max-width: 90vw !important;

            height: 375px !important;

            object-fit: cover !important;

            border-radius: 16px !important;
        }


        [data-testid="stCameraInput"] button {

            border-radius: 20px !important;
        }


        /* ====================================================
           MOBILE
           ==================================================== */

        @media (max-width: 600px) {


            /* ================================================
               MAIN CONTAINER
               ================================================ */

            .block-container {

                width: 100% !important;

                max-width: 100% !important;

                padding-left: 12px !important;

                padding-right: 12px !important;

                padding-top: 1rem !important;

                box-sizing: border-box !important;
            }


            /* ================================================
               HOME / GENERAL BUTTON
               ================================================ */

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


            /* ================================================
               CHAT INPUT
               ================================================ */

            div[data-testid="stChatInput"] {

                width: 90% !important;

                max-width: 160px !important;

                min-width: 0 !important;

                margin-left: auto !important;

                margin-right: auto !important;
            }


            div[data-testid="stChatInput"] textarea {

                width: 100% !important;

                min-height: 46px !important;

                max-height: 46px !important;

                font-size: 14px !important;
            }


            /* ================================================
               DASHBOARD CENTER
               ================================================ */

            .dashboard-center {

                width: 94% !important;

                max-width: 94% !important;

                margin-left: auto !important;

                margin-right: auto !important;
            }


            /* ================================================
               DASHBOARD TABS
               ================================================ */

            .dashboard-tabs {

                width: 100% !important;

                gap: 8px !important;

                justify-content: center !important;

                margin: 20px auto !important;
            }


            .dashboard-tabs div.stButton {

                width: 105px !important;

                min-width: 105px !important;

                max-width: 105px !important;
            }


            .dashboard-tabs div.stButton > button {

                width: 105px !important;

                min-width: 360px !important;

                max-width: 360px !important;

                height: 42px !important;

                min-height: 42px !important;

                max-height: 42px !important;

                border-radius: 22px !important;

                font-size: 13px !important;
            }


            /* ================================================
               ENROLL
               ================================================ */

            .enroll-button div.stButton > button {

                width: 90% !important;

                min-width: 0 !important;

                max-width: 360px !important;

                height: 44px !important;

                min-height: 44px !important;

                max-height: 44px !important;

                border-radius: 23px !important;

                font-size: 14px !important;
            }


            /* ================================================
               LOGOUT
               ================================================ */

            .logout-button div.stButton > button {

                width: 90% !important;

                min-width: 360px !important;

                max-width: 360px !important;

                height: 44px !important;

                min-height: 44px !important;

                max-height: 44px !important;

                border-radius: 23px !important;

                font-size: 14px !important;
            }


            /* ================================================
               UNENROLL
               ================================================ */

            .unenroll-button div.stButton > button {

                width: 90% !important;

                min-width: 0 !important;

                max-width: 360px !important;

                height: 44px !important;

                min-height: 44px !important;

                max-height: 44px !important;

                border-radius: 23px !important;

                font-size: 14px !important;
            }


            /* ================================================
               CAMERA
               ================================================ */

            [data-testid="stCameraInput"] {

                width: 90% !important;

                max-width: 320px !important;

                margin-left: auto !important;

                margin-right: auto !important;
            }


            [data-testid="stCameraInput"] video {

                width: 100% !important;

                max-width: 320px !important;

                height: 240px !important;

                object-fit: cover !important;

                border-radius: 14px !important;
            }


            /* ================================================
               CAMERA BUTTON
               ================================================ */

            [data-testid="stCameraInput"] button {

                min-height: 42px !important;

                border-radius: 20px !important;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# OPTIONAL CAMERA STYLE FUNCTION
# ============================================================

def style_camera():

    st.markdown(
        """
        <style>

        /* ====================================================
           CAMERA DIALOG - LARGE DESKTOP CONTAINER
           ==================================================== */

        [data-testid="stDialog"] {

            width: 900px !important;

            max-width: 95vw !important;

            min-width: 700px !important;
        }


        /* Streamlit dialog inner wrapper */

        [data-testid="stDialog"] > div {

            width: 100% !important;

            max-width: 100% !important;
        }


        /* ====================================================
           DIALOG CONTENT
           ==================================================== */

        [data-testid="stDialog"] .block-container {

            width: 100% !important;

            max-width: 100% !important;

            padding-left: 1.5rem !important;

            padding-right: 1.5rem !important;

            padding-top: 1rem !important;

            padding-bottom: 1rem !important;

            box-sizing: border-box !important;
        }


        /* ====================================================
           DIALOG VERTICAL BLOCKS
           ==================================================== */

        [data-testid="stDialog"] [data-testid="stVerticalBlock"] {

            width: 100% !important;

            max-width: 100% !important;

            box-sizing: border-box !important;
        }


        /* ====================================================
           CAMERA CONTAINER INSIDE DIALOG
           ==================================================== */

        [data-testid="stDialog"] [data-testid="stCameraInput"] {

            width: 100% !important;

            max-width: 100% !important;

            min-width: 0 !important;

            margin-left: auto !important;

            margin-right: auto !important;

            box-sizing: border-box !important;
        }


        /* ====================================================
           CAMERA PREVIEW
           ==================================================== */

        [data-testid="stDialog"] [data-testid="stCameraInput"] video {

            width: 100% !important;

            max-width: 100% !important;

            height: 500px !important;

            min-height: 500px !important;

            object-fit: cover !important;

            border-radius: 16px !important;

            display: block !important;

            box-sizing: border-box !important;
        }


        /* ====================================================
           CAMERA TAKE PHOTO BUTTON
           ==================================================== */

        [data-testid="stDialog"] [data-testid="stCameraInput"] button {

            width: 100% !important;

            max-width: 100vw !important;

            min-height: 48px !important;

            border-radius: 60pxpx !important;

            font-family: 'Outfit', sans-serif !important;

            font-size: 16px !important;

            font-weight: 600 !important;

            box-sizing: border-box !important;
        }


        /* ====================================================
           DIALOG BUTTONS
           CAMERA / UPLOAD / DONE
           ==================================================== */

        [data-testid="stDialog"] div.stButton {

            width: 100% !important;

            display: flex !important;

            justify-content: center !important;

            align-items: center !important;

            box-sizing: border-box !important;
        }


        [data-testid="stDialog"] div.stButton > button {

            width: 100% !important;

            max-width: 100% !important;

            min-height: 48px !important;

            border-radius: 25px !important;

            font-family: 'Outfit', sans-serif !important;

            font-size: 16px !important;

            font-weight: 600 !important;

            box-sizing: border-box !important;
        }


        /* ====================================================
           UPLOAD PHOTOS
           ==================================================== */

        [data-testid="stDialog"] [data-testid="stFileUploader"] {

            width: 100% !important;

            max-width: 100% !important;
            padding-left: 20px !important;
            padding-right: 20px !important;
            box-sizing: border-box !important;
        }


        /* ====================================================
           MOBILE CAMERA DIALOG
           ==================================================== */

        @media (max-width: 700px) {

            [data-testid="stDialog"] {

                width: 95vw !important;

                max-width: 95vw !important;

                min-width: 0 !important;

                box-sizing: border-box !important;
            }


            [data-testid="stDialog"] > div {

                width: 100% !important;

                max-width: 100% !important;
            }


            [data-testid="stDialog"] .block-container {

                width: 100% !important;

                max-width: 100% !important;

                padding-left: 12px !important;

                padding-right: 12px !important;

                padding-top: 10px !important;

                padding-bottom: 10px !important;

                box-sizing: border-box !important;
            }


            [data-testid="stDialog"] [data-testid="stCameraInput"] {

                width: 100% !important;

                max-width: 100% !important;

                min-width: 0 !important;

                margin: 0 auto !important;
            }


            [data-testid="stDialog"] [data-testid="stCameraInput"] video {

                width: 100% !important;

                max-width: 100% !important;

                height: 360px !important;

                min-height: 360px !important;

                object-fit: cover !important;

                border-radius: 14px !important;
            }


            [data-testid="stDialog"] div.stButton {

                width: 100% !important;

                max-width: 100% !important;

            }


            [data-testid="stDialog"] div.stButton > button {

                width: 100% !important;

                max-width: 100% !important;

                min-height: 48px !important;

                font-size: 15px !important;

                border-radius: 25px !important;
            }

        }


        /* ====================================================
           SMALL MOBILE
           ==================================================== */

        @media (max-width: 450px) {

            [data-testid="stDialog"] {

                width: 96vw !important;

                max-width: 96vw !important;

                min-width: 0 !important;
            }


            [data-testid="stDialog"] [data-testid="stCameraInput"] video {

                height: 300px !important;

                min-height: 300px !important;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )