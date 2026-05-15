from utils.db import supabase


def login_user(enrollment, password):

    response = (
        supabase.table("students")
        .select("*")
        .eq("enrollment", enrollment)
        .eq("password_hash", password)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None