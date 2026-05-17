import re
from utils.db import supabase


# -----------------------------
# GET ALL ADMINS
# -----------------------------
def get_all_admins():

    response = (
        supabase.table(
            "admins"
        )
        .select("*")
        .order(
            "admin_name"
        )
        .execute()
    )

    return response.data

# -----------------------------
# VALIDATE EMAIL
# -----------------------------
def is_valid_email(email):

    pattern = (
        r"^[a-zA-Z0-9._%+-]+"
        r"@[a-zA-Z0-9.-]+"
        r"\.[a-zA-Z]{2,}$"
    )

    return re.match(
        pattern,
        email
    )

# -----------------------------
# CHECK DUPLICATE EMAIL
# -----------------------------
def check_duplicate_email(
    email,
    exclude_id=None
):

    response = (
        supabase.table(
            "admins"
        )
        .select("*")
        .execute()
    )

    for row in response.data:

        # skip current editing row
        if (
            exclude_id
            and
            row["admin_id"] == exclude_id
        ):
            continue

        if (
            row["email"]
            .strip()
            .lower()
            ==
            email
            .strip()
            .lower()
        ):

            return {
                "success": False,
                "message":
                    "Email already exists."
            }

    return {
        "success": True
    }


# -----------------------------
# ADD ADMIN
# -----------------------------
def add_admin(
    admin_name,
    email,
    password
):

    admin_name = (
        admin_name.strip()
    )

    email = (
        email.strip()
        .lower()
    )

    password = (
        password.strip()
    )

    # blank validations

    if not admin_name:

        return {
            "success": False,
            "message":
                "Admin name cannot be blank."
        }

    if not email:

        return {
            "success": False,
            "message":
                "Email cannot be blank."
        }

    if not password:

        return {
            "success": False,
            "message":
                "Password cannot be blank."
        }
    # email validation

    if not is_valid_email(email):

        return {
            "success": False,
            "message":
                "Invalid email format."
        }
    # duplicate email

    duplicate = (
        check_duplicate_email(
            email
        )
    )

    if not duplicate["success"]:

        return duplicate

    supabase.table(
        "admins"
    ).insert(
        {
            "admin_name":
                admin_name,

            "email":
                email,

            "password":
                password,

            "admin_type":
                "Admin",

            "is_active":
                True
        }
    ).execute()

    return {
        "success": True,
        "message":
            "Admin added successfully."
    }


# -----------------------------
# UPDATE ADMIN
# -----------------------------
def update_admin(
    admin_id,
    admin_name,
    email,
    password
):

    admin_name = (
        admin_name.strip()
    )

    email = (
        email.strip()
        .lower()
    )

    password = (
        password.strip()
    )

    # blank validations

    if not admin_name:

        return {
            "success": False,
            "message":
                "Admin name cannot be blank."
        }

    if not email:

        return {
            "success": False,
            "message":
                "Email cannot be blank."
        }

    if not password:

        return {
            "success": False,
            "message":
                "Password cannot be blank."
        }

    # email validation

    if not is_valid_email(email):

        return {
            "success": False,
            "message":
                "Invalid email format."
        }
    
    # duplicate email

    duplicate = (
        check_duplicate_email(
            email,
            exclude_id=admin_id
        )
    )

    if not duplicate["success"]:

        return duplicate

    supabase.table(
        "admins"
    ).update(
        {
            "admin_name":
                admin_name,

            "email":
                email,

            "password":
                password
        }
    ).eq(
        "admin_id",
        admin_id
    ).execute()

    return {
        "success": True,
        "message":
            "Admin updated successfully."
    }