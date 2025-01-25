from database import get_database
dbname = get_database()
collection_name = dbname["bobData"]

def updateData(google_id, update_fields):
    # Example: update_fields = {"name": "New Name", "busyHours": "Updated Hours"}
    collection_name.update_one(
        {"google_id": google_id},  # Filter to find the document by google_id
        {"$set": update_fields}    # Updates the specified fields
    )


def fetchUpdates(google_id):
    #gather data from jibreel here
    #format here
    updateData(
    google_id,
    update_fields={
        "assessmentHours": "",
        "assignmentHours": "",
        "quizzes": ""
    }
)