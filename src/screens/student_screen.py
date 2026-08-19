import streamlit as st

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

from PIL import Image
import numpy as np

from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier
)

from src.pipelines.voice_pipeline import (
    get_voice_embedding
)

from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject
)

from src.components.dialog_enroll import (
    enroll_dialog
)

from src.components.subject_card import (
    subject_card
)

from src.database.config import (
    supabase
)


# ============================================================
# STUDENT DASHBOARD
# ============================================================

def student_dashboard():

    student_data = st.session_state.get(
        "student_data"
    )

    if not student_data:

        st.session_state.pop(
            "student_data",
            None
        )

        st.rerun()

        return

    student_id = student_data.get(
        "student_id"
    )

    if student_id is None:

        st.error(
            "Student information is missing."
        )

        return

    # ========================================================
    # HEADER
    # ========================================================

    c1, c2 = st.columns(
        2,
        vertical_alignment="center"
    )

    with c1:

        header_dashboard()

    with c2:

        st.subheader(
            f"Welcome, {student_data.get('name', 'Student')}"
        )

        if st.button(
            "Logout",
            key="student_logout"
        ):

            st.session_state.pop(
                "student_data",
                None
            )

            st.session_state.pop(
                "student_tab",
                None
            )

            st.rerun()

    st.divider()

    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3 = st.columns(
        3
    )

    with tab1:

        if st.button(
            "Subjects",
            key="student_subjects_tab"
        ):

            st.session_state[
                "student_tab"
            ] = "subjects"

            st.rerun()

    with tab2:

        if st.button(
            "Notices",
            key="student_notices_tab"
        ):

            st.session_state[
                "student_tab"
            ] = "notices"

            st.rerun()

    with tab3:

        if st.button(
            "Notes",
            key="student_notes_tab"
        ):

            st.session_state[
                "student_tab"
            ] = "notes"

            st.rerun()

    # ========================================================
    # DEFAULT TAB
    # ========================================================

    if "student_tab" not in st.session_state:

        st.session_state[
            "student_tab"
        ] = "subjects"

    st.divider()

    # ========================================================
    # SUBJECTS
    # ========================================================

    if st.session_state[
        "student_tab"
    ] == "subjects":

        c1, c2 = st.columns(
            2,
            vertical_alignment="center"
        )

        with c1:

            st.header(
                "Your Enrolled Subjects"
            )

        with c2:

            if st.button(
                "Enroll Your Subjects",
                type="primary",
                key="student_enroll_subjects"
            ):

                enroll_dialog()

        # ====================================================
        # GET SUBJECTS
        # ====================================================

        try:

            subjects = get_student_subjects(
                student_id
            )

        except Exception as e:

            st.error(
                f"Unable to load subjects: {e}"
            )

            subjects = []

        # ====================================================
        # GET ATTENDANCE
        # ====================================================

        try:

            logs = get_student_attendance(
                student_id
            )

        except Exception as e:

            st.error(
                f"Unable to load attendance: {e}"
            )

            logs = []

        # ====================================================
        # ATTENDANCE STATS
        # ====================================================

        stats_map = {}

        for log in logs:

            sid = log.get(
                "subject_id"
            )

            if sid is None:

                continue

            if sid not in stats_map:

                stats_map[sid] = {
                    "total": 0,
                    "attended": 0
                }

            stats_map[sid]["total"] += 1

            if log.get(
                "is_present",
                False
            ):

                stats_map[sid]["attended"] += 1

        # ====================================================
        # NO SUBJECTS
        # ====================================================

        if not subjects:

            st.info(
                "You are not enrolled in any subjects yet."
            )

        # ====================================================
        # SUBJECT CARDS
        # ====================================================

        else:

            cols = st.columns(
                2
            )

            for i, sub_node in enumerate(
                subjects
            ):

                if not sub_node:

                    continue

                sub = sub_node.get(
                    "subjects"
                )

                if not sub:

                    continue

                sid = sub.get(
                    "subject_id"
                )

                if sid is None:

                    continue

                subject_name = sub.get(
                    "name",
                    "Unknown Subject"
                )

                subject_code = sub.get(
                    "subject_code",
                    "N/A"
                )

                section = sub.get(
                    "section",
                    "N/A"
                )

                stats = stats_map.get(
                    sid,
                    {
                        "total": 0,
                        "attended": 0
                    }
                )

                def unenroll(
                    subject_id=sid
                ):

                    if st.button(
                        "Unenroll From Enrolled Subjects",
                        key=f"u_{subject_id}",
                        width="stretch"
                    ):

                        try:

                            unenroll_student_to_subject(
                                student_id,
                                subject_id
                            )

                            st.success(
                                "Successfully unenrolled."
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Unable to unenroll: {e}"
                            )

                with cols[
                    i % 2
                ]:

                    subject_card(
                        name=subject_name,
                        code=subject_code,
                        section=section,
                        stats=[
                            (
                                "📅",
                                "Total",
                                stats["total"]
                            ),
                            (
                                "✅",
                                "Attended",
                                stats["attended"]
                            )
                        ],
                        footer_callback=unenroll
                    )

    # ========================================================
    # NOTICES
    # ========================================================

    elif st.session_state[
        "student_tab"
    ] == "notices":

        st.header(
            "📢 Notice For You"
        )

        try:

            notices_response = (
                supabase
                .table("notices")
                .select("*")
                .order(
                    "created_at",
                    desc=True
                )
                .execute()
            )

            notices = (
                notices_response.data or []
            )

        except Exception as e:

            st.error(
                f"Unable to load notices: {e}"
            )

            notices = []

        if not notices:

            st.info(
                "No notices yet"
            )

        else:

            for n in notices:

                title = n.get(
                    "title",
                    "Notice"
                )

                content = n.get(
                    "content",
                    ""
                )

                created_at = n.get(
                    "created_at",
                    ""
                )

                st.markdown(
                    f"""
                    <div style="
                        background-color:#0E1117;
                        padding:18px;
                        border-radius:14px;
                        margin-bottom:15px;
                        border:1px solid #262730;
                        box-shadow:
                            0 4px 10px
                            rgba(0,0,0,0.4);
                    ">

                        <h4 style="
                            color:white;
                            margin-bottom:6px;
                        ">
                            📢 {title}
                        </h4>

                        <p style="
                            color:#cfcfcf;
                            margin-bottom:10px;
                        ">
                            {content}
                        </p>

                        <small style="
                            color:#888;
                        ">
                            {created_at}
                        </small>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # ========================================================
    # NOTES
    # ========================================================

    elif st.session_state[
        "student_tab"
    ] == "notes":

        st.header(
            "📝 Notes For You"
        )

        notes = get_notes_for_student(
            student_id
        )

        if not notes:

            st.info(
                "No notes available"
            )

        else:

            for n in notes:

                st.write(
                    "📌",
                    n.get(
                        "content",
                        ""
                    )
                )

    # ========================================================
    # FOOTER
    # ========================================================

    footer_dashboard()


# ============================================================
# STUDENT SCREEN
# ============================================================

def student_screen():

    style_background_dashboard()
    style_base_layout()

    # ========================================================
    # ALREADY LOGGED IN
    # ========================================================

    if "student_data" in st.session_state:

        student_dashboard()

        return

    # ========================================================
    # HEADER
    # ========================================================

    header_dashboard()

    st.header(
        "Login using Face"
    )

    st.write(
        "Capture your face to login."
    )

    # ========================================================
    # CAMERA
    # ========================================================

    photo = st.camera_input(
        "Capture Face",
        key="student_login_camera"
    )

    if not photo:

        return

    # ========================================================
    # READ IMAGE
    # ========================================================

    try:

        img = np.array(
            Image.open(
                photo
            ).convert("RGB")
        )

    except Exception as e:

        st.error(
            f"Unable to read camera image: {e}"
        )

        return

    # ========================================================
    # FACE PREDICTION
    # ========================================================

    try:

        detected, all_students, faces = (
            predict_attendance(
                img
            )
        )

    except Exception as e:

        st.error(
            f"Face recognition failed: {e}"
        )

        return

    # ========================================================
    # DEBUG INFORMATION
    # ========================================================

    if faces > 0:

        st.write(
            f"Faces detected: {faces}"
        )

    if all_students:

        st.write(
            f"Registered face profiles: {len(all_students)}"
        )

    # ========================================================
    # FACE LOGIN
    # ========================================================

    if faces == 1 and detected:

        sid = list(
            detected.keys()
        )[0]

        try:

            students = get_all_students()

        except Exception as e:

            st.error(
                f"Unable to load student data: {e}"
            )

            return

        student = None

        for s in students:

            try:

                if int(
                    s.get(
                        "student_id"
                    )
                ) == int(sid):

                    student = s

                    break

            except Exception:

                continue

        if student:

            st.session_state[
                "student_data"
            ] = student

            st.session_state[
                "student_tab"
            ] = "subjects"

            st.success(
                "Face recognized successfully! 👋"
            )

            st.rerun()

        else:

            st.error(
                "Student recognized, but student record "
                "was not found in the database."
            )

        return

    # ========================================================
    # FACE NOT RECOGNIZED
    # ========================================================

    if faces == 0:

        st.warning(
            "No face detected. "
            "Please make sure your face is clearly visible."
        )

    elif faces > 1:

        st.warning(
            "Multiple faces detected. "
            "Please make sure only one person "
            "is visible in the camera."
        )

    else:

        st.warning(
            "Face detected but not recognized."
        )

    # ========================================================
    # REGISTRATION
    # ========================================================

    st.divider()

    st.subheader(
        "Register Student"
    )

    name = st.text_input(
        "Name",
        placeholder="Enter your full name",
        key="student_register_name"
    )

    audio = st.audio_input(
        "Voice (optional)",
        key="student_register_voice"
    )

    if st.button(
        "Register",
        type="primary",
        key="student_register_button"
    ):

        if not name.strip():

            st.warning(
                "Please enter your name."
            )

            return

        # ====================================================
        # FACE EMBEDDING
        # ====================================================

        try:

            enc = get_face_embeddings(
                img
            )

        except Exception as e:

            st.error(
                f"Unable to create face embedding: {e}"
            )

            return

        if not enc:

            st.error(
                "Face error. "
                "Please capture a clear image "
                "with your face visible."
            )

            return

        # ====================================================
        # CHECK EMBEDDING
        # ====================================================

        if len(enc[0]) != 128:

            st.error(
                "Invalid face embedding. "
                "Expected 128 values."
            )

            return

        # ====================================================
        # VOICE EMBEDDING
        # ====================================================

        voice = None

        if audio:

            try:

                audio_bytes = audio.read()

                voice = get_voice_embedding(
                    audio_bytes
                )

            except Exception as e:

                st.warning(
                    f"Voice profile could not be created: {e}"
                )

                voice = None

        # ====================================================
        # CREATE STUDENT
        # ====================================================

        try:

            data = create_student(
                name.strip(),
                face_embedding=enc[0].tolist(),
                voice_embedding=voice
            )

        except Exception as e:

            st.error(
                f"Unable to register student: {e}"
            )

            return

        if not data:

            st.error(
                "Student registration failed. "
                "No data was returned from Supabase."
            )

            return

        # ====================================================
        # GET STUDENT ID
        # ========================================================

        created_student = data[0]

        created_student_id = (
            created_student.get(
                "student_id"
            )
        )

        if created_student_id is None:

            st.error(
                "Student was created, but student_id "
                "was not returned."
            )

            return

        # ====================================================
        # REFRESH FACE CLASSIFIER
        # ========================================================

        try:

            trained = train_classifier()

            if not trained:

                st.warning(
                    "Student registered, but the "
                    "face classifier could not be trained."
                )

        except Exception as e:

            st.warning(
                f"Face classifier refresh failed: {e}"
            )

        # ====================================================
        # RELOAD STUDENT FROM DATABASE
        # ========================================================

        try:

            students = get_all_students()

        except Exception as e:

            st.error(
                f"Student created but could not reload "
                f"student information: {e}"
            )

            return

        registered_student = None

        for student in students:

            try:

                if int(
                    student.get(
                        "student_id"
                    )
                ) == int(created_student_id):

                    registered_student = student

                    break

            except Exception:

                continue

        if registered_student is None:

            st.error(
                "Student was registered, but the "
                "student record could not be found."
            )

            return

        # ====================================================
        # LOGIN
        # ====================================================

        st.session_state[
            "student_data"
        ] = registered_student

        st.session_state[
            "student_tab"
        ] = "subjects"

        st.success(
            "Registration successful! 👋"
        )

        st.rerun()


# ============================================================
# MESSAGING
# ============================================================

def is_student_allowing_messages(
    student_id
):

    try:

        res = (
            supabase
            .table("students")
            .select(
                "allow_messages"
            )
            .eq(
                "student_id",
                student_id
            )
            .execute()
        )

        if not res.data:

            return False

        return bool(
            res.data[0].get(
                "allow_messages",
                False
            )
        )

    except Exception:

        return False


def send_student_message(
    sender_id,
    receiver_id,
    message
):

    if not is_student_allowing_messages(
        receiver_id
    ):

        return {
            "error": "User disabled messages"
        }

    return (
        supabase
        .table("messages")
        .insert(
            {
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "message": message
            }
        )
        .execute()
        .data
    )


def get_student_messages(
    student_id
):

    try:

        return (
            supabase
            .table("messages")
            .select("*")
            .eq(
                "receiver_id",
                student_id
            )
            .execute()
            .data
            or []
        )

    except Exception as e:

        st.error(
            f"Unable to load messages: {e}"
        )

        return []


def update_message_permission(
    student_id,
    allow
):

    try:

        return (
            supabase
            .table("students")
            .update(
                {
                    "allow_messages": allow
                }
            )
            .eq(
                "student_id",
                student_id
            )
            .execute()
            .data
        )

    except Exception as e:

        st.error(
            f"Unable to update message permission: {e}"
        )

        return []


# ============================================================
# NOTES
# ============================================================

def get_notes_for_student(
    student_id
):

    try:

        res = (
            supabase
            .table("notes")
            .select("*")
            .execute()
        )

        notes = res.data or []

        return [
            n
            for n in notes
            if (
                n.get("receiver_id") == student_id
                or
                n.get("receiver_id") is None
            )
        ]

    except Exception as e:

        st.error(
            f"Unable to load notes: {e}"
        )

        return []