from utils.db import supabase
import streamlit as st
from utils.document_helper import (
    get_document_types,
    upload_student_document,
)

from utils.auth import login_user

from utils.helpers import (
    get_student_marksheets,
    increment_download_counter,
    download_pdf,
)

st.set_page_config(
    page_title="Student Result Portal",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "student" not in st.session_state:
    st.session_state.student = None


def logout():

    st.session_state.logged_in = False
    st.session_state.student = None

    st.rerun()


def login_page():

    st.title(
        "Student Result Portal Login"
    )

    enrollment = st.text_input(
        "Enrollment Number"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login_user(
            enrollment,
            password
        )

        if user:

            st.session_state.logged_in = True

            st.session_state.student = user

            st.rerun()

        else:

            st.error(
                "Invalid Enrollment or Password"
            )


def download_results_page():

    st.title("Download Marksheets")

    enrollment = (
        st.session_state
        .student["enrollment"]
    )

    semester = st.selectbox(
        "Select Semester",
        [
            "sem1",
            "sem2",
            "sem3",
            "sem4",
            "sem5",
            "sem6",
        ],
        index=None,
        placeholder="Choose Semester"
    )

    if not semester:
        return

    with st.spinner(
        "Loading marksheets..."
    ):

        results = get_student_marksheets(
            enrollment,
            semester
        )

    if not results:

        st.warning(
            "No marksheets found."
        )

        return

    h1, h2, h3, h4, h5, h6 = (
        st.columns([1, 2, 2, 2, 3, 2])
    )

    with h1:
        st.markdown("**S#**")

    with h2:
        st.markdown("**Semester**")

    with h3:
        st.markdown("**Session**")

    with h4:
        st.markdown("**Downloads**")

    with h5:
        st.markdown(
            "**Last Downloaded**"
        )

    with h6:
        st.markdown("**Action**")

    st.divider()

    for i, result in enumerate(
        results,
        start=1
    ):

        col1, col2, col3, col4, col5, col6 = (
            st.columns([1, 2, 2, 2, 3, 2])
        )

        with col1:
            st.write(i)

        with col2:
            st.write(
                f"Semester "
                f"{result['semester']}"
            )

        with col3:
            st.write(result["session"])

        with col4:
            st.write(
                result["downloads"]
            )

        with col5:

            if result[
                "last_downloaded"
            ]:

                st.write(
                    result[
                        "last_downloaded"
                    ]
                )

            else:

                st.write("-")

        with col6:

            pdf_bytes = download_pdf(
                result["filepath"]
            )

            if st.download_button(
                label="Download",
                data=pdf_bytes,
                file_name=result["filename"],
                mime="application/pdf",
                key=result["filepath"]
            ):

                increment_download_counter(
                    result["resid"],
                    result["downloads"]
                )

                st.rerun()

def upload_document_page():
    
    st.title(
        "Upload Student Application"
    )

    enrollment = (
        st.session_state
        .student["enrollment"]
    )

    document_types = (
        get_document_types()
    )

    selected_doc = st.selectbox(
        "Select Document Type",

        document_types,

        format_func=lambda x:
            x["doc_type_name"]
    )

    uploaded_file = st.file_uploader(
        "Upload PDF",

        type=["pdf"]
    )

    st.caption(
        "Maximum file size: 5 MB"
    )

    if uploaded_file:

        file_size_mb = (
            uploaded_file.size
            / (1024 * 1024)
        )

        if file_size_mb > 5:

            st.error(
                "File size exceeds 5 MB."
            )

            return

    if st.button(
        "Upload Document"
    ):

        if not uploaded_file:

            st.error(
                "Please upload a PDF."
            )

            return

        result = upload_student_document(
            enrollment,
            selected_doc,
            uploaded_file
        )

        if result["success"]:

            st.success(
                result["message"]
            )

        else:

            st.error(
                result["message"]
            )

        st.success(
            "Document uploaded successfully."
        )

def dashboard():

    st.sidebar.title("Menu")

    menu = st.sidebar.radio(
        "Select Option",
        [
            "Download Marksheets",
            "Upload Document",
            "Logout",
        ],
    )

    if menu == "Download Marksheets":

        download_results_page()

    elif menu == "Upload Document":
        upload_document_page()
        
    elif menu == "Logout":

        logout()


if st.session_state.logged_in:

    dashboard()

else:

    login_page()