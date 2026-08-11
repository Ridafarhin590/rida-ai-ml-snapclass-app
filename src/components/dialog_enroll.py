import streamlit as st
import time

from src.database.db import enroll_student_to_subject
from src.database.config import supabase


@st.dialog("Enroll in Subject")
def enroll_dialog():

    st.write(
        "Enter the subject code provided by your teacher to enroll"
    )

    join_code = st.text_input(
        "Subject Code",
        placeholder="Eg. CS101"
    )

    if st.button(
        "Enroll now",
        type="primary",
        width="stretch"
    ):

        if join_code:

            # Remove accidental spaces and make code uppercase
            join_code = join_code.strip().upper()

            # Find subject
            res = (
                supabase
                .table("subjects")
                .select("subject_id, name, subject_code")
                .eq("subject_code", join_code)
                .execute()
            )

            if res.data:

                subject = res.data[0]

                student_id = st.session_state.student_data["student_id"]

                # Check whether student is already enrolled
                check = (
                    supabase
                    .table("subject_students")
                    .select("*")
                    .eq("subject_id", subject["subject_id"])
                    .eq("student_id", student_id)
                    .execute()
                )

                if check.data:

                    st.warning(
                        "You are already enrolled in this subject."
                    )

                else:

                    # Enroll student
                    enroll_student_to_subject(
                        student_id,
                        subject["subject_id"]
                    )

                    st.success(
                        f"Successfully enrolled in {subject['name']}!"
                    )

                    time.sleep(1)

                    st.rerun()

            else:

                st.error(
                    f"No subject found with code: {join_code}"
                )

        else:

            st.warning(
                "Please enter a subject code."
            )