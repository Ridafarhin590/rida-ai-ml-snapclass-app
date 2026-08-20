# 🎓 SnapClass – AI-Based Attendance Management System

<p align="center">
  <img src="assets/ai_background.png" alt="SnapClass" width="800">
</p>

<h3 align="center">
  AI-Powered Attendance Management using Face & Voice Recognition
</h3>

<p align="center">
  An intelligent attendance management system designed for teachers and students.
</p>

<p align="center">
  <a href="https://rida-ai-ml-landing-web-page-git-main-rida-farhins-projects.vercel.app/">
    🌐 Landing Page
  </a>
  &nbsp; • &nbsp;
  <a href="https://rida-ai-ml-snapclass-app.streamlit.app/">
    🚀 Live Application
  </a>
</p>

---

## 🌐 Live Demo

### 🌎 SnapClass Landing Page

👉 **[Visit Landing Page](https://rida-ai-ml-landing-web-page-git-main-rida-farhins-projects.vercel.app/)**

The landing page provides an overview of the SnapClass project, its features, technologies, and project information.

### 🚀 SnapClass AI Application

👉 **[Launch SnapClass](https://rida-ai-ml-snapclass-app.streamlit.app/)**

The live Streamlit application allows users to interact with the AI-based attendance system.

---

# 📌 About SnapClass

**SnapClass** is an AI-based attendance management system that automates classroom attendance using **Face Recognition** and **Voice Recognition**.

The system provides separate interfaces for:

- 👨‍🏫 Teachers
- 👨‍🎓 Students

Teachers can create subjects, share enrollment codes, capture classroom photos, perform AI face recognition, use voice attendance, publish notices, and view attendance records.

Students can register using their face, optionally create a voice profile, enroll in subjects, view attendance, and access notices and notes.

---

# ✨ Features

## 👨‍🏫 Teacher Portal

### 🔐 Teacher Authentication

- Teacher registration
- Teacher login
- Secure session-based authentication
- Logout functionality

### 📚 Subject Management

Teachers can:

- Create subjects
- Define subject codes
- Define sections
- View enrolled students
- Share subject enrollment codes

### 📸 AI Face Attendance

Teachers can:

- Capture classroom photos using the camera
- Upload multiple classroom images
- Detect faces using Dlib
- Generate face embeddings
- Recognize enrolled students
- Automatically mark attendance
- View attendance results

### 🎤 Voice Attendance

The system supports voice-based attendance using:

- Audio recording
- Voice embeddings
- Speaker identification
- Cosine similarity
- Multiple-speaker audio processing

### 📊 Attendance Records

Teachers can:

- View attendance history
- View subject-wise records
- View present/absent counts
- View attendance timestamps

### 📢 Notices

Teachers can:

- Create notices
- Generate notice content
- Publish notices
- View previously published notices

---

# 👨‍🎓 Student Portal

## 👤 Face-Based Login

Students can log in using:

- Camera capture
- Face detection
- Face recognition
- Stored face embeddings

---

## 📝 Student Registration

Students can register using:

- Name
- Face image
- Optional voice recording

The system generates:

- Face embedding
- Voice embedding

and stores the profiles for future recognition.

---

## 📚 Subject Enrollment

Students can enter a subject code provided by their teacher.

Example:

```text
MCA401
