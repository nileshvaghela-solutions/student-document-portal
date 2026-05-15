from utils.db import supabase
from datetime import datetime


def get_student_marksheets(
    enrollment,
    semester_folder
):

    all_results = []

    semester_no = int(
        semester_folder.replace("sem", "")
    )

    tracking_response = (
        supabase.table("results")
        .select("*")
        .eq("enrollment", enrollment)
        .eq("semester", semester_no)
        .execute()
    )

    tracking_map = {}

    for row in tracking_response.data:

        tracking_map[
            row["result_session"]
        ] = row

    storage_response = (
        supabase.storage
        .from_("results")
        .list(semester_folder)
    )

    for file in storage_response:

        filename = file["name"]

        if filename.startswith(enrollment):

            session = (
                filename
                .replace(".pdf", "")
                .split("_")[1]
            )

            filepath = (
                f"{semester_folder}/{filename}"
            )

            if session not in tracking_map:

                insert_response = (
                    supabase.table("results")
                    .insert(
                        {
                            "enrollment":
                                enrollment,

                            "semester":
                                semester_no,

                            "result_session":
                                session,

                            "pdf_path":
                                filepath,

                            "downloadcounter":
                                0,
                        }
                    )
                    .execute()
                )

                tracking = (
                    insert_response.data[0]
                )

                tracking_map[
                    session
                ] = tracking

            tracking = tracking_map[
                session
            ]

            all_results.append(
                {
                    "resid":
                        tracking["resid"],

                    "semester":
                        semester_no,

                    "session":
                        session,

                    "filename":
                        filename,

                    "filepath":
                        filepath,

                    "downloads":
                        tracking[
                            "downloadcounter"
                        ],

                    "last_downloaded":
                        tracking[
                            "last_downloaded_at"
                        ],
                }
            )

    return sorted(
        all_results,
        key=lambda x: x["session"]
    )


def increment_download_counter(
    resid,
    current_count
):

    supabase.table("results").update(
        {
            "downloadcounter":
                current_count + 1,

            "last_downloaded_at":
                datetime.now().isoformat(),
        }
    ).eq("resid", resid).execute()


def download_pdf(filepath):

    response = (
        supabase.storage
        .from_("results")
        .download(filepath)
    )

    return response