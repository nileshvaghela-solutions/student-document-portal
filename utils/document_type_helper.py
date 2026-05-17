from utils.db import supabase


# -----------------------------
# GET ALL DOCUMENT TYPES
# -----------------------------
def get_all_document_types():

    response = (
        supabase.table(
            "doc_types"
        )
        .select("*")
        .order(
            "doc_type_name"
        )
        .execute()
    )

    return response.data


# -----------------------------
# CHECK DUPLICATE
# -----------------------------
def check_duplicate_document_type(
    doc_type_name,
    short_code,
    exclude_id=None
):

    query = (
        supabase.table(
            "doc_types"
        )
        .select("*")
    )

    response = query.execute()

    for row in response.data:

        # skip current editing row
        if (
            exclude_id
            and
            row["doc_type_id"] == exclude_id
        ):
            continue

        if (
            row["doc_type_name"]
            .strip()
            .lower()
            ==
            doc_type_name
            .strip()
            .lower()
        ):

            return {
                "success": False,
                "message":
                    "Document type name already exists."
            }

        if (
            row["short_code"]
            .strip()
            .lower()
            ==
            short_code
            .strip()
            .lower()
        ):

            return {
                "success": False,
                "message":
                    "Short code already exists."
            }

    return {
        "success": True
    }


# -----------------------------
# ADD DOCUMENT TYPE
# -----------------------------
def add_document_type(
    doc_type_name,
    short_code
):

    doc_type_name = (
        doc_type_name.strip()
    )

    short_code = (
        short_code
        .strip()
        .lower()
    )

    # blank validation
    if not doc_type_name:

        return {
            "success": False,
            "message":
                "Document type name cannot be blank."
        }

    if not short_code:

        return {
            "success": False,
            "message":
                "Short code cannot be blank."
        }

    # duplicate validation
    duplicate = (
        check_duplicate_document_type(
            doc_type_name,
            short_code
        )
    )

    if not duplicate["success"]:

        return duplicate

    supabase.table(
        "doc_types"
    ).insert(
        {
            "doc_type_name":
                doc_type_name,

            "short_code":
                short_code,

            "is_active":
                True
        }
    ).execute()

    return {
        "success": True,
        "message":
            "Document type added successfully."
    }


# -----------------------------
# UPDATE DOCUMENT TYPE
# -----------------------------
def update_document_type(
    doc_type_id,
    doc_type_name,
    short_code
):

    doc_type_name = (
        doc_type_name.strip()
    )

    short_code = (
        short_code
        .strip()
        .lower()
    )

    # blank validation
    if not doc_type_name:

        return {
            "success": False,
            "message":
                "Document type name cannot be blank."
        }

    if not short_code:

        return {
            "success": False,
            "message":
                "Short code cannot be blank."
        }

    # duplicate validation
    duplicate = (
        check_duplicate_document_type(
            doc_type_name,
            short_code,
            exclude_id=doc_type_id
        )
    )

    if not duplicate["success"]:

        return duplicate

    supabase.table(
        "doc_types"
    ).update(
        {
            "doc_type_name":
                doc_type_name,

            "short_code":
                short_code
        }
    ).eq(
        "doc_type_id",
        doc_type_id
    ).execute()

    return {
        "success": True,
        "message":
            "Document type updated successfully."
    }