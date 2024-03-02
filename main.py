import pytesseract
import re
import cv2
from datetime import datetime as dt
import os.path
import conversion as cnvs

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


#Image input
image_path = 'data/workschedule.jpg'
img = cv2.imread(image_path)

#Dictionary to store all 
shifts_dict = {}

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Use pytesseract to perform OCR on the grayscale image
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(gray, config=custom_config)

# Split the OCR output into words
words = text.split()

# Initialize variables to track the current date, start time, and end time
current_date = None
current_start_time = None
current_end_time = None

# Combine relevant components
combined_times = []
current_time = ""
for word in words:
    #print(word)
    if not re.match(r'\d{1,2}/\d{1,2}', word) and any(char.isdigit() for char in word) or word.lower() in ["a.m.", "p.m."]:
        current_time += word
    else:
        if current_time:
            combined_times.append(current_time.strip())
            current_time = ""
    if re.match(r'\d{1,2}/\d{1,2}', word):
        combined_times.append(word)

#print(combined_times)

for time in combined_times:
    if not re.match(r'\d{1,2}/\d{1,2}', time):
        if not current_start_time:
            current_start_time = time
        else:
            current_end_time = time
    else:
        current_date = time + "/2024"
        shifts_dict[cnvs.convert_date(current_date)] = cnvs.convert_time(current_start_time), cnvs.convert_time(current_end_time)

        current_start_time = None
        current_end_time = None


#GOOGLE API

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
    
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        for date,time in zip(shifts_dict.keys(), shifts_dict.values()):
            if time[0] and time[1] != None:
                event = {
                    'summary': 'Cashier',
                    'location': 'Publix Super Market at Lake Ella Plaza, 1700 N Monroe St, Tallahassee, FL 32303, USA',
                    'description': 'Break: ',
                    'start': {
                        'dateTime' : f'{date}T{time[0]}:00',
                        'timeZone' : 'GMT-5:00'
                    },
                    'end': {
                        'dateTime' : f'{date}T{time[1]}:00',
                        'timeZone' : 'GMT-5:00'
                    }
                }
                event = service.events().insert(calendarId='85r1j11m1vc3983imhkpi44j1c@group.calendar.google.com', body=event).execute()
                print('Event created')

    except HttpError as error:
        print("An error occurerd: ", error)
main()