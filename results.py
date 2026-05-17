import streamlit as st

from utils.result_helper import (
    get_result_summary
)

from utils.document_helper import (
    download_document
)

from utils.helpers import (
    get_student_marksheets
)


def show_results():

    st.header("View Result Downloads")

    enrollment = st.text_input(
        "Enter Enrollment Number",
        key="result_enrollment"
    )

    if st.button("Search Results"):

        st.session_state["result_search"] = enrollment

        # reset old selection
        if "selected_semester" in st.session_state:
            del st.session_state["selected_semester"]

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

                button_key = (
                    f"view_"
                    f"{row['Semester Folder']}"
                )

                if cols[3].button(
                    "View",
                    key=button_key
                ):

                    st.session_state[
                        "selected_semester"
                    ] = (
                        row["Semester Folder"]
                    )

            # ---------------- DETAILS ---------------- #

            if (
                "selected_semester"
                in st.session_state
            ):

                semester_folder = (
                    st.session_state[
                        "selected_semester"
                    ]
                )

                st.subheader(
                    f"Marksheets - "
                    f"{semester_folder.upper()}"
                )

                results = (
                    get_student_marksheets(
                        enrollment,
                        semester_folder
                    )
                )

                headers = st.columns(
                    [1, 2, 2, 2, 2]
                )

                headers[0].markdown("**S#**")
                headers[1].markdown("**Session**")
                headers[2].markdown("**Downloads**")
                headers[3].markdown("**Last Downloaded**")
                headers[4].markdown("**Download**")

                for index, result in enumerate(
                    results,
                    start=1
                ):

                    cols = st.columns(
                        [1, 2, 2, 2, 2]
                    )

                    cols[0].write(index)

                    cols[1].write(
                        result["session"]
                    )

                    cols[2].write(
                        result["downloads"]
                    )

                    cols[3].write(
                        result["last_downloaded"]
                    )

                    pdf_bytes = (
                        download_document(
                            result["filepath"],
                            bucket="results"
                        )
                    )

                    cols[4].download_button(

                        label="Download",

                        data=pdf_bytes,

                        file_name=
                            result["filename"],

                        mime=
                            "application/pdf",

                        key=
                            f"result_"
                            f"{result['filename']}",
                        
                        on_click="ignore"
                    )