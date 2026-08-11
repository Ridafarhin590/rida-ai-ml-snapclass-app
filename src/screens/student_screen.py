import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np

from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding

from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject
)

import time

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
from src.database.config import supabase


# ===================== STUDENT DASHBOARD =====================
def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2 = st.columns(2)
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']}")
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    st.divider()

    # ---------- TABS ----------
    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        if st.button("Subjects"):
            st.session_state.student_tab = "subjects"

    with tab2:
        if st.button("Notices"):
            st.session_state.student_tab = "notices"

    with tab3:
        if st.button("Notes"):
            st.session_state.student_tab = "notes"

    if "student_tab" not in st.session_state:
        st.session_state.student_tab = "subjects"

    st.divider()

    # ================= SUBJECTS =================
    if st.session_state.student_tab == "subjects":

        c1, c2 = st.columns(2)
        with c1:
            st.header("Your Enrolled Subjects")
        with c2:
            if st.button("Enroll Your Subjects"):
                enroll_dialog()

        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

        stats_map = {}

        for log in logs:
            sid = log['subject_id']
            if sid not in stats_map:
                stats_map[sid] = {"total": 0, "attended": 0}

            stats_map[sid]['total'] += 1
            if log.get('is_present'):
                stats_map[sid]['attended'] += 1

        cols = st.columns(2)

        for i, sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub['subject_id']

            stats = stats_map.get(sid, {"total": 0, "attended": 0})

            def unenroll():
                if st.button("Unenroll From Enrolled Subjects", key=f"u_{sid}"):
                    unenroll_student_to_subject(student_id, sid)
                    st.rerun()

            with cols[i % 2]:
                subject_card(
                    name=sub['name'],
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=[
                        ("📅", "Total", stats['total']),
                        ("✅", "Attended", stats['attended'])
                    ],
                    footer_callback=unenroll
                )

    # ================= NOTICES =================
    elif st.session_state.student_tab == "notices":
        st.header("📢 Notice For You")

        notices = supabase.table("notices").select("*").order("created_at", desc=True).execute().data

        if not notices:
            st.info("No notices yet")
        else:
            for n in notices:st.markdown(f"""
    <div style="
        background-color:#0E1117;
        padding:18px;
        border-radius:14px;
        margin-bottom:15px;
        border:1px solid #262730;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    ">
        <h4 style="color:white; margin-bottom:6px;">📢 {n['title']}</h4>
        <p style="color:#cfcfcf; margin-bottom:10px;">{n['content']}</p>
        <small style="color:#888;">{n['created_at']}</small>
    </div>
    """, unsafe_allow_html=True)

    # ================= NOTES =================
    elif st.session_state.student_tab == "notes":
        st.header("📝 Notes For You")

        notes = get_notes_for_student(student_id)

        if not notes:
            st.info("No notes available")
        else:
            for n in notes:
                st.write("📌", n["content"])

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
            st.warning("Not recognized. Register below")

            name = st.text_input("Name")

            audio = st.audio_input("Voice (optional)")

            if st.button("Register"):
                enc = get_face_embeddings(img)

                if not enc:
                    st.error("Face error")
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


# ===================== MESSAGING =====================
def is_student_allowing_messages(student_id):
    res = supabase.table("students").select("allow_messages").eq("id", student_id).execute()
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
    return supabase.table("students").update({
        "allow_messages": allow
    }).eq("id", student_id).execute().data


# ===================== NOTES =====================
def get_notes_for_student(student_id):
    res = supabase.table("notes").select("*").execute()

    return [
        n for n in res.data
        if n["receiver_id"] == student_id or n["receiver_id"] is None
    ]