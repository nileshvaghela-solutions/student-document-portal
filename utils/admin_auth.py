from utils.db import supabase


def admin_login(
    email,
    password
):

    response = (
        supabase.table("admins")
        .select("*")
        .eq("email", email)
        .eq("password", password)
        .eq("is_active", True)
        .execute()
    )

    if response.data:

        return response.data[0]

    return None