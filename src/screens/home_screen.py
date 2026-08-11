import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.components.chatbot import chatbot

def home_screen():

    style_background_home()
    style_base_layout()

    header_home()

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