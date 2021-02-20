import pandas as pd # Pandas is what allows us to work with the retrieved data as a data frame
from datetime import date, time, datetime, timedelta
from googleAPI import *
import requests

def getAnnouncements(verbose=True):
    # Get date/time data which is important for getting the correct maintenance
    today = datetime.now()

    # Tell the Google API that we want to access a spreadsheet
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Google Sheet ID (from the sharable URL)
    SPREADSHEET_ID = 'PLACE YOUR SPREADSHEET ID HERE'

    # Define which tab of the spreadsheet we want to retrieve
    SPREADSHEET_TAB_NAME = today.strftime("Announcements")

    # Gets the data from the Google Sheet and stores it in the variable "Data"
    announcementsRawData = pull_sheet_data(SCOPES, SPREADSHEET_ID, SPREADSHEET_TAB_NAME, verbose)

    # Convert the retrieved raw "Data" to a data frame that can be more easily worked with
    announcementsDF = pd.DataFrame(announcementsRawData[1:], columns=['Timestamp', 'Announcement Message', 'Website Link', 'Requesting Entity', 'Announcement Start Date', 'Announcement Expiry Date'])

    announcementsDF.rename(columns = {'Announcement Start Date':'START_DATE'}, inplace = True)
    announcementsDF.rename(columns = {'Announcement Expiry Date':'END_DATE'}, inplace = True)

    # Convert some of the entries of the data frame so they are recognized as dates
    announcementsDF['START_DATE'] = pd.to_datetime(announcementsDF.START_DATE)
    announcementsDF['END_DATE'] = pd.to_datetime(announcementsDF.END_DATE)

    announcementsDF = announcementsDF.sort_values(['END_DATE'], ascending=[True])

    booleanMask = (announcementsDF['START_DATE'] <= today.strftime("%-m/%-d/%Y")) & (announcementsDF['END_DATE'] >= today.strftime("%-m/%-d/%Y"))

    currentAnnouncements = announcementsDF[booleanMask] 

    return currentAnnouncements.reset_index(drop=True)






