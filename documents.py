import streamlit as st

from utils.document_helper import (
    get_student_document_summary,
    get_student_documents,
    download_document
)


def show_documents():

    st.header(
        "View Student Documents"
    )

    enrollment = st.text_input(
        "Enter Enrollment Number",
        key="document_enrollment"
    )

    # ---------------- SEARCH ---------------- #

    if st.button(
        "Search Documents"
    ):

        st.session_state[
            "searched_enrollment"
        ] = enrollment

        # reset old selection
        if (
            "selected_doc_type"
            in st.session_state
        ):

            del st.session_state[
                "selected_doc_type"
            ]

    # ---------------- RESULTS ---------------- #

    if (
        "searched_enrollment"
        in st.session_state
    ):

        enrollment = (
            st.session_state[
                "searched_enrollment"
            ]
        )

        summary = (
            get_student_document_summary(
                enrollment
            )
        )

        documents = (
            get_student_documents(
                enrollment
            )
        )

        if not summary:

            st.warning(
                "No documents found."
            )

        else:
            left_col, space_col, right_col = st.columns([1, 0.08, 1.4])
            with left_col:

                summary_box = st.container(
                    border=True
                )

                with summary_box:
            
            
            # ---------------- SUMMARY TABLE ---------------- #

                    st.subheader(
                        "Document Summary"
                    )

                    headers = st.columns(
                        #[1, 4, 3, 2, 2]
                        [1, 4, 2, 2]
                    )

                    headers[0].markdown(
                        "**S#**"
                    )

                    headers[1].markdown(
                        "**Document Type**"
                    )

                    #headers[2].markdown(
                    #    "**Short Code**"
                    #)

                    headers[2].markdown(
                        "**Count**"
                    )

                    headers[3].markdown(
                        "**Action**"
                    )

                    for row in summary:

                        cols = st.columns(
                            [1, 4, 2, 2]
                        )

                        cols[0].write(
                            row["S#"]
                        )

                        cols[1].write(
                            row["Document Type"]
                        )

                        #cols[2].write(
                        #    row["short_code"]
                        #)

                        cols[2].write(
                            row["Count"]
                        )

                        button_key = (
                            f"view_doc_"
                            f"{row['short_code']}"
                        )

                        if cols[3].button(
                            "View",
                            key=button_key
                        ):

                            st.session_state[
                                "selected_doc_type"
                            ] = (
                                row["short_code"]
                            )

            # ---------------- DOCUMENT DETAILS ---------------- #
            with right_col:

                details_box = st.container(
                    border=True
                )

                with details_box:
                    if (
                        "selected_doc_type"
                        in st.session_state
                    ):

                        selected = (
                            st.session_state[
                                "selected_doc_type"
                            ]
                        )

                        filtered_docs = [

                            d for d in documents

                            if (
                                d["short_code"]
                                == selected
                            )
                        ]

                        st.subheader(
                            f"Documents - "
                            f"{selected}"
                        )

                        headers = st.columns(
                            #[1, 2, 4, 2]
                            [1, 2, 2]
                        )

                        headers[0].markdown(
                            "**S#**"
                        )

                        headers[1].markdown(
                            "**Upload Date**"
                        )

                        #headers[2].markdown(
                        #    "**Document Type**"
                        #)

                        headers[2].markdown(
                            "**Download**"
                        )

                        for doc in filtered_docs:

                            cols = st.columns(
                                #[1, 2, 4, 2]
                                [1, 2, 2]
                            )

                            cols[0].write(
                                doc["S#"]
                            )

                            cols[1].write(
                                doc["Upload Date"]
                            )

                            #cols[2].write(
                            #    doc["Document Type"]
                            #)

                            pdf_bytes = (
                                download_document(

                                    doc["filepath"],

                                    bucket=
                                        "student-documents"
                                )
                            )

                            cols[2].download_button(

                                label="Download",

                                data=pdf_bytes,

                                file_name=
                                    doc["filename"],

                                mime=
                                    "application/pdf",

                                key=
                                    f"doc_"
                                    f"{doc['filename']}",

                                on_click="ignore"
                            )