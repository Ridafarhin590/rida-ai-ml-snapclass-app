import streamlit as st


def style_background_home():
    """
    Home page background is handled directly inside home_screen.py.
    This function is kept for compatibility with existing imports.
    """
    st.markdown(
        """
        <style>
        .stApp {
            background: transparent !important;
            background-color: transparent !important;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }

        [data-testid="stAppViewContainer"] > .main {
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
