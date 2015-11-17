from __future__ import print_function
import httplib2

from googleapiclient import discovery

from oauth2client.client import SignedJwtAssertionCredentials

import datetime
from datetime import timedelta
import dateutil.parser

class AppletonMakerspaceWeeklyCalendar():
    """
    Creates a Google Calendar API service object and outputs a list of the next
    7 days of events on the user's calendar.
    """
    def __init__(self, service_account_name, path_to_key):
        self.service_account_name = service_account_name
        self.path_to_key = path_to_key

    def fetch_events(self):
        f = file(self.path_to_key, 'rb')
        key = f.read()
        f.close()

        # Note that the first parameter to SignedJwtAssertionCredentials, service_account_name,
        # is the Email address created for the Service account. It must be the email
        # address associated with the key that was created.

        #https://console.developers.google.com/apis/credentials?project=appletonmakerspace-1075

        credentials = SignedJwtAssertionCredentials(
            #you need to share access to the calendar to this user from the dev console:
            self.service_account_name,
            key,
            scope='https://www.googleapis.com/auth/calendar.readonly')

        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        #now_date = datetime.datetime.utcnow()
        now_date = datetime.datetime.now()#FIXME
        start_lookahead_date = now_date.isoformat() + 'Z' # 'Z' indicates UTC time
        end_lookahead_date = (now_date + datetime.timedelta(days=7)).isoformat() + 'Z'

        eventsResult = service.events().list(
            calendarId='appletonmakerspace@gmail.com', #this is the calendar shared to the service account
            timeMin=start_lookahead_date,
            timeMax=end_lookahead_date,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = eventsResult.get('items', [])

        result = ''

        if not events:
            pass
        for event in events:
            start = dateutil.parser.parse(event['start'].get('dateTime', event['start'].get('date')))
            end = dateutil.parser.parse(event['end'].get('dateTime', event['end'].get('date')))
            result += '- ' + event['summary'] + '! ' + start.strftime("%A %-I:%M%p") + '-' + end.strftime("%-I:%M%p") + '\n\n'

        return result

