from config import *
#from google_connect import *
import google_connect
import csv_creation
import canvas_api


if __name__ == '__main__':
    print (google_connect.listGoogleSheets())

    repeat = "y"
    while repeat.lower() == 'y':
        sheet_choice = input ('Type in very carefully the Spreadsheet you want to import. ')
        school_account = input ('What is the school account number? ')

        csv_creation.createCSVsCoursesEnrollmentsTerms(sheet_choice, school_account)
        canvas_api.sisIMPORT()
        canvas_api.createZip()
        repeat = input ('Do you have another spreadsheet to import? (Y or N) ')

