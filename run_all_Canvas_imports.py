from config import *
from google_connect import *
from csv_creation import *
from canvas_api import *

spreadsheetList = createListGoogleSheets()

for name in spreadsheetList:
    if (name[:13]) == "Import2Canvas":
        subAccountNumber = name[13:16]
        createCSVsCoursesEnrollmentsTerms(name, subAccountNumber)
        createZip(subAccountNumber)
        sisIMPORT(subAccountNumber)
        

