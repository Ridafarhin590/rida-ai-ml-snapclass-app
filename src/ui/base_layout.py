import streamlit as st
import base64
from pathlib import Path


def style_background_home():

    # Project root
    project_root = Path(__file__).resolve().parents[2]

    # Image location
    image_path = project_root / "assets" / "ai_background.png"

    # Check image exists
    if not image_path.exists():
        st.error(
            f"Background image not found:\n{image_path}"
        )
        return

    # Read image
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Convert image to base64
    encoded_image = base64.b64encode(
        image_data
    ).decode("utf-8")

    # Full page background
    st.markdown(
        f"""
        <style>

        /* =========================================
           MAIN STREAMLIT APP
        ========================================= */

        .stApp {{
            background-image:
                url("data:image/png;base64,{encoded_image}") !important;

            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;

            min-height: 100vh !important;
        }}


        /* =========================================
           STREAMLIT APP CONTAINER
        ========================================= */

        [data-testid="stAppViewContainer"] {{
            background: transparent !important;
        }}


        /* =========================================
           MAIN CONTENT
        ========================================= */

        [data-testid="stAppViewContainer"] > .main {{
            background: transparent !important;
        }}


        /* =========================================
           HEADER
        ========================================= */

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}


        /* =========================================
           DECORATIVE TOP CONTAINER
        ========================================= */

        [data-testid="stDecoration"] {{
            background: transparent !important;
        }}


        /* =========================================
           MAIN BLOCK
        ========================================= */

        .block-container {{
            background: transparent !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

def style_background_dashboard():

    st.markdown("""
    <style>

    .stApp{
        background: #E0E3FF !important;
    }

    </style>
    """, unsafe_allow_html=True)


def style_base_layout():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1.5rem !important;
    }

    h1 {
        font-family: 'Climate Crisis', sans-serif !important;
        font-size: 3.5rem !important;
    }

    h2 {
        font-family: 'Climate Crisis', sans-serif !important;
        font-size: 2rem !important;
    }

    h3, h4, p {
        font-family: 'Outfit', sans-serif !important;
    }

    button {
        border-radius: 1.5rem !important;
        border: none !important;
        transition: transform 0.25s ease-in-out !important;
    }

    button[kind="primary"] {
        background: linear-gradient(90deg,#D946EF,#3B82F6) !important;
        color: white !important;
    }

    button[kind="secondary"] {
        background: linear-gradient(90deg,#D946EF,#3B82F6)  !important;
        color: white !important;
    }

    button[kind="tertiary"] {
        background: black !important;
        color: white !important;
    }

    button:hover {
        transform: scale(1.05);
    }

    </style>
    """, unsafe_allow_html=True)
