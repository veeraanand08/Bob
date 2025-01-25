from database import get_database
dbname = get_database()
collection_name = dbname["bobData"]

#string format:
# Busy Hours: dayOfTheWeek.times (as in like 1-2;3-6;15-20),
# assessmentHours: name.dateDue.hoursNeeded.timeperdate.dates (as in like 11/1/24-11/2/24-11/3/24...).content,name.date.hours
# assignmentHours: name.datedue.hoursNeeded.timeperdate.dates (as in like 11/1/24-11/2/24-11/3/24...),next assignment
# Quizzes (only for test/quizzes): name,Q1) blah blah blah,Q1ANSWER) blah blah blah,Q2) blah blah blah,...
# ExtraTimeUsed: date.timmes (as in like 1-2;3-6;15-20 from the assesments or assignments)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/save_user_data', methods=['POST'])
def save_user_data():
    # Get data from the frontend
    data = request.get_json()
    new_user = data.get('bool_user')
    user_email = data.get('email')
    user_name = data.get('name')
    google_id = data.get('googleId')

    return new_user, google_id, user_email, user_name        

if __name__ == '__main__':
    app.run(debug=True)


def insertStartData(): #inserts data from client of either assignment, test/quiz, project, or not available time for some google user ID
    b, id, e, n = save_user_data
    item = {
    "google_id" : id,
    "email" : e,
    "name" : n,
    "assessmentHours" : "NONE",
    "assignmentHours" : "NONE",
    "quizzes" : "NONE",
    }
    if b:
        collection_name.insert_one(item)



