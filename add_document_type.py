import streamlit as st

from utils.document_type_helper import (

    get_all_document_types,

    add_document_type,

    update_document_type
)


def show_add_document_type():

    st.header(
        "Add Document Type"
    )

    # ==============================
    # ADD NEW TYPE
    # ==============================

    with st.container(border=True):

        st.subheader(
            "New Document Type"
        )

        new_name = st.text_input(
            "Document Type Name",
            key="new_doc_name"
        )

        new_code = st.text_input(
            "Short Code",
            key="new_short_code"
        )

        if st.button(
            "Add Document Type"
        ):

            result = add_document_type(
                new_name,
                new_code
            )

            if result["success"]:

                st.success(
                    result["message"]
                )

                st.rerun()

            else:

                st.error(
                    result["message"]
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==============================
    # LAYOUT
    # ==============================

    left_col, space_col, right_col = st.columns(
        [1.4, 0.04, 1.1]
    )

    # ==============================
    # LEFT SIDE LIST
    # ==============================

    with left_col:

        with st.container(border=True):

            st.subheader(
                "Available Document Types"
            )

            all_types = (
                get_all_document_types()
            )

            headers = st.columns(
                [1, 4, 3, 2]
            )

            headers[0].markdown(
                "**S#**"
            )

            headers[1].markdown(
                "**Document Type**"
            )

            headers[2].markdown(
                "**Short Code**"
            )

            headers[3].markdown(
                "**Action**"
            )

            for index, row in enumerate(
                all_types,
                start=1
            ):

                cols = st.columns(
                    [1, 4, 3, 2]
                )

                cols[0].write(index)

                cols[1].write(
                    row["doc_type_name"]
                )

                cols[2].write(
                    row["short_code"]
                )

                if cols[3].button(
                    "Edit",
                    key=f"edit_{row['doc_type_id']}"
                ):

                    st.session_state[
                        "selected_doc_type"
                    ] = row

    # ==============================
    # RIGHT SIDE EDIT PANEL
    # ==============================

    with right_col:

        if (
            "selected_doc_type"
            in st.session_state
        ):

            selected = (
                st.session_state[
                    "selected_doc_type"
                ]
            )

            with st.container(border=True):

                st.subheader(
                    "Edit Document Type"
                )

                edit_name = st.text_input(
                    "Document Type Name",
                    value=selected[
                        "doc_type_name"
                    ],
                    key="edit_doc_name"
                )

                edit_code = st.text_input(
                    "Short Code",
                    value=selected[
                        "short_code"
                    ],
                    key="edit_short_code"
                )

                if st.button(
                    "Update Document Type"
                ):

                    result = update_document_type(

                        selected[
                            "doc_type_id"
                        ],

                        edit_name,

                        edit_code
                    )

                    if result["success"]:

                        st.success(
                            result["message"]
                        )

                        del st.session_state[
                            "selected_doc_type"
                        ]

                        st.rerun()

                    else:

                        st.error(
                            result["message"]
                        )