import pandas as pd # Pandas is what allows us to work with the retrieved data as a data frame
from datetime import date, time, datetime, timedelta
from googleAPI import *

###################################################################

def getMaintenanceData(verbose=True):
    # Get date/time data which is important for getting the correct maintenance
    today = datetime.now()
    yesterday = datetime.today() - timedelta(days=1)

    # Tell the Google API that we want to access a spreadsheet
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Google Sheet ID (from the sharable URL)
    SPREADSHEET_ID = 'YOUR SPREADSHEET ID HERE'

    # Define which tab of the spreadsheet we want to retrieve
    SPREADSHEET_TAB_NAME = today.strftime("%B") ## Gets the tab of the current month

    # Gets the data from the Google Sheet and stores it in the variable "Data"
    maintenanceRawData = pull_sheet_data(SCOPES, SPREADSHEET_ID, SPREADSHEET_TAB_NAME, verbose)

    # Convert the retrieved raw "Data" to a data frame that can be more easily worked with
    maintenanceDF = pd.DataFrame(maintenanceRawData[1:], columns=maintenanceRawData[0])

    dateText = today.strftime("%B %-d, %Y") # Month dd, YYYY
    dateNumeric = today.strftime("%-m/%-d") # dd/mm/YY
    yesterdayNumeric = yesterday.strftime("%-m/%-d") # dd/mm/YY

    if verbose: print("Today is " + dateText)
    if verbose: print("Yesterday was  " + yesterdayNumeric)

    shift = "Error: shift not set"

    # Evaluate the time data to set the shift
    if today.hour >= 7 and today.hour < 15:
        shift = "DW"
    elif today.hour >= 15 or today.hour < 7:
        shift = "EM"

    if verbose: print("Current shift: " + shift)

    data = []

    currentShiftData = maintenanceDF.loc[maintenanceDF['DATE'] == dateNumeric]

    if yesterday.month != today.month:
        SPREADSHEET_TAB_NAME = yesterday.strftime("%B") ## Gets the tab of the current month

        maintenanceRawData_yester = pull_sheet_data(SCOPES, SPREADSHEET_ID, SPREADSHEET_TAB_NAME, verbose)

        yesterData = pd.DataFrame(maintenanceRawData_yester[1:], columns=maintenanceRawData_yester[0])

        yesterData = yesterData.loc[yesterData['DATE'] == yesterdayNumeric]
    elif yesterday.month == today.month:
        yesterData = maintenanceDF.loc[maintenanceDF['DATE'] == yesterdayNumeric]

    birthday = currentShiftData.iloc[0]['BIRTHDAY']
    holiday = currentShiftData.iloc[0]['HOLIDAY']

    if birthday != None:
        if verbose: print("Happy Birthday " + birthday + "!")
    if holiday != None and holiday != "Christmas Day" and holiday != "Christmas Eve":
        if verbose: print("Happy " + holiday + "!")
    elif holiday != None and (holiday == "Christmas Day" or holiday == "Christmas Eve"):
        if verbose: print("Merry " + holiday + "!")

    if shift == "EM":
        if today.hour >= 15:
            shiftMaintenance = currentShiftData.iloc[0]["EM" + ' MAINTENANCE DUTY']
            if verbose: print("Current shift maintenance: " + shiftMaintenance)
            data.append([shift, shiftMaintenance, birthday, holiday])

            prevShiftMaintenance = currentShiftData.iloc[0]["DW" + ' MAINTENANCE DUTY']
            if verbose: print("Previous shift maintenance: " + prevShiftMaintenance)
            data.append(["DW", prevShiftMaintenance, birthday, holiday])
        elif today.hour < 7:
            shiftMaintenance = yesterData.iloc[0]["EM" + ' MAINTENANCE DUTY']
            if verbose: print("Current shift maintenance: " + shiftMaintenance)
            data.append([shift, shiftMaintenance, birthday, holiday])

            prevShiftMaintenance = shiftMaintenance = yesterData.iloc[0]["DW" + ' MAINTENANCE DUTY']
            if verbose: print("Previous shift maintenance: " + prevShiftMaintenance)
            data.append(["DW", prevShiftMaintenance, birthday, holiday])
    elif shift == "DW":
        prevShiftMaintenance = yesterData.iloc[0]["EM" + ' MAINTENANCE DUTY']
        if verbose: print("Previous shift maintenance: " + prevShiftMaintenance)
        data.append(["EM", prevShiftMaintenance, "", ""])

        shiftMaintenance = currentShiftData.iloc[0]["DW" + ' MAINTENANCE DUTY']
        if verbose: print("Current shift maintenance: " + shiftMaintenance)
        data.append([shift, shiftMaintenance, birthday, holiday])      

    ### Create the pandas dataframe and return it
    finalData = pd.DataFrame(data, columns = ['Shift', 'MaintenanceDuty', 'Birthday', 'Holiday']) 
    return(finalData)


def getCurrentDateTime():
    today = datetime.now()
    currentDateTime = today.strftime("%-m/%-d") + " at " + today.strftime("%H:%M")
    return currentDateTime

def todaysDate():
    today = datetime.now()
    currentDate = today.strftime("%A, %B %-d, %Y")
    return currentDate

