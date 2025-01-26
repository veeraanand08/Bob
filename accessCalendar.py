from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request




def get_free_times(calendar_service, start_date, end_date):
    events_result = calendar_service.events().list(
        calendarId='veera.anand08@gmail.com',
        timeMin=start_date,
        timeMax=end_date,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    free_times = []
    sleep_start = datetime.strptime("22:30", "%H:%M").time()
    sleep_end = datetime.strptime("07:00", "%H:%M").time()
    period_start = datetime.fromisoformat(start_date[:-1])
    period_end = datetime.fromisoformat(end_date[:-1])
    current_time = period_start

    for event in events:
        event_start = datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))
        event_end = datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date')))

        if current_time < event_start:
            free_start = max(current_time, datetime.combine(event_start.date(), sleep_end))
            free_end = min(event_start, datetime.combine(event_start.date(), sleep_start))
            if free_start < free_end:
                free_times.append((free_start.isoformat(), free_end.isoformat()))

        current_time = max(current_time, event_end)

    if current_time < period_end:
        free_start = max(current_time, datetime.combine(period_end.date(), sleep_end))
        free_end = min(period_end, datetime.combine(period_end.date(), sleep_start))
        if free_start < free_end:
            free_times.append((free_start.isoformat(), free_end.isoformat()))

    return free_times

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file(
    "C:/Users/jchoh/Downloads/client_secret_375024145336-9441tkreviiiknfeul3e11f51e42ecje.apps.googleusercontent.com.json",  SCOPES)
credentials = flow.run_local_server(port=0)

calendar_service = build('calendar', 'v3', credentials=credentials)

free_times = get_free_times(
    calendar_service=calendar_service,
    start_date='2025-01-26T00:00:00Z',
    end_date='2025-01-27T23:59:59Z'
)

for start, end in free_times:
    print(f"Free time from {start} to {end}")
