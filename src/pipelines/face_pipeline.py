import dlib
import numpy as np
import face_recognition_models
import streamlit as st

from sklearn.svm import SVC
from src.database.db import get_all_students


# ============================================================
# LOAD DLIB MODELS
# ============================================================

@st.cache_resource
def load_dlib_models():

    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


# ============================================================
# GET FACE EMBEDDINGS
# ============================================================

def get_face_embeddings(image_np):

    detector, sp, facerec = load_dlib_models()

    image_np = np.asarray(
        image_np,
        dtype=np.uint8
    )

    faces = detector(image_np, 1)

    encodings = []

    for face in faces:

        shape = sp(
            image_np,
            face
        )

        face_descriptor = facerec.compute_face_descriptor(
            image_np,
            shape,
            1
        )

        embedding = np.asarray(
            face_descriptor,
            dtype=np.float64
        )

        # Dlib face embedding must contain 128 values
        if embedding.shape == (128,):

            encodings.append(embedding)

    return encodings


# ============================================================
# TRAIN CLASSIFIER
# ============================================================

@st.cache_resource
def get_trained_model():

    X = []
    y = []

    # --------------------------------------------------------
    # GET STUDENTS
    # --------------------------------------------------------

    try:

        students = get_all_students()

    except Exception as e:

        print("Error getting students:", e)

        return None

    if not students:

        print("No students found.")

        return None

    # --------------------------------------------------------
    # COLLECT VALID EMBEDDINGS
    # --------------------------------------------------------

    for student in students:

        student_id = student.get("student_id")
        embedding = student.get("face_embedding")

        if student_id is None:
            continue

        if embedding is None:
            continue

        try:

            embedding = np.asarray(
                embedding,
                dtype=np.float64
            )

        except Exception:

            print(
                f"Invalid embedding for student "
                f"{student_id}"
            )

            continue

        # ----------------------------------------------------
        # MUST BE 128 DIMENSIONS
        # ----------------------------------------------------

        if embedding.shape != (128,):

            print(
                f"Skipping student {student_id}: "
                f"embedding shape = {embedding.shape}"
            )

            continue

        # ----------------------------------------------------
        # CHECK NAN / INFINITY
        # ----------------------------------------------------

        if not np.all(np.isfinite(embedding)):

            print(
                f"Skipping student {student_id}: "
                f"embedding contains invalid numbers"
            )

            continue

        X.append(embedding)
        y.append(int(student_id))

    # --------------------------------------------------------
    # NO VALID DATA
    # --------------------------------------------------------

    if len(X) == 0:

        print("No valid face embeddings.")

        return None

    # --------------------------------------------------------
    # UNIQUE STUDENTS
    # --------------------------------------------------------

    unique_students = sorted(
        set(y)
    )

    print(
        "Students used for training:",
        unique_students
    )

    print(
        "Number of embeddings:",
        len(X)
    )

    # ========================================================
    # ONE STUDENT
    # ========================================================

    if len(unique_students) == 1:

        return {
            "clf": None,
            "X": X,
            "y": y,
            "single_student_id": unique_students[0]
        }

    # ========================================================
    # TWO OR MORE STUDENTS
    # ========================================================

    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    # VERY IMPORTANT:
    # DO NOT silently ignore training errors.

    try:

        clf.fit(
            np.asarray(X),
            np.asarray(y)
        )

    except Exception as e:

        print(
            "SVC TRAINING FAILED:",
            repr(e)
        )

        return None

    # --------------------------------------------------------
    # CONFIRM MODEL IS FITTED
    # --------------------------------------------------------

    if not hasattr(clf, "support_"):

        print(
            "ERROR: SVC was created but not fitted."
        )

        return None

    print("SVC successfully trained.")

    return {
        "clf": clf,
        "X": X,
        "y": y,
        "single_student_id": None
    }


# ============================================================
# RETRAIN CLASSIFIER
# ============================================================

def train_classifier():

    try:

        get_trained_model.clear()

    except Exception:

        pass

    model_data = get_trained_model()

    return model_data is not None


# ============================================================
# PREDICT ATTENDANCE
# ============================================================

def predict_attendance(image_np):

    detected_student = {}

    # --------------------------------------------------------
    # DETECT FACE
    # --------------------------------------------------------

    encodings = get_face_embeddings(
        image_np
    )

    if not encodings:

        return (
            detected_student,
            [],
            0
        )

    # --------------------------------------------------------
    # GET MODEL
    # --------------------------------------------------------

    model_data = get_trained_model()

    if model_data is None:

        print(
            "No trained face model available."
        )

        return (
            detected_student,
            [],
            len(encodings)
        )

    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(
        set(y_train)
    )

    if not all_students:

        return (
            detected_student,
            [],
            len(encodings)
        )

    clf = model_data["clf"]

    single_student_id = model_data.get(
        "single_student_id"
    )

    # --------------------------------------------------------
    # PROCESS DETECTED FACES
    # --------------------------------------------------------

    for encoding in encodings:

        encoding = np.asarray(
            encoding,
            dtype=np.float64
        )

        if encoding.shape != (128,):

            continue

        # ====================================================
        # ONE STUDENT
        # ====================================================

        if len(all_students) == 1:

            predicted_id = int(
                single_student_id
            )

        # ====================================================
        # MULTIPLE STUDENTS
        # ====================================================

        else:

            # NEVER call predict() if clf is None
            if clf is None:

                print(
                    "Classifier is unavailable."
                )

                continue

            # NEVER use an unfitted classifier
            if not hasattr(clf, "support_"):

                print(
                    "Classifier is not fitted."
                )

                continue

            try:

                predicted_id = int(
                    clf.predict(
                        [encoding]
                    )[0]
                )

            except Exception as e:

                print(
                    "Prediction failed:",
                    repr(e)
                )

                continue

        # ----------------------------------------------------
        # FIND STUDENT EMBEDDINGS
        # ----------------------------------------------------

        indexes = [
            i
            for i, student_id
            in enumerate(y_train)
            if int(student_id) == predicted_id
        ]

        if not indexes:

            continue

        # ----------------------------------------------------
        # CALCULATE FACE DISTANCE
        # ----------------------------------------------------

        best_distance = float("inf")

        for index in indexes:

            student_embedding = np.asarray(
                X_train[index],
                dtype=np.float64
            )

            distance = np.linalg.norm(
                student_embedding - encoding
            )

            if distance < best_distance:

                best_distance = distance

        # ----------------------------------------------------
        # FACE MATCH THRESHOLD
        # ----------------------------------------------------

        threshold = 0.6

        print(
            f"Student: {predicted_id} | "
            f"Face distance: {best_distance:.4f}"
        )

        if best_distance <= threshold:

            detected_student[
                predicted_id
            ] = True

    return (
        detected_student,
        all_students,
        len(encodings)
    )
