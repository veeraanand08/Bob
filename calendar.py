from flask import Flask, request, jsonify
import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

# Define the Google API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Function to get the Google Calendar service
def get_calendar_service(credentials):
    return build('calendar', 'v3', credentials=credentials)

# Function to get events from the calendar
def get_events_from_calendar(credentials):
    service = get_calendar_service(credentials)

    # Call the Google Calendar API to fetch events
    events_result = service.events().list(calendarId='primary', timeMin='2025-01-01T00:00:00Z', singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

@app.route('/get_calendar_events', methods=['POST'])
def get_calendar_events():
    access_token = request.headers.get('Authorization').split(" ")[1]
    if not access_token:
        return jsonify({"error": "Access token missing"}), 400

    # Fetch credentials using the access token
    credentials = Credentials(token=access_token, client_id=os.environ['CLIENT_ID'], client_secret=os.environ['CLIENT_SECRET'])

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    # Fetch calendar events
    events = get_events_from_calendar(credentials)

    # Return events as JSON
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)
