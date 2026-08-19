import streamlit as st

from src.pipelines.voice_pipeline import process_bulk_audio

from src.database.config import supabase

import pandas as pd

from src.components.dialog_attendance_results import show_attendance_result

from datetime import datetime


@st.dialog('Voice Attendance')
def voice_attendance_dialog(selected_subject_id):

    st.write(
        'Record audio of students saying I am present. '
        'Then AI will recognize the students'
    )

    audio_data = st.audio_input(
        "Record classroom audio"
    )

    if st.button(
        'Analyze Audio',
        width='stretch',
        type='primary'
    ):

        if audio_data is None:

            st.warning(
                'Please record classroom audio first'
            )

            return

        with st.spinner(
            'Processing Audio data'
        ):

            try:

                # ==========================================
                # GET ENROLLED STUDENTS
                # ==========================================

                enrolled_res = (
                    supabase
                    .table('subject_students')
                    .select('*, students(*)')
                    .eq(
                        'subject_id',
                        selected_subject_id
                    )
                    .execute()
                )

                enrolled_students = (
                    enrolled_res.data or []
                )

                if not enrolled_students:

                    st.warning(
                        'No students enrolled in this course'
                    )

                    return


                # ==========================================
                # CREATE VOICE CANDIDATES
                # ==========================================

                candidates_dict = {}

                for node in enrolled_students:

                    student = node.get(
                        'students'
                    )

                    if not student:
                        continue

                    student_id = student.get(
                        'student_id'
                    )

                    voice_embedding = student.get(
                        'voice_embedding'
                    )

                    if (
                        student_id is None
                        or voice_embedding is None
                    ):
                        continue

                    try:

                        if isinstance(
                            voice_embedding,
                            str
                        ):

                            import json

                            voice_embedding = json.loads(
                                voice_embedding
                            )

                        if not isinstance(
                            voice_embedding,
                            list
                        ):

                            voice_embedding = list(
                                voice_embedding
                            )

                        if len(
                            voice_embedding
                        ) == 0:

                            continue

                        candidates_dict[
                            int(student_id)
                        ] = voice_embedding

                    except Exception:

                        continue


                # ==========================================
                # CHECK VOICE PROFILES
                # ==========================================

                if not candidates_dict:

                    st.error(
                        'No enrolled students have voice '
                        'profiles registered'
                    )

                    return


                # ==========================================
                # READ AUDIO
                # ==========================================

                audio_bytes = audio_data.read()

                if not audio_bytes:

                    st.warning(
                        'Recorded audio is empty. '
                        'Please record again.'
                    )

                    return


                # ==========================================
                # PROCESS AUDIO
                # ==========================================

                detected_scores = process_bulk_audio(
                    audio_bytes,
                    candidates_dict
                )


                if detected_scores is None:

                    detected_scores = {}


                # ==========================================
                # CREATE RESULTS
                # ==========================================

                results = []

                attendance_to_log = []

                current_timestamp = (
                    datetime.now().strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )
                )


                for node in enrolled_students:

                    student = node.get(
                        'students'
                    )

                    if not student:
                        continue

                    student_id = student.get(
                        'student_id'
                    )

                    student_name = student.get(
                        'name',
                        'Unknown Student'
                    )

                    if student_id is None:
                        continue

                    student_id = int(
                        student_id
                    )

                    score = detected_scores.get(
                        student_id
                    )

                    is_present = (
                        student_id
                        in detected_scores
                    )


                    # ======================================
                    # RESULT
                    # ======================================

                    results.append(
                        {
                            "Name": student_name,

                            "ID": student_id,

                            "Source": (
                                f"{score:.2f}"
                                if is_present
                                else "-"
                            ),

                            "Status": (
                                "✅ Present"
                                if is_present
                                else "❌ Absent"
                            )
                        }
                    )


                    # ======================================
                    # ATTENDANCE LOG
                    # ======================================

                    attendance_to_log.append(
                        {
                            'student_id': student_id,

                            'subject_id': selected_subject_id,

                            'timestamp': current_timestamp,

                            'is_present': bool(
                                is_present
                            )
                        }
                    )


                # ==========================================
                # CHECK RESULTS
                # ==========================================

                if not results:

                    st.warning(
                        'No valid student records found'
                    )

                    return


                # ==========================================
                # SAVE RESULTS IN SESSION
                # ==========================================

                st.session_state[
                    'voice_attendance_results'
                ] = (
                    pd.DataFrame(results),
                    attendance_to_log
                )


                # ==========================================
                # SHOW SUCCESS
                # ==========================================

                present_count = sum(
                    1
                    for result in results
                    if result["Status"] == "✅ Present"
                )

                st.success(
                    f"Voice analysis completed. "
                    f"{present_count} student(s) detected."
                )


            except Exception as e:

                st.error(
                    f'Voice attendance failed: {e}'
                )


    # ==============================================
    # SHOW ATTENDANCE RESULTS
    # ==============================================

    if st.session_state.get(
        'voice_attendance_results'
    ):

        st.divider()

        df_results, logs = (
            st.session_state[
                'voice_attendance_results'
            ]
        )

        show_attendance_result(
            df_results,
            logs
        )