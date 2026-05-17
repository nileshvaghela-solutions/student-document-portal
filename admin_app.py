import streamlit as st
from utils.admin_auth import admin_login
from results import show_results
from documents import show_documents

st.set_page_config(
    page_title="Admin Portal",
    page_icon="🔐",
    layout="wide"
)

# ---------------- LOGIN ---------------- #
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


# ---------------- LOGOUT ---------------- #
def logout():

    if "admin" in st.session_state:
        del st.session_state["admin"]

    st.rerun()


# ---------------- DASHBOARD ---------------- #
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

    # ---------------- ROUTING ONLY ---------------- #

    if menu == "View Student Documents":
        show_documents()

    elif menu == "View Result Downloads":
        show_results()

    elif menu == "Add Document Type":
        st.header("Add Document Type")

    elif menu == "Add Admin":
        st.header("Add Admin")

    elif menu == "Logout":
        logout()


# ---------------- APP START ---------------- #
if "admin" not in st.session_state:
    login_page()
else:
    dashboard()