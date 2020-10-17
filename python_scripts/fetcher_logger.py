from __future__ import print_function
import datetime
import dateutil.parser
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
import sys

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main(days_prior=None, print_visible=True, target_calendar=None):
    """Script for logging all google calendar events on a specified day.

    Usage Examples
    -----
    python3 fetcher_logger.py
    Logs all google calendar events from yesterday whose start and end times are between 00:00 and 23:59.

    python3 fetcher_logger.py n
    Logs all google calendar events from `n` days ago whose start and end times are between 00:00 and 23:59.

    References
    ----------
    [1] https://dev.to/scriptingwithpy/create-a-csv-of-yesterdays-google-calendar-events-dgm
    [2] https://developers.google.com/calendar/quickstart/python#further_reading
    [3] https://developers.google.com/calendar/v3/reference/events/list
    """

    # Fetcher:
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Get a list of all my Google Calendars
    page_token = None
    calendar_list = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    # Set up Logger
    # using the keyword `with` means the .csv will automatically close
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    day_to_log = None
    if days_prior is None:
        if len(sys.argv) == 1:
            # by default, we log all of yesterday's events
            days_prior = 1
        elif len(sys.argv) == 2:
            days_prior = int(sys.argv[1])
        else:
            print('Invalid combination or number of CLI arguments. No calendar data pulled. Exiting script.')
            sys.exit()

    day_to_log = today - datetime.timedelta(days=days_prior)
    time_tracking_file = day_to_log.isoformat()
    with open(f'/home/mhtl/Projects/automated-timetracking/' +
              f'timetracking_data/{time_tracking_file}.csv', 'w') as f:
        # Start CSV heading
        new_row = f'start,end,summary,calendar\n'
        f.write(new_row)

        # Call the Calendar API
        timezone_offset = '-04:00'  # because of Toronto timezone with respect to UTC
        day_logged = None
        if len(sys.argv) == 1:
            day_logged = 'yesterday'
        else:
            day_logged = day_to_log.strftime('%A, %B %d, %Y')
        if print_visible:
            print(f'Getting all visible events from {day_logged}.')

        calendar_list['items'] = [c for c in calendar_list['items'] if 'selected' in c.keys()]
        calendar_list['items'].sort(key=lambda c: c.get('summary', ''))
        for counter, calendar_list_entry in enumerate(calendar_list['items']):
            if print_visible:
                print(f'{counter+1} out of {len(calendar_list["items"])} calendars appended. ' +
                      f'Calendar Name: {calendar_list_entry["summary"]}')
            events_result = service.events().list(calendarId=calendar_list_entry['id'],
                                                  timeMin=day_to_log.isoformat() + timezone_offset,
                                                  timeMax=today.isoformat() + timezone_offset,
                                                  maxResults=2500, singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

            # Add to CSV via Logger
            if not events:
                pass
                # print('No events from requested day found.')
            else:
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    end = event['end'].get('dateTime', event['end'].get('date'))
                    # swap commas with semi-colons so values don't get misinterpreted as different fields
                    summary = event.get("summary", '').replace(',', ';')
                    calendar = calendar_list_entry.get("summary", '').replace(',', ';')
                    new_row = f'{start},{end},{summary},{calendar}\n'
                    f.write(new_row)
        if print_visible:
            print(f'Done logging to {time_tracking_file}.csv!')
            print(f'Logging completed at {datetime.datetime.today().strftime("%I:%M%p, %A, %B %d, %Y")}')


if __name__ == '__main__':
    main()
