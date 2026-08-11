import streamlit as st


def style_background_home():

    st.markdown(
        """
        <style>

        .stApp {
            background-image: url(
                "https://raw.githubusercontent.com/Ridafarhin590/rida-ai-ml-snapclass-app/main/assets/ai_background.png"
            ) !important;

            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;

            min-height: 100vh !important;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }

        [data-testid="stAppViewContainer"] > .main {
            background: transparent !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        [data-testid="stDecoration"] {
            background: transparent !important;
        }

        .block-container {
            background: transparent !important;
        }

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
