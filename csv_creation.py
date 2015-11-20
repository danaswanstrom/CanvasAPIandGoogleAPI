from google_connect import *
from config import *
import pandas as pd
import numpy as np
import json
import csv


#### Moved to Config.py
#CSV Formats
#columnsCoursesCSV = ["course_id", "long_name", "short_name", "account_id", "status"]
#columnsEnrollmentCSV = ["course_id","user_id","role","status"]
#Define location of file exports. Must have a trailing "/" for it to work.
#csvExportLocation = "C:\Temp\Inbox"


#The first group of funtions are Skyward File injestions. Long term we want the script here to access the files from
#a server that has fresh files each night.


def coursesDF(workbookName,accountID):
    """
    Inputs: Name of a Google Spreadsheet that has been shared with the account whose Oauth Credentials are used in this script
    and an accountID for canvas.
    
    Variables needed for this function:
    Global Variables:
    columnsCoursesCSV: list of the column names needed for the Canvas import
    
    Helper Functions:
    importSheet()
    
    Returns: dataframe called enrollments
    """
    importedGoogleSheet = importSheet(workbookName)
    index = 0
    courses = pd.DataFrame(data=np.zeros((0,len(columnsCoursesCSV))), columns=columnsCoursesCSV)
    while index < len(importedGoogleSheet.index) and importedGoogleSheet.course_name[index] != '':
        courses = courses.append({'course_id':importedGoogleSheet.loc[index,"course_id"], 'long_name':importedGoogleSheet.loc[index,"course_name"],'short_name':importedGoogleSheet.loc[index,"course_name"], 'account_id':accountID, 'status':'active'},ignore_index=True)
        index += 1
    return courses

def enrollmentsDF(workbookName):
    """
    Inputs: Name of a Google Spreadsheet that has been shared with the account whose Oauth Credentials are used in this script.
        
    Variables needed for this function:
    Global Variables:
    lowercaseColumnNames: this contains a list of the column names from the imported Google spreadsheet where all letters are converted to lowercase
    columnsEnrollmentCSV: list of the column names needed for the Canvas import
    
    Helper Functions:
    importSheet()
    
    Returns: dataframe called enrollments
    
    """
    index = 0
    importedGoogleSheet = importSheet(workbookName)
    
    lowercaseColumnNames = importedGoogleSheet.columns
    #create an empty dataframe based on the required columns for a Canvas csv.
    enrollments = pd.DataFrame(data=np.zeros((0,len(columnsEnrollmentCSV))), columns=columnsEnrollmentCSV)
        
    #For enrollments to be created for a course, the course must have a name given in the Google spreadsheet. Next line checks for blank course names.
    while index < len(importedGoogleSheet.index) and importedGoogleSheet.course_name[index] != '':
        #Three sections of code to add principals (which get added as teachers), teachers, and then students
        #The range for each section is based on the number of columns in the original google sheet
        #Each section has a loop that goes through possible column names that might be in the Google spreadsheet
            #The first if determines if a column name exists in the Google spreadsheet.
                #The second if checks to make sure that that row has a person in that column 
                #A new row is added to the enrollments dataframe if both conditions are met for the possible column names
        
        for x in range(1,len(importedGoogleSheet.columns)):
            possibleColumnName = "principal" + str(x)
            if possibleColumnName in lowercaseColumnNames:
                try:
                    sis_id = canvasStaffandStudentsIndexed.loc[importedGoogleSheet.loc[index,possibleColumnName],'user_id']
                    enrollments = enrollments.append({'course_id':importedGoogleSheet.loc[index,"course_id"], 'user_id':sis_id,'role':'Teacher',  'status':'active'},ignore_index=True)
                except: 
                    if importedGoogleSheet.loc[index,possibleColumnName] != '': 
                        enrollments = enrollments.append({'course_id':importedGoogleSheet.loc[index,"course_id"], 'user_id':999998,'role':'Student',  'status':'active'},ignore_index=True)
        
        for x in range(1,len(importedGoogleSheet.columns)):
            possibleColumnName = "teacher" + str(x)
            if possibleColumnName in lowercaseColumnNames:
                try:
                    sis_id = canvasStaffandStudentsIndexed.loc[importedGoogleSheet.loc[index,possibleColumnName],'user_id']
                    enrollments = enrollments.append({'course_id':importedGoogleSheet.loc[index,"course_id"], 'user_id':sis_id,'role':'Teacher',  'status':'active'},ignore_index=True)
                except:
                    if importedGoogleSheet.loc[index,possibleColumnName] != '':
                        enrollments = enrollments.append({'course_id':importedGoogleSheet.loc[index,"course_id"], 'user_id':999998,'role':'Student',  'status':'active'},ignore_index=True)
        
        for x in range(1,len(importedGoogleSheet.columns)):
            possibleColumnName = "student" + str(x)
            if possibleColumnName in lowercaseColumnNames:
                try:
                    sis_id = canvasStaffandStudentsIndexed.loc[importedGoogleSheet.loc[index,possibleColumnName],'user_id']
                    enrollments = enrollments.append({'course_id':importedGoogleSheet.loc[index,"course_id"], 'user_id':sis_id,'role':'Student',  'status':'active'},ignore_index=True)
                except:
                    if importedGoogleSheet.loc[index,possibleColumnName] != '':
                        enrollments = enrollments.append({'course_id':importedGoogleSheet.loc[index,"course_id"], 'user_id':999998,'role':'Student',  'status':'active'},ignore_index=True)
        
        #index counter takes us through each row of the dataframe
        index +=1
    
    
    return enrollments


def createCSVsCoursesEnrollmentsTerms(workbookName, AccountID):
    """
    This fuction will take in Google Spreadsheet name.
    Return: A list of lists composed of each row of the spread
    """
    terms = importSheet("terms")
    terms.to_csv(csvExportLocation +"terms.csv", index=False, float_format='%.0f')
    enrollments = enrollmentsDF(workbookName)
    courses = coursesDF(workbookName, AccountID)
    enrollments.to_csv(csvExportLocation +"enrollments.csv", index=False, float_format='%.0f')
    courses.to_csv(csvExportLocation +"courses.csv", index=False, float_format='%.0f')
    return print("Done with CSV Files. Files located in " + csvExportLocation)



