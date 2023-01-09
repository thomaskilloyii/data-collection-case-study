from __future__ import print_function

import os.path
import settings

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of the spreadsheet containing a list of names.
# You will need to add your own Spreadsheet ID
# Please refer to the beginning of the README.md
SPREADSHEET_ID = ''

# Enter ranges to search by
SAMPLE_RANGE_NAME = ["!A2:A", "!B2:B", "!C2:C", "!D2:D"]


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().batchGet(spreadsheetId=SPREADSHEET_ID,
                                         ranges=SAMPLE_RANGE_NAME,
                                         majorDimension="COLUMNS").execute()

        # Returns multiple ranges as JSON
        values_json = result.get('valueRanges', [])

        # Add spreadsheet ranges as separate lists
        # within values list
        values = []
        for i, value in enumerate(values_json):
            if i >= 4:
                break
            get_lists = values_json[i].get("values")

            for individual_list in get_lists:
                values.append(individual_list)

        if not values:
            print('No data found.')
            return

        # Append values list to global list from settings.py
        # values is indexed by 0 which corresponds to column A
        # Save names from Handles Spreadsheet as List from settings.py
        for twit_list in values[0]:
            settings.twitter_handles.append('%s' % twit_list)

        for telegram_list in values[1]:
            settings.telegram_handles.append('%s' % telegram_list)

        for youtube_list in values[3]:
            settings.youtube_handles.append('%s' % youtube_list)

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()


# Portions of this page are reproduced from work created and shared by Google and
# used according to terms described in the Creative Commons 4.0 Attribution License.
