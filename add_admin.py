import streamlit as st

from utils.admin_management_helper import (

    get_all_admins,

    add_admin,

    update_admin
)


def show_add_admin():

    st.header(
        "Add Admin"
    )

    # ==============================
    # ADD ADMIN
    # ==============================

    with st.container(border=True):

        st.subheader(
            "New Admin"
        )

        new_name = st.text_input(
            "Admin Name",
            key="new_admin_name"
        )

        new_email = st.text_input(
            "Email",
            key="new_admin_email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            key="new_admin_password"
        )

        if st.button(
            "Add Admin"
        ):

            result = add_admin(
                new_name,
                new_email,
                new_password
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
        [1, 0.04, 1.4]
    )

    # ==============================
    # ADMIN LIST
    # ==============================

    with left_col:

        with st.container(border=True):

            st.subheader(
                "Available Admins"
            )

            admins = (
                get_all_admins()
            )

            headers = st.columns(
                [1, 4, 2]
            )

            headers[0].markdown(
                "**S#**"
            )

            headers[1].markdown(
                "**Admin Name**"
            )

            headers[2].markdown(
                "**Action**"
            )

            for index, row in enumerate(
                admins,
                start=1
            ):

                cols = st.columns(
                    [1, 4, 2]
                )

                cols[0].write(index)

                cols[1].write(
                    row["admin_name"]
                )

                if cols[2].button(
                    "Edit",
                    key=f"edit_admin_{row['admin_id']}"
                ):

                    st.session_state[
                        "selected_admin"
                    ] = row

                    # reset cached edit fields

                    st.session_state[
                        "edit_admin_name"
                    ] = row["admin_name"]

                    st.session_state[
                        "edit_admin_email"
                    ] = row["email"]

                    st.session_state[
                        "edit_admin_password"
                    ] = row["password"]

                    st.rerun()
    # ==============================
    # EDIT PANEL
    # ==============================

    with right_col:

        if (
            "selected_admin"
            in st.session_state
        ):

            selected = (
                st.session_state[
                    "selected_admin"
                ]
            )

            with st.container(border=True):

                st.subheader(
                    "Edit Admin"
                )

                edit_name = st.text_input(
                    "Admin Name",
                    key="edit_admin_name"
                )

                edit_email = st.text_input(
                    "Email",
                    key="edit_admin_email"
                )

                edit_password = st.text_input(
                    "Password",
                    type="password",
                    key="edit_admin_password"
                )

                if st.button(
                    "Update Admin"
                ):

                    result = update_admin(

                        selected[
                            "admin_id"
                        ],

                        edit_name,

                        edit_email,

                        edit_password
                    )

                    if result["success"]:
                        st.session_state["new_admin_name"] = ""

                        st.session_state["new_admin_email"] = ""

                        st.session_state["new_admin_password"] = ""
                        
                        st.success(
                            result["message"]
                        )

                        del st.session_state[
                            "selected_admin"
                        ]

                        st.rerun()

                    else:

                        st.error(
                            result["message"]
                        )