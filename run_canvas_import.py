from config import *
from google_connect import *
from csv_creation import *
from canvas_api import *
print (listGoogleSheets())

repeat = "y"
while repeat.lower() == 'y':
    sheet_choice = input ('Type in very carefully the Spreadsheet you want to import. ')
    school_account = input ('What is the school account number? ')

    createCSVsCoursesEnrollmentsTerms(sheet_choice, school_account)
    sisIMPORT()
    createZip()
    repeat = input ('Do you have another spreadsheet to import? (Y or N) ')
