import streamlit as st
import pandas as pd
from io import BytesIO

from utils.admin_auth import (
    admin_login
)

from utils.admin_helper import (
    get_student_document_summary,
    get_student_documents,
    download_document,
    get_result_summary
)

from utils.helpers import (
    get_student_marksheets
)

st.set_page_config(
    page_title="Admin Portal",
    page_icon="🔐",
    layout="wide"
)

st.markdown(
    """
    <style>
    .doc-row {
        border: 1px solid #666;
        padding: 8px;
        border-radius: 4px;
        margin-bottom: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def logout():

    if "admin" in st.session_state:
        del st.session_state["admin"]

    st.rerun()


def login_page():

    st.title("Admin Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        admin = admin_login(email, password)

        if admin:
            st.session_state.admin = admin
            st.rerun()
        else:
            st.error("Invalid Credentials")


def dashboard():

    admin = st.session_state.admin

    st.sidebar.title("Admin Menu")

    menu_options = [
        "View Student Documents",
        "View Result Downloads",
    ]

    if admin["admin_type"] == "Super Admin":
        menu_options.extend([
            "Add Document Type",
            "Add Admin",
        ])

    menu_options.append("Logout")

    menu = st.sidebar.radio("Select Option", menu_options)

    st.title(f"Welcome {admin['admin_name']}")

    # ---------------- DOCUMENT MODULE ---------------- #
    if menu == "View Student Documents":

        st.header("View Student Documents")

        enrollment = st.text_input(
            "Enter Enrollment Number",
            key="document_enrollment"
        )

        if st.button("Search Documents"):
            st.session_state["searched_enrollment"] = enrollment
            st.session_state.pop("selected_doc_type", None)

        if "searched_enrollment" in st.session_state:

            enrollment = st.session_state["searched_enrollment"]

            summary = get_student_document_summary(enrollment)
            documents = get_student_documents(enrollment)

            if not summary:
                st.warning("No documents found.")
            else:

                # ---------------- SUMMARY ---------------- #
                st.subheader("Document Summary")

                summary_df = pd.DataFrame(summary)
                summary_df.index = range(1, len(summary_df) + 1)
                st.table(summary_df)

                st.markdown("### Select Document Type")

                for row in summary:

                    cols = st.columns([1, 4, 2, 2])

                    cols[0].write(row["S#"])
                    cols[1].write(row["Document Type"])
                    cols[2].write(row["Count"])

                    btn_key = f"view_doc_{row['short_code']}_{row['S#']}"

                    if cols[3].button("View", key=btn_key):
                        st.session_state["selected_doc_type"] = row["short_code"]

                # ---------------- DETAIL VIEW ---------------- #
                if "selected_doc_type" in st.session_state:

                    selected = st.session_state["selected_doc_type"]

                    filtered_docs = [
                        d for d in documents
                        if d.get("short_code") == selected
                    ]

                    st.subheader("Document Details")

                    headers = st.columns([1, 2, 4, 2])
                    headers[0].markdown("**S#**")
                    headers[1].markdown("**Upload Date**")
                    headers[2].markdown("**Document Type**")
                    headers[3].markdown("**Download**")

                    st.markdown(
                        "<hr style='margin-top:0;margin-bottom:10px;border:1px solid #ccc !important;'>",
                        unsafe_allow_html=True
                    )

                    for doc in filtered_docs:

                        cols = st.columns([1, 2, 4, 2])

                        cols[0].write(doc["S#"])
                        cols[1].write(doc["Upload Date"])
                        cols[2].write(doc["Document Type"])

                        pdf_bytes = download_document(
                            doc["filepath"],
                            bucket="student_documents"
                        )

                        file_key = f"{doc['short_code']}_{doc['S#']}_{doc['filename']}"

                        cols[3].download_button(
                            "Download",
                            data=pdf_bytes,
                            file_name=doc["filename"],
                            mime="application/pdf",
                            key=file_key
                        )

    # ---------------- RESULT MODULE (UNCHANGED) ---------------- #
    elif menu == "View Result Downloads":

        st.header("View Result Downloads")

        enrollment = st.text_input(
            "Enter Enrollment Number",
            key="result_enrollment"
        )

        if st.button("Search Results"):
            st.session_state["result_search"] = enrollment

        if "result_search" in st.session_state:

            enrollment = st.session_state["result_search"]

            summary = get_result_summary(enrollment)

            if not summary:
                st.warning("No results found.")
            else:

                st.subheader("Semester Wise Summary")

                headers = st.columns([1, 3, 2, 2])
                headers[0].markdown("**S#**")
                headers[1].markdown("**Semester**")
                headers[2].markdown("**Count**")
                headers[3].markdown("**Action**")

                for row in summary:

                    cols = st.columns([1, 3, 2, 2])

                    cols[0].write(row["S#"])
                    cols[1].write(row["Semester"])
                    cols[2].write(row["Count"])

                    button_key = f"view_{row['Semester Folder']}"

                    if cols[3].button("View", key=button_key):
                        st.session_state["selected_semester"] = row["Semester Folder"]

                if "selected_semester" in st.session_state:

                    semester_folder = st.session_state["selected_semester"]

                    st.subheader(f"Marksheets - {semester_folder.upper()}")

                    results = get_student_marksheets(enrollment, semester_folder)

                    headers = st.columns([1, 2, 2, 2, 2])
                    headers[0].markdown("**S#**")
                    headers[1].markdown("**Session**")
                    headers[2].markdown("**Downloads**")
                    headers[3].markdown("**Last Downloaded**")
                    headers[4].markdown("**Download**")

                    for index, result in enumerate(results, start=1):

                        cols = st.columns([1, 2, 2, 2, 2])

                        cols[0].write(index)
                        cols[1].write(result["session"])
                        cols[2].write(result["downloads"])
                        cols[3].write(result["last_downloaded"])

                        pdf_bytes = download_document(
                            result["filepath"],
                            bucket="results"
                        )

                        cols[4].download_button(
                            label="Download",
                            data=pdf_bytes,
                            file_name=result["filename"],
                            mime="application/pdf",
                            key=f"result_{result['filename']}"
                        )

    elif menu == "Add Document Type":
        st.header("Add Document Type")

    elif menu == "Add Admin":
        st.header("Add Admin")

    elif menu == "Logout":
        logout()


if "admin" not in st.session_state:
    login_page()
else:
    dashboard()