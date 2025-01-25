import google.generativeai as genai
import os
import requests  
from datetime import datetime, timedelta

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))



def scrape_resources(topics):
    resources = {}
    for topic in topics:
        
        response = requests.get(f"https://api.webscraping.com/{topic}")
        resources[topic] = response.content  # Assuming JSON response
    return resources

def split_study_sessions(test_date, available, totalHours):
    
    total_minutes = totalHours * 60

    test_date_datetime = test_date

    # Calculate the maximum number of sessions based on days between today and the test date
    today = datetime.today()
    days_until_test = max((test_date_datetime - today.date()).days, 1)
    max_sessions = min(len(available), days_until_test)

    time_per_session = total_minutes // max_sessions

    study_sessions = []
    remaining_minutes = total_minutes

    # Distribute sessions across the available slots
    for i, slot in enumerate(available):
        if remaining_minutes <= 0 or len(study_sessions) >= max_sessions:
            break

        # Parse the slot into start and end times
        date_part, time_part = slot.split("T")
        start_time, end_time = time_part.split("-")
        start_datetime = datetime.strptime(f"{date_part}T{start_time}", "%Y-%m-%dT%H:%M")
        end_datetime = datetime.strptime(f"{date_part}T{end_time}", "%Y-%m-%dT%H:%M")

        # Ensure the slot is before the test date
        if start_datetime.date() >= test_date_datetime:
            continue

        # Calculate available minutes in the slot
        available_minutes = int((end_datetime - start_datetime).total_seconds() // 60)

        # Determine the study time for this slot
        study_time = min(remaining_minutes, available_minutes, time_per_session)

        # Skip very short sessions (e.g., less than 15 minutes)
        if study_time < 15:
            continue

        # Calculate end time for the study session
        session_end_datetime = start_datetime + timedelta(minutes=study_time)
        study_sessions.append(
            f"{start_datetime.strftime('%Y-%m-%dT%H:%M')}" +
            f"-{session_end_datetime.strftime('%H:%M')}"
        )

        # Decrease the remaining study time
        remaining_minutes -= study_time

    return study_sessions
    
def generate_study_plan(test_date, sessions, topics, resources):
    
    try:
        # Configure the model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="You are a helpful assistant. Create a study plan based on user input."
        )

        # Create the prompt
        prompt = f"Generate a study plan for the following topics: {topics}. The test is on {test_date}. Sessions are {sessions}. The plan is meant to be implemented with the Google Calendar API so each session should have the exact format (should add nothing extra than) of Date YYYY-MM-2DDTSTARTTIME-ENDTIME (use military time, example: 09:00-13:00)  followed by Description: (insert text)"

        # Generate the content
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.7
            )
        )

        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Inputs
test_date = datetime(2025, 1, 30).date()
calendar_sessions = [
    "2025-01-26T14:35-19:35",
    "2025-01-27T16:00-18:00",
    "2025-01-27T19:00-23:00",
    "2025-01-29T10:00-11:00"
    ]
study_guide = ["U-sub integration", "reimann sums", "definite integrals", "area between curves"]
hours = 5

# Workflow
resources = scrape_resources(study_guide)
sessions = split_study_sessions(test_date, calendar_sessions,  hours)
study_plan = generate_study_plan(test_date, sessions, study_guide, resources)

# Output
print(study_plan)
