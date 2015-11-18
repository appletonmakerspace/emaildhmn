"""
Began from:
https://developers.google.com/google-apps/calendar/quickstart/python
--
Copyright (c) 2015 Mike Putnam <mike@theputnams.net>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from __future__ import print_function
import httplib2

from googleapiclient import discovery

from oauth2client.client import SignedJwtAssertionCredentials

import datetime


class EventCalendar():

    def __init__(
        self,
        service_account_name,
        path_to_key,
        calendar_id,
        time_delta,
    ):
        self.service_account_name = service_account_name
        self.path_to_key = path_to_key
        self.calendar_id = calendar_id
        self.time_delta = time_delta

    def fetch_events(self):

        with open(self.path_to_key, 'r+b') as f:
            key = f.read()
        f.close()

        # Note that the first parameter to SignedJwtAssertionCredentials,
        # service_account_name, is the Email address created for the Service
        # account. It must be the email address associated with the key that
        # was created via the Google API console:
        #
        # https://console.developers.google.com
        #
        # Further, you need to share or delegate the calendar access to the
        # email address associated with the key. This is done from the
        # user-side settings behind the calendar itself.

        credentials = SignedJwtAssertionCredentials(
            self.service_account_name,
            key,
            scope='https://www.googleapis.com/auth/calendar.readonly'
        )

        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now_date = datetime.datetime.utcnow()
        start_lookahead_date = now_date.isoformat() + 'Z'
        end_lookahead_date = (
            now_date + self.time_delta
        ).isoformat() + 'Z'

        eventsResult = service.events().list(
            calendarId=self.calendar_id,
            timeMin=start_lookahead_date,
            timeMax=end_lookahead_date,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = eventsResult.get('items', [])

        return events
