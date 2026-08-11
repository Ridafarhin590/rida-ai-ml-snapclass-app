import streamlit as st
import base64
from pathlib import Path


def style_background_home():

    # Project root:
    # ai-attendance-project-app/
    project_root = Path(__file__).resolve().parents[2]

    image_path = project_root / "assets" / "ai_background.png"

    # Check image exists
    if not image_path.exists():
        st.error(f"❌ IMAGE NOT FOUND: {image_path}")
        return

    # Read image
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Convert PNG to base64
    encoded = base64.b64encode(image_bytes).decode("utf-8")

    st.markdown(
        f"""
        <style>

        /* =========================================
           REMOVE STREAMLIT BACKGROUND
        ========================================= */

        html,
        body,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main {{
            background: transparent !important;
            background-color: transparent !important;
        }}


        /* =========================================
           FULL SCREEN IMAGE
        ========================================= */

        #snapclass-background {{
            position: fixed !important;

            top: 0 !important;
            left: 0 !important;

            width: 100vw !important;
            height: 100vh !important;

            object-fit: cover !important;
            object-position: center !important;

            z-index: 0 !important;

            pointer-events: none !important;
        }}


        /* =========================================
           KEEP STREAMLIT CONTENT ABOVE IMAGE
        ========================================= */

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
            id="snapclass-background"
            src="data:image/png;base64,{encoded}"
        />
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
