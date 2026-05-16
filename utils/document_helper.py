from utils.db import supabase

from datetime import datetime


def get_document_types():

    response = (
        supabase.table("doc_types")
        .select("*")
        .eq("is_active", True)
        .order("doc_type_name")
        .execute()
    )

    return response.data


def get_today_upload_count(
    enrollment,
    doc_type_id
):

    today = datetime.now().strftime(
        "%d%m%Y"
    )

    response = (
        supabase.table(
            "student_documents"
        )
        .select("*")
        .eq("enrollment", enrollment)
        .eq("doc_type_id", doc_type_id)
        .eq("upload_date", today)
        .execute()
    )

    return len(response.data)


def generate_filename(
    enrollment,
    short_code,
    upload_number
):

    today = datetime.now().strftime(
        "%d%m%Y"
    )

    return (
        f"{enrollment}_"
        f"{short_code}_"
        f"{today}_"
        f"{upload_number}.pdf"
    )


def upload_student_document(
    enrollment,
    doc_type,
    uploaded_file
):

    upload_count = (
        get_today_upload_count(
            enrollment,
            doc_type["doc_type_id"]
        )
    )

    if upload_count >= 3:

        return {
            "success": False,
            "message":
                "Maximum 3 uploads "
                "allowed per day "
                "for this document type."
        }

    upload_number = (
        upload_count + 1
    )

    generated_filename = (
        generate_filename(
            enrollment,
            doc_type["short_code"],
            upload_number
        )
    )

    filepath = (
        f"{doc_type['short_code']}/"
        f"{generated_filename}"
    )

    file_bytes = uploaded_file.read()

    supabase.storage.from_(
        "student-documents"
    ).upload(
        path=filepath,
        file=file_bytes,
        file_options={
            "content-type":
                "application/pdf"
        }
    )

    supabase.table(
        "student_documents"
    ).insert(
        {
            "enrollment":
                enrollment,

            "doc_type_id":
                doc_type["doc_type_id"],

            "original_filename":
                uploaded_file.name,

            "stored_filename":
                generated_filename,

            "document_url":
                filepath,
                
            "upload_date":
                datetime.now().strftime(
                    "%d%m%Y"
            ),
        }
    ).execute()

    return {
        "success": True,
        "message":
            ""
    }