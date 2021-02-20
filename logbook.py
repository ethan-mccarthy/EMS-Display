import pandas as pd # Pandas is what allows us to work with the retrieved data as a data frame
from datetime import datetime
from googleAPI import *


###################################################################
## These are the links and access information for the station officer Google Sheet

# Tell the Google API that we want to access a spreadsheet
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Google Sheet ID (from the sharable URL)
SPREADSHEET_ID = 'PLACE YOUR SPREADSHEET ID HERE'

###################################################################

## Get the data to get the fields that we want and print them to the console
def getShiftData(n = 5, verbose=True):
    # Define which tab of the spreadsheet we want to retrieve
    SPREADSHEET_TAB_NAME = 'Station Officer Log Book'

    # Gets the data from the Google Sheet and stores it in the variable "stationOfficerRawData"
    stationOfficerRawData = pull_sheet_data(SCOPES, SPREADSHEET_ID, SPREADSHEET_TAB_NAME, verbose)

    # Convert the retrieved raw "stationOfficerRawData" to a data frame that can be more easily worked with
    stationOfficerDF = pd.DataFrame(stationOfficerRawData[1:], columns=stationOfficerRawData[0])

    # Edit some of the dataframe so it's easier to reference
    stationOfficerDF.rename(columns = {'SHIFT DATE':'SHIFT_DATE'}, inplace = True)
    stationOfficerDF.rename(columns = {'START TIME':'START_TIME'}, inplace = True)

    # Convert some of the entries of the data frame so they are recognized as dates
    stationOfficerDF['SHIFT_DATE'] = pd.to_datetime(stationOfficerDF.SHIFT_DATE)
    stationOfficerDF['START_TIME'] = pd.to_datetime(stationOfficerDF.START_TIME)

    # Sort the dataframe first by the shift date, then by the time of the shift (needed to get "most")
    stationOfficerDF = stationOfficerDF.sort_values(['SHIFT_DATE', 'START_TIME'], ascending=[True, True])

    shiftData = stationOfficerDF.tail(n).reset_index(drop=True)

    # initialize list of lists (which will get returned by this function)
    data = [] 

    # iterate through each row of the dataframe and add parsed date to a new dataframe
    for ind in reversed(shiftData.index): 
        dateShift = shiftData.iloc[ind]['SHIFT_DATE'].to_pydatetime()
        timeShift = shiftData.iloc[ind]['START_TIME'].to_pydatetime()

        if verbose:
            print(str(abs(ind-4)) + " shift(s) ago: \nDate: " + dateShift.strftime("%m/%d/%y") + 
                "\nTime: " + timeShift.strftime("%H%M") +
                "\nRelief Crew: " + shiftData.iloc[ind]['RELIEF'] + 
                "\nPrevious Crew: " + shiftData.iloc[ind]['PREVIOUS CREW'])

        data.append([dateShift.strftime("%m/%d/%y"), 
            timeShift.strftime("%H%M"), 
            shiftData.iloc[ind]['RELIEF'],
            shiftData.iloc[ind]['PREVIOUS CREW']])

    if verbose: print("Done looping through dataframe")

    ### Create the pandas dataframe and return it
    recentShifts = pd.DataFrame(data, columns = ['SHIFT_DATE', 'START_TIME', 'RELIEF', 'PREVIOUS_CREW']) 
    return(recentShifts)

##########################################################################

# Get COVID-19 log book (from the master spreadsheet)
def getCovidLog(verbose = True):
    # Define which tab of the spreadsheet we want to retrieve
    SPREADSHEET_TAB_NAME = 'COVID-19 Log Book'

    # Gets the data from the Google Sheet and stores it in the variable "Data"
    covid19LogRawData = pull_sheet_data(SCOPES, SPREADSHEET_ID, SPREADSHEET_TAB_NAME, verbose)

    # Convert the retrieved raw "Data" to a data frame that can be more easily worked with
    covid19LogDF = pd.DataFrame(covid19LogRawData[1:], columns=covid19LogRawData[0])
    
    print(covid19LogDF.tail())

















