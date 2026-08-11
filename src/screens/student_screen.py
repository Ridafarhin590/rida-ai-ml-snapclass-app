import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px
import time

# Internal UI imports
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card

# Dialog imports
from src.components.dialog_enroll import enroll_dialog

# ML Pipeline imports
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding

# Database imports
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject
)
from src.database.config import supabase


# ===================== STUDENT DASHBOARD =====================
def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2 = st.columns(2)
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome Dear Student {student_data['name']}")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    st.divider()
    
    # ---------- TABS ----------
    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        if st.button("Your Subjects", use_container_width=True):
            st.session_state.student_tab = "subjects"
            st.rerun()

    with tab2:
        if st.button("Notice For You", use_container_width=True):
            st.session_state.student_tab = "notices"
            st.rerun()

    with tab3:
        if st.button("Notes For You", use_container_width=True):
            st.session_state.student_tab = "notes"
            st.rerun()

    if "student_tab" not in st.session_state:
        st.session_state.student_tab = "subjects"

    st.divider()

    # ================= SUBJECTS =================
    if st.session_state.student_tab == "subjects":

        c1, c2 = st.columns(2)
        with c1:
            st.header("Your Enrolled Subjects")
        with c2:
            if st.button("Enroll Your Subjects", type="primary"):
                enroll_dialog()

        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

        # 💡 FIX: Initialise stats_map for safe dictionary lookup calculation
        stats_map = {}
        for sub_node in subjects:
            sid = sub_node['subjects']['subject_id']
            stats_map[sid] = {"total": 0, "attended": 0}

        for log in logs:
            sid = log['subject_id']
            if sid in stats_map:
                stats_map[sid]['total'] += 1
                if log.get('is_present'):
                    stats_map[sid]['attended'] += 1

        graph_data = []

        for sub_node in subjects:
            sub = sub_node['subjects']
            sid = sub['subject_id']

            stats = stats_map.get(sid, {"total": 0, "attended": 0})
            attendance_percent = 0

            if stats["total"] > 0:
                attendance_percent = round(
                    (stats["attended"] / stats["total"]) * 100, 1
                )

            graph_data.append({
                "Subject": sub["subject_code"],
                "Attendance": attendance_percent
            })

        if graph_data:
            st.subheader("📊 Attendance Analytics")
            df = pd.DataFrame(graph_data)
            fig = px.bar(
                df,
                x="Subject",
                y="Attendance",
                text="Attendance",
                title="Subject Wise Attendance (%)"
            )
            st.plotly_chart(fig, use_container_width=True)

        cols = st.columns(2)

        for i, sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub['subject_id']

            stats = stats_map.get(sid, {"total": 0, "attended": 0})

            # 💡 FIX: Properly scoped variable wrapper closure factory for nested callbacks
            def make_unenroll_callback(current_sid=sid):
                def unenroll():
                    if st.button("Unenroll from course", key=f"u_{current_sid}", type="secondary"):
                        unenroll_student_to_subject(student_id, current_sid)
                        st.rerun()
                return unenroll

            with cols[i % 2]:
                subject_card(
                    name=sub['name'],
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=[
                        ("📅", "Total", stats['total']),
                        ("✅", "Attended", stats['attended'])
                    ],
                    footer_callback=make_unenroll_callback()
                )

    # ================= NOTICES =================
    # 💡 FIX: Rectified Indentation Error (was unindented back to base root margin level)
    elif st.session_state.student_tab == "notices":
        st.header("📢 Notice")

        try:
            notices = (
                supabase.table("notices")
                .select("*")
                .order("created_at", desc=True)
                .execute()
                .data
            )
        except Exception:
            notices = []

        if not notices:
            st.info("No notices posted yet.")
        else:
            for n in notices:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#0E1117;
                        padding:18px;
                        border-radius:14px;
                        margin-bottom:15px;
                        border:1px solid #262730;
                        box-shadow:0 4px 10px rgba(0,0,0,0.4);
                    ">
                        <h4 style="color:white; margin-bottom:6px;">
                            📢 {n.get('title', 'No Title')}
                        </h4>
                        <p style="color:#cfcfcf; margin-bottom:10px;">
                            {n.get('content', '')}
                        </p>
                        <small style="color:#888;">
                            {n.get('created_at', '')}
                        </small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ================= NOTES =================
    elif st.session_state.student_tab == "notes":
        st.header("📝 Notes")
        
        # Fallback dictionary method logic assuming table reads match system design patterns
        try:
            notes_res = supabase.table("notes").select("*").eq("student_id", student_id).execute().data
        except Exception:
            notes_res = []

        if not notes_res:
            st.info("No educational notes found shared to your profile.")
        else:
            for n in notes_res:
                st.write("📌", n.get("content", ""))

    footer_dashboard()


# ===================== STUDENT SCREEN =====================
def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    header_dashboard()
    st.header("Login using Face")

    photo = st.camera_input("Capture Face")

    if photo:
        img = np.array(Image.open(photo))
        detected, _, faces = predict_attendance(img)

        if faces == 1 and detected:
            sid = list(detected.keys())[0]
            students = get_all_students()

            student = next((s for s in students if s['student_id'] == sid), None)

            if student:
                st.session_state.student_data = student
                st.rerun()
        else:
            st.warning("Face profile unrecognized. Complete manual registration profile record underneath:")

            name = st.text_input("Name")
            audio = st.audio_input("Voice (optional)")

            if st.button("Register Profile"):
                enc = get_face_embeddings(img)

                if not enc:
                    st.error("Face bounding error. Reposition camera view alignment.")
                    return

                voice = None
                if audio:
                    voice = get_voice_embedding(audio.read())

                data = create_student(
                    name,
                    face_embedding=enc[0].tolist(),
                    voice_embedding=voice
                )

                if data:
                    train_classifier()
                    st.session_state.student_data = data[0]
                    st.rerun()


# ===================== MESSAGING & PERMISSIONS =====================
def is_student_allowing_messages(student_id):
    res = supabase.table("students").select("allow_messages").eq("student_id", student_id).execute()
    return res.data and res.data[0]["allow_messages"]


def send_student_message(sender_id, receiver_id, message):
    if not is_student_allowing_messages(receiver_id):
        return {"error": "User disabled messages"}

    return supabase.table("messages").insert({
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "message": message
    }).execute().data


def get_student_messages(student_id):
    return supabase.table("messages").select("*").eq("receiver_id", student_id).execute().data


def update_message_permission(student_id, allow):
    # 💡 FIX: Restructured the broken truncated cutoff line securely
    return supabase.table("students").update({"allow_messages": allow}).eq("student_id", student_id).execute().data