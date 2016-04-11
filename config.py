#config.py file
import sys
import os


#First is Canvas Related Config Information
danasToken = "***REMOVED***"
sis_import_Token = "***REMOVED***"
danaDec1Token = "***REMOVED***"


#Most code in other modules will use CanvasSISImportToken, so this is a way to switch tokens behind the scences
CanvasSISImportToken = danaDec1Token


Canvas_account_id = 1
Canvas_base_api_url = 'https://ecasd.instructure.com/api/'
#The write version is for imports and anything else that is written to Canvas to make sure accidents don't happen
Canvas_base_api_url_write = 'https://ecasd.test.instructure.com/api/'

#This section is Google Related Config Information
SECRETS_FILE = '/Users/dswanstrom/Documents/GitHub Local/SchoolProjects/CanvasAPI/Tokens/GoogleSpreadsheettoCanvasPythn-8a3815cd54b0.json'

#Define location of the CSV file exports. Must have a trailing "/" for it to work.
      
path = os.getcwd()

csvExportLocation = '{path}/CSVZipFiles/'.format(path = path)
#csvExportLocation = "X:/Inbox/"


########## DO NOT EDIT BELOW THIS LINE ##############
#CSV Formats for Canvas SIS Imports
columnsCoursesCSV = ["course_id", "long_name", "short_name", "account_id", "status"]
columnsEnrollmentCSV = ["course_id","user_id","role","status"]





























## Information for Google
#SECRETS_FILE = "C:\Temp\GoogleSpreadsheettoCanvasPythn-8a3815cd54b0.json"
#SCOPE = ["https://spreadsheets.google.com/feeds"]


## Information for csv_creation
#CSV Formats
#columnsCoursesCSV = ["course_id", "long_name", "short_name", "account_id", "status"]
#columnsEnrollmentCSV = ["course_id","user_id","role","status"]

#Define location of file exports. Must have a trailing "/" for it to work.

#csvExportLocation = "X:/Inbox/"

#Requires Python 3

#You will need to obtain a Google Secrets file as a json file. Please place this in the Tokens folder.
#It is best practice to use a service Google account
#Directions on obtaining that file can be found at http://pbpython.com/pandas-google-forms-part1.html

#These lines import some spreadsheets from Google that are imported from Skyward each day.
#The imports first get a student list and then a staff list and then removed duplicates
#The two dataframes are then combined into one so that any lookups of the student user_id can be made from one dataframe












###### Moved to Google connect .py
#canvasStudentImport = importSheet("1801Student")
#canvasStudentImport.drop_duplicates(inplace = True)
#canvasStudentIndexed = canvasStudentImport.set_index(['login_id'])

#canvasStaffImport = importSheet("1801Staff")
#canvasStaffImport.drop_duplicates(inplace = True)
#canvasStaffIndexed = canvasStaffImport.set_index(['login_id'])



#canvasStaffandStudentsIndexed = pd.concat([canvasStudentIndexed, canvasStaffIndexed], axis=0)