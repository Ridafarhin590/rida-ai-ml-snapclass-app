import streamlit as st
import base64
from pathlib import Path


def style_background_home():

    # Find project root
    project_root = Path(__file__).resolve().parents[2]

    # Exact location:
    # ai-attendance-project-app/assets/ai_background.png
    image_path = project_root / "assets" / "ai_background.png"

    # Check file exists
    if not image_path.exists():
        st.error(f"❌ Background image not found: {image_path}")
        return

    # Read image
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Convert image to base64
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    st.markdown(
        f"""
        <style>

        /* =====================================================
           FULL SCREEN BACKGROUND
        ===================================================== */

        html,
        body,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main,
        .stApp {{
            background: transparent !important;
            background-color: transparent !important;
        }}


        /* =====================================================
           BACKGROUND IMAGE
        ===================================================== */

        .snapclass-background {{
            position: fixed;

            top: 0;
            left: 0;

            width: 100vw;
            height: 100vh;

            background-image: url(
                "data:image/png;base64,{encoded_image}"
            );

            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;

            z-index: 0;

            pointer-events: none;
        }}


        /* =====================================================
           STREAMLIT CONTENT ABOVE IMAGE
        ===================================================== */

        [data-testid="stAppViewContainer"] {{
            position: relative;
            z-index: 1;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        [data-testid="stDecoration"] {{
            background: transparent !important;
        }}

        .main {{
            background: transparent !important;
        }}

        .block-container {{
            position: relative;
            z-index: 2;
            background: transparent !important;
        }}


        /* =====================================================
           MAKE ALL MAIN CONTENT TRANSPARENT
        ===================================================== */

        [data-testid="stVerticalBlock"] {{
            background: transparent !important;
        }}

        </style>

        <div class="snapclass-background"></div>
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
