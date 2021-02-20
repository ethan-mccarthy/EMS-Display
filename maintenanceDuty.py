import pandas as pd # Pandas is what allows us to work with the retrieved data as a data frame
from datetime import date, time, datetime, timedelta
from googleAPI import *

###################################################################

def getMaintenanceData(verbose=True):
    # Get date/time data which is important for getting the correct maintenance
    today = datetime.now()

    # Tell the Google API that we want to access a spreadsheet
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Google Sheet ID (from the sharable URL)
    SPREADSHEET_ID = 'PLACE YOUR SPREADSHEET ID HERE'

    # Define which tab of the spreadsheet we want to retrieve
    SPREADSHEET_TAB_NAME = today.strftime("%B") ## Gets the tab of the current month

    # Gets the data from the Google Sheet and stores it in the variable "Data"
    maintenanceRawData = pull_sheet_data(SCOPES, SPREADSHEET_ID, SPREADSHEET_TAB_NAME, verbose)

    # Convert the retrieved raw "Data" to a data frame that can be more easily worked with
    maintenanceDF = pd.DataFrame(maintenanceRawData[1:], columns=maintenanceRawData[0])

    dateText = today.strftime("%B %-d, %Y") # Month dd, YYYY
    dateNumeric = today.strftime("%-m/%-d") # dd/mm/YY

    if verbose: print("Today is " + dateText)

    shift = "Error: shift not set"

    # Evaluate the time data to set the shift
    if today.hour >= 7 and today.hour < 15:
        shift = "DW"
    elif today.hour >= 15 or today.hour < 7:
        shift = "EM"

    if verbose: print("Current shift: " + shift)

    data = []

    currentShiftData = maintenanceDF.loc[maintenanceDF['DATE'] == dateNumeric]

    shiftMaintenance = currentShiftData.iloc[0][shift + ' MAINTENANCE DUTY']
    birthday = currentShiftData.iloc[0]['BIRTHDAY']
    holiday = currentShiftData.iloc[0]['HOLIDAY']

    data.append([shift, shiftMaintenance, birthday, holiday])

    if shiftMaintenance == "" or shiftMaintenance == None:
        if verbose: print("Looks like you don't have maintenance today, yay!")
    else:
        if verbose: print("Today's maintenance:  " + shiftMaintenance)

    if birthday != None:
        if verbose: print("Happy Birthday " + birthday + "!")
    if holiday != None and holiday != "Christmas Day" and holiday != "Christmas Eve":
        if verbose: print("Happy " + holiday + "!")
    elif holiday != None and (holiday == "Christmas Day" or holiday == "Christmas Eve"):
        if verbose: print("Merry " + holiday + "!")

    if shift == "EM":
        prevShiftMaintenance = currentShiftData.iloc[0]["DW" + ' MAINTENANCE DUTY']
        if verbose: print("Previous shift maintenance: " + prevShiftMaintenance)
        data.append(["DW", prevShiftMaintenance, "", ""])
    elif shift == "DW":
        yesterday = datetime.today() - timedelta(days=1)
        if yesterday.month != today.month:
            ## Get the previous day's maintenance spreadsheet
            # Define which tab of the spreadsheet we want to retrieve
            SPREADSHEET_TAB_NAME = yesterday.strftime("%B") ## Gets the tab of the current month

            # Tell the Google API that we want to access a spreadsheet
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

            # Google Sheet ID (from the sharable URL)
            SPREADSHEET_ID = '1drj0USNBd01L1Nr6lqRnx2vEsH8hei6sEASFitYE0fY'

            # Gets the data from the Google Sheet and stores it in the variable "Data"
            maintenanceRawData_yester = pull_sheet_data(SCOPES, SPREADSHEET_ID, SPREADSHEET_TAB_NAME, verbose)

            # Convert the retrieved raw "Data" to a data frame that can be more easily worked with
            maintenanceDF_yester = pd.DataFrame(maintenanceRawData_yester[1:], columns=maintenanceRawData_yester[0])

            prevShiftData = maintenanceDF_yester.loc[maintenanceDF_yester['DATE'] == dateNumeric]

            prevShiftMaintenance = prevShiftData.iloc[0]["EM" + ' MAINTENANCE DUTY']
            data.append(["EM", prevShiftMaintenance, "", ""])
        elif yesterday.month == today.month:
            yesterdayShiftData = maintenanceDF.loc[maintenanceDF['DATE'] == yesterday.strftime("%-m/%-d")]
            yesterdayMaintenance = yesterdayShiftData.iloc[0]["EM" + ' MAINTENANCE DUTY']
            data.append(["EM", yesterdayMaintenance, "", ""])

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
















































