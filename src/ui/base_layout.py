import streamlit as st
from pathlib import Path
import base64


# ============================================================
# HOME PAGE BACKGROUND
# ============================================================

def style_background_home():

    # --------------------------------------------------------
    # Find project root
    #
    # base_layout.py:
    # project/src/ui/base_layout.py
    #
    # parents[0] -> ui
    # parents[1] -> src
    # parents[2] -> project root
    # --------------------------------------------------------

    project_root = Path(__file__).resolve().parents[2]

    image_path = rida-ai-ml-snapclass-app / "assets" / "ai_background.png"

    # --------------------------------------------------------
    # Check image
    # --------------------------------------------------------

    if not image_path.exists():
        st.error(
            f"Background image not found.\n\n"
            f"Expected location:\n{image_path}"
        )
        return

    # --------------------------------------------------------
    # Convert PNG to Base64
    # --------------------------------------------------------

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # --------------------------------------------------------
    # Apply background DIRECTLY to Streamlit application
    # --------------------------------------------------------

    st.markdown(
        f"""
        <style>

        /* ====================================================
           ENTIRE STREAMLIT APPLICATION
        ==================================================== */

        .stApp {{
            min-height: 100vh !important;

            background-image:
                url("data:image/png;base64,{image_base64}") !important;

            background-size: cover !important;

            background-position: center center !important;

            background-repeat: no-repeat !important;

            background-attachment: fixed !important;

            background-color: transparent !important;
        }}


        /* ====================================================
           STREAMLIT APP VIEW
        ==================================================== */

        [data-testid="stAppViewContainer"] {{
            min-height: 100vh !important;

            background: transparent !important;

            background-color: transparent !important;
        }}


        /* ====================================================
           MAIN AREA
        ==================================================== */

        [data-testid="stAppViewContainer"] > .main {{
            background: transparent !important;

            background-color: transparent !important;

            min-height: 100vh !important;
        }}


        /* ====================================================
           MAIN CONTENT
        ==================================================== */

        [data-testid="stMain"] {{
            background: transparent !important;

            background-color: transparent !important;
        }}


        /* ====================================================
           BLOCK CONTAINER
        ==================================================== */

        .block-container {{
            background: transparent !important;

            background-color: transparent !important;
        }}


        /* ====================================================
           HEADER
        ==================================================== */

        [data-testid="stHeader"] {{
            background: transparent !important;

            background-color: transparent !important;
        }}


        /* ====================================================
           SIDEBAR
        ==================================================== */

        [data-testid="stSidebar"] {{
            background: transparent !important;
        }}


        /* ====================================================
           HIDE STREAMLIT DEFAULT HEADER
        ==================================================== */

        #MainMenu,
        footer,
        header {{
            visibility: hidden !important;
        }}


        /* ====================================================
           REMOVE POSSIBLE WHITE OVERLAY
        ==================================================== */

        [data-testid="stVerticalBlock"],
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
            background-image: none !important;
            background: #E0E3FF !important;
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

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# COMMON BASE LAYOUT
# ============================================================

def style_base_layout():

    st.markdown(
        """
        <style>

        @import url(
            'https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap'
        );

        @import url(
            'https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap'
        );


        /* ----------------------------------------------------
           HIDE STREAMLIT DEFAULT UI
        ---------------------------------------------------- */

        #MainMenu,
        footer,
        header {
            visibility: hidden !important;
        }


        /* ----------------------------------------------------
           MAIN CONTAINER
        ---------------------------------------------------- */

        .block-container {
            padding-top: 1.5rem !important;
            background: transparent !important;
        }


        /* ----------------------------------------------------
           HEADINGS
        ---------------------------------------------------- */

        h1 {
            font-family:
                'Climate Crisis',
                sans-serif !important;

            font-size: 3.5rem !important;
        }


        h2 {
            font-family:
                'Climate Crisis',
                sans-serif !important;

            font-size: 2rem !important;
        }


        h3,
        h4,
        p {
            font-family:
                'Outfit',
                sans-serif !important;
        }


        /* ----------------------------------------------------
           BUTTONS
        ---------------------------------------------------- */

        button {
            border-radius: 1.5rem !important;

            border: none !important;

            transition:
                transform 0.25s ease-in-out !important;
        }


        button[kind="primary"] {
            background:
                linear-gradient(
                    90deg,
                    #D946EF,
                    #3B82F6
                ) !important;

            color: white !important;
        }


        button[kind="secondary"] {
            background:
                linear-gradient(
                    90deg,
                    #D946EF,
                    #3B82F6
                ) !important;

            color: white !important;
        }


        button[kind="tertiary"] {
            background: black !important;

            color: white !important;
        }


        button:hover {
            transform: scale(1.05) !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
