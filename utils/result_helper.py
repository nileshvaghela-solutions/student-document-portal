from utils.helpers import (
    get_student_marksheets
)


def get_result_summary(
    enrollment
):

    enrollment = (
        enrollment
        .strip()
        .upper()
    )

    summary = []

    counter = 1

    for sem in range(1, 7):

        semester_folder = (
            f"sem{sem}"
        )

        results = (
            get_student_marksheets(
                enrollment,
                semester_folder
            )
        )

        if results:

            summary.append(
                {
                    "S#":
                        counter,

                    "Semester":
                        semester_folder,

                    "Semester Folder":
                        semester_folder,

                    "Count":
                        len(results),
                }
            )

            counter += 1

    return summary