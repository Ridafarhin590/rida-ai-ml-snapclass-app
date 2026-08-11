import streamlit as st

def chatbot():

    st.markdown("""
    <style>

    .ai-panel {
        position: fixed;
        top: 50%;
        right: 30px;
        transform: translateY(-50%);
        width: 380px;
        z-index: 999;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ai-panel">', unsafe_allow_html=True)

    if "show_ai" not in st.session_state:
        st.session_state["show_ai"] = False

    if st.button(
        "🤖 SnapClass AI Assistant",
        key="ai_btn",
        use_container_width=True
    ):
        st.session_state["show_ai"] = not st.session_state["show_ai"]

    if st.session_state["show_ai"]:

        with st.container(border=True):

            st.markdown("### 🤖 SnapClass AI Assistant")

            question = st.text_input(
                "Ask anything about SnapClass...",
                key="chat_question"
            )

            if question:
                q = question.lower()

                if "face" in q:
                    st.success("Face Recognition uses Dlib and SVM Classification.")

                elif "voice" in q:
                    st.success("Voice Recognition uses Resemblyzer and Librosa.")

                elif "attendance" in q:
                    st.success("Attendance can be marked using Face and Voice Recognition.")

                elif "teacher" in q:
                    st.success("Teachers can create subjects, QR codes and reports.")

                elif "student" in q:
                    st.success("Students can enroll, register face/voice and view attendance.")

                elif "technology" in q:
                    st.success("Python, Streamlit, Supabase, Dlib, Resemblyzer and Scikit-Learn.")
                
                else:
                    st.info("Ask about Face, Voice, Attendance, Teacher Module, Student Module or Technology.")
                
    st.markdown("</div>", unsafe_allow_html=True)