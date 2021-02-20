from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle

# Gets the data from the Google Sheet
def pull_sheet_data(SCOPES,SPREADSHEET_ID,RANGE_NAME, verbose):
    #creds = gsheet_api_check(SCOPES)
    service = build('sheets', 'v4', developerKey="PLACE YOUR GOOGLE API KEY HERE", cache_discovery=False)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=RANGE_NAME).execute()
        data = rows.get('values')
        if verbose: print("COMPLETE: Data retrieved successfully!")
        return data