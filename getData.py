from database import get_database
import csv
import datetime
dbname = get_database()
collection_name = dbname["bobData"]


def getFieldValue(google_id, field):
    # Use projection to retrieve only the specified field
    query = {"google_id": google_id}
    projection = {field: 1, "_id": 0}  # Include only the desired field
    result = collection_name.find_one(query, projection)
    return result.get(field)  # Return the value of the field


# assessmentHours: name.dateDue.hoursNeeded.timeperdate.dates (as in like 11/1/24-11/2/24-11/3/24...).content,name.date.hours
# assignmentHours: name.datedue.hoursNeeded.timeperdate.dates (as in like 11/1/24-11/2/24-11/3/24...),next assignment
# Quizzes (only for test/quizzes): name,Q1) blah blah blah,Q1ANSWER) blah blah blah,Q2) blah blah blah,...


def getAssessmentHours(google_id):
    assessment_hours = getFieldValue(google_id="---", field="assessmentHours")
    result = []

    # Split the input string into individual entries by commas
    entries = assessment_hours.split(',')

    for entry in entries:
        # Split the entry into its parts
        parts = entry.split('.')
        name, date_due, hours_needed, time_per_date, dates, content = parts

        # Format
        dates_list = dates.split('-')
        entry_result = {
            "name": name.strip(),
            "dateDue": date_due.strip(),
            "hoursNeeded": hours_needed.strip(),
            "timePerDate": time_per_date.strip(),
            "dates": [date.strip() for date in dates_list],
            "content": content.strip()
        }
        result.append(entry_result)

    return result


def getAssignmentHours(google_id):
    assignment_hours = getFieldValue(google_id="---", field="assignmentHours")
    result = []

    # Split the input string into individual entries by commas
    entries = assignment_hours.split(',')

    for entry in entries:
        # Split the entry into its parts
        parts = entry.split('.')
        name, date_due, hours_needed, time_per_date, dates, content = parts

        # Format
        dates_list = dates.split('-')
        entry_result = {
            "name": name.strip(),
            "dateDue": date_due.strip(),
            "hoursNeeded": hours_needed.strip(),
            "timePerDate": time_per_date.strip(),
            "dates": [date.strip() for date in dates_list],
        }
        result.append(entry_result)

    return result
