from __future__ import print_function

import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from oauth2client.service_account import ServiceAccountCredentials

from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
path = 'C://Users//Administrator//Desktop//Scripts//Google Calendar//'
SERVICE_ACCOUNT_FILE = path+'credentials.json'


def main(mail, num_eventi, time_min, time_max):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming events for: ' + mail)
        events_result = service.events().list(calendarId = mail,
                                              maxResults = num_eventi,
                                              timeMin = time_min,
                                              timeMax = time_max,
                                              singleEvents = 1
                                              ).execute() #singleEvents per splittare eventi ripetuti
        # calendars_result = service.calendarList().list().execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
            return

    except HttpError as error:
        print('An error occurred: %s' % error)
    
    return events
    
if __name__ == '__main__':
    main()