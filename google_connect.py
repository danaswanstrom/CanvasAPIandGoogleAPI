
#Connection to Google

#Code to import all of the functions that we will need

from config import *
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import pandas as pd
import numpy as np
import json


#code to connect to Google Spreadsheets
#information for this section came from http://pbpython.com/pandas-google-forms-part1.html

SCOPE = ["https://spreadsheets.google.com/feeds"]
json_key = json.load(open(SECRETS_FILE))
credentials = SignedJwtAssertionCredentials(json_key['client_email'],
bytes(json_key['private_key'], 'UTF-8'),
SCOPE)
gc = gspread.authorize(credentials)



def listGoogleSheets():
    """
    This function will just print out the list of Google Spreadsheets in the folder that the json file is pointing to.
    """
    #Code to print out the Spreadsheets that are Available in Google
    print("The following sheets are available")
    for sheet in gc.openall():
        print("{} - {}".format(sheet.title, sheet.id))
    return("That's the List!")

def createListGoogleSheets():
    """
    This function will create a python list of the spreadsheets that can be used in loops etc.
    """
    GoogleSheetsList = []
    for sheet in gc.openall():
        GoogleSheetsList.append(sheet.title)
    return GoogleSheetsList

def importSheet(workbookName):
    """
    Given a string that is the workbookName, the first sheet in the workbook will be imported into Python as a dataframe
    """
    workbook = gc.open(workbookName)
    # Get the first sheet
    firstSheet = workbook.sheet1
    # Extract all data into a dataframe
    firstSheetDataFrame = pd.DataFrame(firstSheet.get_all_records())
    #lowercaseColumnNames = [x.lower() for x in firstSheetDataFrame.columns.values]
    #firstSheetDataFrame.columns = lowercaseColumnNames
    return firstSheetDataFrame


canvasStudentImport = importSheet("1801Student")
canvasStudentImport.drop_duplicates(inplace = True)
canvasStudentIndexed = canvasStudentImport.set_index(['login_id'])

canvasStaffImport = importSheet("1801Staff")
canvasStaffImport.drop_duplicates(inplace = True)
canvasStaffIndexed = canvasStaffImport.set_index(['login_id'])
canvasStaffandStudentsIndexed = pd.concat([canvasStudentIndexed, canvasStaffIndexed], axis=0)