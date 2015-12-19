"""
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
import argparse
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import dateutil.parser

"""
Based on:
http://codecomments.wordpress.com/2008/01/04/python-gmail-smtp-example/

Added argparse bits to move gmail credentials out of the script.
Hardcoded the schedule and messages into the script.
"""


def sendMail(u, p, r, subject, text):
    gmailUser = u
    gmailPassword = p
    recipient = r

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()

footer = """


--
Want a place to track your project, or look at what others are working on?

Check out the Trello Project Board! https://trello.com/b/eSPKdh9O/dhmn-project-board

Appleton Makerspace
121R B North Douglas St
Appleton, WI 54914
"""  # NOQA

projects = """
Makers! It's time to share... what have you been hacking on or making?

Reply to this email with a brief run-down of whatever projects have been keeping you busy.


*** This weekly sharing encouragement idea shamelessly stolen from reMMinderbot at Milwaukee Makerspace http://groups.google.com/group/milwaukeemakerspace
"""  # NOQA


def formatEvents(events):

    lines = []

    for event in events:
        start = dateutil.parser.parse(
            event['start'].get(
                'dateTime',
                event['start'].get('date')
            )
        )
        end = dateutil.parser.parse(
            event['end'].get(
                'dateTime',
                event['end'].get('date')
            )
        )
        lines.append(
            '    - {summary}! {start}-{end}'.format(
                summary=event['summary'],
                start=start.strftime("%A %-I:%M%p"),
                end=end.strftime("%-I:%M%p"),
            )
        )

    return '\n\n'.join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Send weekly events to dhmn-discuss.'
    )
    parser.add_argument(
        '--user',
        help='Gmail user.'
    )
    parser.add_argument(
        '--password',
        help='Gmail password.'
    )
    parser.add_argument(
        '--service_account_name',
        help='Google Calendar API Service Account name'
    )
    parser.add_argument(
        '--path_to_key',
        help='Path to Google Calendar API private key'
    )
    parser.add_argument(
        '--calendar_id',
        help='Calendar from which to pull events. ' +
        'Must be shared to the Service Account user.'
    )
    parser.add_argument(
        '--days',
        help='Days from now to search through for events.'
    )
    parser.add_argument(
        'recipient'
    )
    args = parser.parse_args()

    import datetime
    d = datetime.date.today()
    datestring = '{0:04d}-{1:02d}-{2:02d}'.format(d.year, d.month, d.day)

    from eventcalendar import EventCalendar
    calendar = EventCalendar(
        args.service_account_name,
        args.path_to_key,
        args.calendar_id,
        datetime.timedelta(days=int(args.days)),
    )

    from recentwikiedits import RecentWikiEdits
    recent_wiki_edits = RecentWikiEdits()

    separator = '\n---------------------------------------------------------\n'
    this_week_email_body = separator
    this_week_email_body += 'This Week at the Appleton Makerspace'
    this_week_email_body += separator + '\n'
    this_week_email_body += formatEvents(calendar.fetch_events())
    this_week_email_body += '\n\n'
    this_week_email_body += separator
    this_week_email_body += 'Recent Wiki Edits'
    this_week_email_body += separator + '\n'
    this_week_email_body += recent_wiki_edits.fetch()
    this_week_email_body += '\n\n'

    sendMail(
        args.user,
        args.password,
        args.recipient,
        "This Week at the Appleton Makerspace",
        this_week_email_body + footer,
    )
    sendMail(
        args.user,
        args.password,
        args.recipient,
        "What Have You Been Hacking/Making? [" + datestring + " edition]",
        projects
    )
