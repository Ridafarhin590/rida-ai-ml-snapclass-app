import streamlit as st
import time
import numpy as np
import pandas as pd

from datetime import datetime

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher
)

from src.database.config import supabase

from src.components.dialog_create_subject import (
    create_subject_dialog
)

from src.components.dialog_share_subject import (
    share_subject_dialog
)

from src.components.dialog_add_photo import (
    add_photos_dialog
)

from src.components.dialog_voice_attendance import (
    voice_attendance_dialog
)

from src.components.dialog_attendance_results import (
    attendance_result_dialog
)

from src.pipelines.face_pipeline import (
    predict_attendance
)


# ============================================================
# TEACHER MAIN SCREEN
# ============================================================

def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    # --------------------------------------------------------
    # LOGGED IN
    # --------------------------------------------------------

    if "teacher_data" in st.session_state:

        teacher_dashboard()
        return

    # --------------------------------------------------------
    # DEFAULT LOGIN TYPE
    # --------------------------------------------------------

    if "teacher_login_type" not in st.session_state:

        st.session_state["teacher_login_type"] = "login"

    # --------------------------------------------------------
    # LOGIN / REGISTER
    # --------------------------------------------------------

    if st.session_state["teacher_login_type"] == "register":

        teacher_screen_register()

    else:

        teacher_screen_login()


# ============================================================
# TEACHER DASHBOARD
# ============================================================

def teacher_dashboard():

    teacher_data = st.session_state.get(
        "teacher_data"
    )

    if not teacher_data:

        st.session_state.pop(
            "teacher_data",
            None
        )

        st.session_state[
            "teacher_login_type"
        ] = "login"

        st.rerun()

    # ========================================================
    # HEADER
    # ========================================================

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="large"
    )

    with c1:

        header_dashboard()

    with c2:

        st.subheader(
            f"Welcome, {teacher_data.get('name', 'Teacher')}"
        )

        if st.button(
            "Logout",
            type="secondary",
            key="teacher_logout"
        ):

            st.session_state.pop(
                "teacher_data",
                None
            )

            st.session_state[
                "is_logged_in"
            ] = False

            st.session_state[
                "user_role"
            ] = None

            st.session_state[
                "teacher_login_type"
            ] = "login"

            st.session_state[
                "current_teacher_tab"
            ] = "take_attendance"

            st.session_state[
                "attendance_images"
            ] = []

            st.rerun()

    st.divider()

    # ========================================================
    # DEFAULT TAB
    # ========================================================

    if "current_teacher_tab" not in st.session_state:

        st.session_state[
            "current_teacher_tab"
        ] = "take_attendance"

    # ========================================================
    # NAVIGATION
    # ========================================================

    tab1, tab2, tab3, tab4 = st.columns(
        4
    )

    with tab1:

        if st.button(
            "📸 Attendance",
            width="stretch",
            key="teacher_nav_attendance"
        ):

            st.session_state[
                "current_teacher_tab"
            ] = "take_attendance"

            st.rerun()

    with tab2:

        if st.button(
            "📚 Subjects",
            width="stretch",
            key="teacher_nav_subjects"
        ):

            st.session_state[
                "current_teacher_tab"
            ] = "manage_subjects"

            st.rerun()

    with tab3:

        if st.button(
            "📢 Notices",
            width="stretch",
            key="teacher_nav_notices"
        ):

            st.session_state[
                "current_teacher_tab"
            ] = "notices"

            st.rerun()

    with tab4:

        if st.button(
            "📊 Records",
            width="stretch",
            key="teacher_nav_records"
        ):

            st.session_state[
                "current_teacher_tab"
            ] = "attendance_records"

            st.rerun()

    st.divider()

    # ========================================================
    # CURRENT TAB
    # ========================================================

    current_tab = st.session_state[
        "current_teacher_tab"
    ]

    if current_tab == "take_attendance":

        teacher_tab_take_attendance()

    elif current_tab == "manage_subjects":

        teacher_tab_manage_subjects()

    elif current_tab == "notices":

        teacher_tab_notices()

    elif current_tab == "attendance_records":

        teacher_tab_attendance_records()

    footer_dashboard()


# ============================================================
# GET ENROLLED STUDENTS
# ============================================================

def get_enrolled_students_for_subject(
    subject_id
):

    try:

        # ----------------------------------------------------
        # FIRST GET ENROLLMENT ROWS
        # ----------------------------------------------------

        enrollment_response = (
            supabase
            .table("subject_students")
            .select(
                "student_id, subject_id"
            )
            .eq(
                "subject_id",
                subject_id
            )
            .execute()
        )

        enrollment_rows = (
            enrollment_response.data or []
        )

        if not enrollment_rows:

            return []

        # ----------------------------------------------------
        # GET STUDENT IDS
        # ----------------------------------------------------

        student_ids = [
            int(row["student_id"])
            for row in enrollment_rows
            if row.get("student_id") is not None
        ]

        if not student_ids:

            return []

        # ----------------------------------------------------
        # GET STUDENTS
        # ----------------------------------------------------

        students_response = (
            supabase
            .table("students")
            .select(
                "student_id, name"
            )
            .in_(
                "student_id",
                student_ids
            )
            .execute()
        )

        students = (
            students_response.data or []
        )

        # ----------------------------------------------------
        # MAP STUDENTS
        # ----------------------------------------------------

        student_map = {
            int(student["student_id"]): student
            for student in students
        }

        enrolled_students = []

        for row in enrollment_rows:

            student_id = int(
                row["student_id"]
            )

            student = student_map.get(
                student_id
            )

            if student:

                enrolled_students.append(
                    {
                        "student_id": student_id,
                        "students": student
                    }
                )

        return enrolled_students

    except Exception as e:

        st.error(
            f"Unable to load enrolled students: {e}"
        )

        return []


# ============================================================
# TAKE ATTENDANCE
# ============================================================

def teacher_tab_take_attendance():

    teacher_id = st.session_state[
        "teacher_data"
    ]["teacher_id"]

    st.header(
        "📸 AI Attendance"
    )

    st.write(
        "Take attendance using classroom photos "
        "or voice recognition."
    )

    # ========================================================
    # ATTENDANCE IMAGES
    # ========================================================

    if "attendance_images" not in st.session_state:

        st.session_state[
            "attendance_images"
        ] = []

    # ========================================================
    # GET SUBJECTS
    # ========================================================

    try:

        subjects = get_teacher_subjects(
            teacher_id
        )

    except Exception as e:

        st.error(
            f"Unable to load subjects: {e}"
        )

        return

    if not subjects:

        st.warning(
            "You haven't created any subjects yet."
        )

        st.info(
            "Go to 📚 Subjects and create a subject first."
        )

        return

    # ========================================================
    # SUBJECT DROPDOWN
    # ========================================================

    subject_options = {}

    for subject in subjects:

        subject_name = subject.get(
            "name",
            "Unknown Subject"
        )

        subject_code = subject.get(
            "subject_code",
            "N/A"
        )

        subject_id = subject.get(
            "subject_id"
        )

        if subject_id is not None:

            subject_options[
                f"{subject_name} - {subject_code}"
            ] = subject_id

    if not subject_options:

        st.error(
            "No valid subjects found."
        )

        return

    col1, col2 = st.columns(
        [3, 1],
        vertical_alignment="bottom"
    )

    with col1:

        selected_subject_label = st.selectbox(
            "Select Subject",
            list(
                subject_options.keys()
            ),
            key="attendance_subject"
        )

    with col2:

        if st.button(
            "📷 Add Photos",
            type="primary",
            width="stretch",
            key="add_attendance_photos"
        ):

            add_photos_dialog()

    selected_subject_id = (
        subject_options[
            selected_subject_label
        ]
    )

    st.divider()

    # ========================================================
    # ATTENDANCE METHOD
    # ========================================================

    st.subheader(
        "Choose Attendance Method"
    )

    method1, method2 = st.columns(
        2
    )

    with method1:

        st.info(
            "📸 Photo Attendance\n\n"
            "Upload classroom photos and "
            "run AI face recognition."
        )

    with method2:

        st.info(
            "🎤 Voice Attendance\n\n"
            "Use voice recognition to mark "
            "student attendance."
        )

    st.divider()

    # ========================================================
    # SHOW PHOTOS
    # ========================================================

    if st.session_state[
        "attendance_images"
    ]:

        st.subheader(
            "Added Classroom Photos"
        )

        gallery_cols = st.columns(
            4
        )

        for idx, image in enumerate(
            st.session_state[
                "attendance_images"
            ]
        ):

            with gallery_cols[
                idx % 4
            ]:

                st.image(
                    image,
                    width="stretch",
                    caption=f"Photo {idx + 1}"
                )

    # ========================================================
    # HAS PHOTOS
    # ========================================================

    has_photos = bool(
        st.session_state[
            "attendance_images"
        ]
    )

    # ========================================================
    # ACTION BUTTONS
    # ========================================================

    c1, c2, c3 = st.columns(
        3
    )

    # ========================================================
    # CLEAR
    # ========================================================

    with c1:

        if st.button(
            "🗑️ Clear Photos",
            width="stretch",
            disabled=not has_photos,
            key="clear_all_photos"
        ):

            st.session_state[
                "attendance_images"
            ] = []

            st.rerun()

    # ========================================================
    # FACE ATTENDANCE
    # ========================================================

    with c2:

        if st.button(
            "🔍 Run Face Analysis",
            type="secondary",
            width="stretch",
            disabled=not has_photos,
            key="run_face_analysis"
        ):

            run_photo_attendance(
                selected_subject_id
            )

    # ========================================================
    # VOICE ATTENDANCE
    # ========================================================

    with c3:

        if st.button(
            "🎤 Voice Attendance",
            type="primary",
            width="stretch",
            key="voice_attendance"
        ):

            try:

                voice_attendance_dialog(
                    selected_subject_id
                )

            except Exception as e:

                st.error(
                    f"Unable to start voice attendance: {e}"
                )


# ============================================================
# PHOTO ATTENDANCE
# ============================================================

def run_photo_attendance(
    selected_subject_id
):

    with st.spinner(
        "Deep scanning classroom photos..."
    ):

        # ====================================================
        # GET ENROLLED STUDENTS FIRST
        # ====================================================

        enrolled_students = (
            get_enrolled_students_for_subject(
                selected_subject_id
            )
        )

        if not enrolled_students:

            st.warning(
                "No students enrolled in this course."
            )

            st.info(
                "Ask students to enroll using the "
                "subject code before taking attendance."
            )

            return

        st.success(
            f"{len(enrolled_students)} "
            f"student(s) enrolled in this subject."
        )

        # ====================================================
        # FACE DETECTION
        # ====================================================

        all_detected_ids = {}

        images = st.session_state.get(
            "attendance_images",
            []
        )

        if not images:

            st.warning(
                "Please add at least one classroom photo."
            )

            return

        # ====================================================
        # PROCESS EVERY PHOTO
        # ====================================================

        for idx, image in enumerate(
            images
        ):

            try:

                image_np = np.array(
                    image.convert("RGB")
                )

                detected, _, _ = (
                    predict_attendance(
                        image_np
                    )
                )

                if detected:

                    for student_id in detected.keys():

                        try:

                            student_id = int(
                                student_id
                            )

                        except Exception:

                            continue

                        all_detected_ids.setdefault(
                            student_id,
                            []
                        ).append(
                            f"Photo {idx + 1}"
                        )

            except Exception as e:

                st.error(
                    f"Photo {idx + 1} analysis failed: {e}"
                )

        # ====================================================
        # CREATE RESULTS
        # ====================================================

        results = []

        attendance_to_log = []

        current_timestamp = (
            datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
        )

        for enrollment in enrolled_students:

            student = enrollment.get(
                "students"
            )

            if not student:

                continue

            student_id = int(
                student["student_id"]
            )

            student_name = student.get(
                "name",
                "Unknown Student"
            )

            sources = (
                all_detected_ids.get(
                    student_id,
                    []
                )
            )

            is_present = bool(
                sources
            )

            results.append(
                {
                    "Name": student_name,
                    "ID": student_id,
                    "Source": (
                        ", ".join(sources)
                        if sources
                        else "-"
                    ),
                    "Status": (
                        "✅ Present"
                        if is_present
                        else "❌ Absent"
                    )
                }
            )

            attendance_to_log.append(
                {
                    "student_id": student_id,
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": is_present
                }
            )

        # ====================================================
        # SHOW RESULTS
        # ====================================================

        if not results:

            st.warning(
                "No valid student records found."
            )

            return

        result_df = pd.DataFrame(
            results
        )

        # Show preview
        st.subheader(
            "Attendance Result"
        )

        st.dataframe(
            result_df,
            width="stretch",
            hide_index=True
        )

        # ====================================================
        # ATTENDANCE RESULT DIALOG
        # ====================================================

        try:

            attendance_result_dialog(
                result_df,
                attendance_to_log
            )

        except Exception as e:

            st.error(
                f"Unable to open attendance result: {e}"
            )


# ============================================================
# MANAGE SUBJECTS
# ============================================================

def teacher_tab_manage_subjects():

    teacher_id = st.session_state[
        "teacher_data"
    ]["teacher_id"]

    st.header(
        "📚 Manage Subjects"
    )

    st.write(
        "Create subjects and share the enrollment "
        "code with students."
    )

    # ========================================================
    # CREATE SUBJECT
    # ========================================================

    if st.button(
        "➕ Create New Subject",
        type="primary",
        key="create_new_subject"
    ):

        create_subject_dialog(
            teacher_id
        )

    st.divider()

    # ========================================================
    # GET SUBJECTS
    # ========================================================

    try:

        subjects = get_teacher_subjects(
            teacher_id
        )

    except Exception as e:

        st.error(
            f"Unable to load subjects: {e}"
        )

        return

    if not subjects:

        st.info(
            "No subjects found. "
            "Create your first subject above."
        )

        return

    # ========================================================
    # SUBJECT CARDS
    # ========================================================

    for subject in subjects:

        subject_name = subject.get(
            "name",
            "Unknown Subject"
        )

        subject_code = subject.get(
            "subject_code",
            "N/A"
        )

        section = subject.get(
            "section",
            "N/A"
        )

        stats = [
            (
                "👥",
                "Students",
                subject.get(
                    "total_students",
                    0
                )
            ),
            (
                "🕐",
                "Classes",
                subject.get(
                    "total_classes",
                    0
                )
            )
        ]

        def share_button(
            sub=subject
        ):

            if st.button(
                f"🔗 Share Code: {sub.get('name', 'Subject')}",
                width="stretch",
                key=f"share_{sub.get('subject_id')}"
            ):

                share_subject_dialog(
                    sub.get(
                        "name",
                        "Subject"
                    ),
                    sub.get(
                        "subject_code",
                        ""
                    )
                )

        subject_card(
            name=subject_name,
            code=subject_code,
            section=section,
            stats=stats,
            footer_callback=share_button
        )


# ============================================================
# ATTENDANCE RECORDS
# ============================================================

def teacher_tab_attendance_records():

    st.header(
        "📊 Attendance Records"
    )

    teacher_id = st.session_state[
        "teacher_data"
    ]["teacher_id"]

    try:

        records = get_attendance_for_teacher(
            teacher_id
        )

    except Exception as e:

        st.error(
            f"Unable to load attendance records: {e}"
        )

        return

    if not records:

        st.info(
            "No attendance records found."
        )

        return

    data = []

    for record in records:

        timestamp = record.get(
            "timestamp"
        )

        subject = (
            record.get("subjects")
            or {}
        )

        try:

            formatted_time = (
                datetime.fromisoformat(
                    timestamp
                ).strftime(
                    "%Y-%m-%d %I:%M %p"
                )
                if timestamp
                else "N/A"
            )

        except Exception:

            formatted_time = (
                str(timestamp)
                if timestamp
                else "N/A"
            )

        data.append(
            {
                "ts_group": (
                    str(timestamp).split(".")[0]
                    if timestamp
                    else None
                ),

                "Time": formatted_time,

                "Subject": subject.get(
                    "name",
                    "Unknown"
                ),

                "Subject Code": subject.get(
                    "subject_code",
                    "N/A"
                ),

                "is_present": bool(
                    record.get(
                        "is_present",
                        False
                    )
                )
            }
        )

    if not data:

        st.info(
            "No attendance records found."
        )

        return

    df = pd.DataFrame(
        data
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    summary = (
        df.groupby(
            [
                "ts_group",
                "Time",
                "Subject",
                "Subject Code"
            ]
        )
        .agg(
            Present_Count=(
                "is_present",
                "sum"
            ),
            Total_Count=(
                "is_present",
                "count"
            )
        )
        .reset_index()
    )

    summary[
        "Attendance Stats"
    ] = (
        "✅ "
        + summary[
            "Present_Count"
        ].astype(str)
        + " / "
        + summary[
            "Total_Count"
        ].astype(str)
        + " Students"
    )

    display_df = (
        summary
        .sort_values(
            by="ts_group",
            ascending=False
        )
        [
            [
                "Time",
                "Subject",
                "Subject Code",
                "Attendance Stats"
            ]
        ]
    )

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )


# ============================================================
# TEACHER LOGIN
# ============================================================

def login_teacher(
    username,
    password
):

    if not username or not password:

        return False

    try:

        teacher = teacher_login(
            username.strip(),
            password
        )

    except Exception as e:

        st.error(
            f"Login error: {e}"
        )

        return False

    if teacher:

        st.session_state[
            "user_role"
        ] = "teacher"

        st.session_state[
            "teacher_data"
        ] = teacher

        st.session_state[
            "is_logged_in"
        ] = True

        return True

    return False


# ============================================================
# LOGIN PAGE
# ============================================================

def teacher_screen_login():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="large"
    )

    with c1:

        header_dashboard()

    with c2:

        if st.button(
            "Go back to Home",
            type="secondary",
            key="teacher_login_back"
        ):

            st.session_state[
                "login_type"
            ] = None

            st.session_state[
                "teacher_login_type"
            ] = "login"

            st.rerun()

    st.header(
        "Teacher Login",
        text_alignment="center"
    )

    teacher_username = st.text_input(
        "Username",
        placeholder="Enter username",
        key="teacher_login_username"
    )

    teacher_password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password",
        key="teacher_login_password"
    )

    st.divider()

    c1, c2 = st.columns(
        2
    )

    with c1:

        if st.button(
            "🔐 Login",
            type="primary",
            width="stretch",
            key="teacher_login_button"
        ):

            if not teacher_username:

                st.warning(
                    "Please enter your username."
                )

            elif not teacher_password:

                st.warning(
                    "Please enter your password."
                )

            elif login_teacher(
                teacher_username,
                teacher_password
            ):

                st.success(
                    "Welcome back! 👋"
                )

                time.sleep(0.7)

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

    with c2:

        if st.button(
            "Create Teacher Account",
            width="stretch",
            key="teacher_register_button"
        ):

            st.session_state[
                "teacher_login_type"
            ] = "register"

            st.rerun()

    footer_dashboard()


# ============================================================
# REGISTER TEACHER
# ============================================================

def register_teacher(
    username,
    name,
    password,
    confirm_password
):

    if not username:

        return False, "Username is required."

    if not name:

        return False, "Name is required."

    if not password:

        return False, "Password is required."

    if not confirm_password:

        return False, "Please confirm your password."

    username = username.strip()
    name = name.strip()

    if password != confirm_password:

        return False, "Passwords do not match."

    try:

        if check_teacher_exists(
            username
        ):

            return False, "Username already taken."

    except Exception as e:

        return False, (
            f"Unable to check username: {e}"
        )

    try:

        create_teacher(
            username,
            password,
            name
        )

        return (
            True,
            "Teacher account created successfully."
        )

    except Exception as e:

        return (
            False,
            f"Registration failed: {e}"
        )


# ============================================================
# REGISTER PAGE
# ============================================================

def teacher_screen_register():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="large"
    )

    with c1:

        header_dashboard()

    with c2:

        if st.button(
            "Go back to Login",
            type="secondary",
            key="teacher_register_back"
        ):

            st.session_state[
                "teacher_login_type"
            ] = "login"

            st.rerun()

    st.header(
        "Create Teacher Account",
        text_alignment="center"
    )

    username = st.text_input(
        "Username",
        placeholder="Enter username",
        key="teacher_register_username"
    )

    name = st.text_input(
        "Teacher Name",
        placeholder="Enter teacher name",
        key="teacher_register_name"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password",
        key="teacher_register_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Confirm password",
        key="teacher_register_confirm"
    )

    st.divider()

    c1, c2 = st.columns(
        2
    )

    with c1:

        if st.button(
            "📝 Register",
            type="primary",
            width="stretch",
            key="teacher_register_now"
        ):

            success, message = register_teacher(
                username,
                name,
                password,
                confirm_password
            )

            if success:

                st.success(
                    message
                )

                time.sleep(1)

                st.session_state[
                    "teacher_login_type"
                ] = "login"

                st.rerun()

            else:

                st.error(
                    message
                )

    with c2:

        if st.button(
            "Already have account? Login",
            width="stretch",
            key="teacher_login_instead"
        ):

            st.session_state[
                "teacher_login_type"
            ] = "login"

            st.rerun()

    footer_dashboard()


# ============================================================
# CREATE NOTICE
# ============================================================

def create_notice(
    title,
    content,
    teacher_id
):

    data = {
        "title": title,
        "content": content,
        "teacher_id": teacher_id
    }

    return (
        supabase
        .table("notices")
        .insert(data)
        .execute()
        .data
    )


# ============================================================
# GET NOTICES
# ============================================================

def get_notices():

    response = (
        supabase
        .table("notices")
        .select("*")
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return response.data or []


# ============================================================
# TEACHER NOTICE TAB
# ============================================================

def teacher_tab_notices():

    teacher_id = st.session_state[
        "teacher_data"
    ]["teacher_id"]

    st.header(
        "📢 Post Notice"
    )

    st.write(
        "Create a notice and publish it for students."
    )

    # ========================================================
    # TITLE
    # ========================================================

    title = st.text_input(
        "Notice Title",
        placeholder="MCA Major Project Review",
        key="notice_title"
    )

    # ========================================================
    # TOPIC
    # ========================================================

    topic = st.text_input(
        "Notice Topic",
        placeholder=(
            "Exam, Attendance, Project Review, Holiday..."
        ),
        key="notice_topic"
    )

    # ========================================================
    # AI GENERATE
    # ========================================================

    if st.button(
        "✨ Generate Notice",
        type="secondary",
        key="generate_ai_notice"
    ):

        if not topic:

            st.warning(
                "Please enter a notice topic."
            )

        elif "exam" in topic.lower():

            st.session_state[
                "generated_notice"
            ] = (
                "Dear Students,\n\n"
                "This is to inform you that examinations "
                "will be conducted as per the academic schedule.\n\n"
                "Please prepare accordingly and maintain "
                "regular attendance.\n\n"
                "Regards,\n"
                "Faculty Coordinator"
            )

        elif "attendance" in topic.lower():

            st.session_state[
                "generated_notice"
            ] = (
                "Dear Students,\n\n"
                "Students with low attendance are advised "
                "to improve their attendance percentage "
                "immediately.\n\n"
                "Short attendance may affect examination "
                "eligibility.\n\n"
                "Regards,\n"
                "Faculty Coordinator"
            )

        elif "project" in topic.lower():

            st.session_state[
                "generated_notice"
            ] = (
                "Dear Students,\n\n"
                "This is a reminder regarding the MCA "
                "Major Project Review.\n\n"
                "Please keep your project report, source "
                "code and presentation ready.\n\n"
                "Regards,\n"
                "Faculty Coordinator"
            )

        else:

            st.session_state[
                "generated_notice"
            ] = (
                f"Dear Students,\n\n"
                f"This notice is regarding {topic}.\n\n"
                "Please follow the instructions shared "
                "by your faculty.\n\n"
                "Regards,\n"
                "Faculty Coordinator"
            )

        st.rerun()

    # ========================================================
    # CONTENT
    # ========================================================

    content = st.text_area(
        "Notice Content",
        value=st.session_state.get(
            "generated_notice",
            ""
        ),
        height=220,
        key="notice_content"
    )

    # ========================================================
    # POST NOTICE
    # ========================================================

    if st.button(
        "📢 Post Notice",
        type="primary",
        width="stretch",
        key="post_notice"
    ):

        if not title.strip():

            st.warning(
                "Please enter a notice title."
            )

            return

        if not content.strip():

            st.warning(
                "Please enter notice content."
            )

            return

        try:

            create_notice(
                title.strip(),
                content.strip(),
                teacher_id
            )

            st.success(
                "Notice posted successfully! ✅"
            )

            st.session_state.pop(
                "generated_notice",
                None
            )

            st.session_state[
                "notice_content"
            ] = ""

            time.sleep(0.8)

            st.rerun()

        except Exception as e:

            st.error(
                f"Unable to post notice: {e}"
            )

    st.divider()

    # ========================================================
    # EXISTING NOTICES
    # ========================================================

    st.subheader(
        "Published Notices"
    )

    try:

        notices = get_notices()

    except Exception as e:

        st.error(
            f"Unable to load notices: {e}"
        )

        return

    if not notices:

        st.info(
            "No notices have been posted yet."
        )

        return

    for notice in notices:

        title_value = notice.get(
            "title",
            "Notice"
        )

        content_value = notice.get(
            "content",
            ""
        )

        created_at = notice.get(
            "created_at",
            ""
        )

        st.markdown(
            f"""
            <div class="notice-card">

                <h3>
                    📢 {title_value}
                </h3>

                <p>
                    {content_value}
                </p>

                <small>
                    📅 {created_at}
                </small>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# NOTES
# ============================================================

def send_note(
    sender_id,
    receiver_id,
    content
):

    data = {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "content": content
    }

    return (
        supabase
        .table("notes")
        .insert(data)
        .execute()
        .data
    )


def get_notes_for_student(
    student_id
):

    response = (
        supabase
        .table("notes")
        .select("*")
        .execute()
    )

    notes = []

    for note in response.data or []:

        if (
            note.get("receiver_id") == student_id
            or
            note.get("receiver_id") is None
        ):

            notes.append(
                note
            )

    return notes