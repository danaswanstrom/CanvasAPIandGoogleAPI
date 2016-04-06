import numpy as np
import pandas as pd
import canvas_api
import google_connect


#The first group of funtions are Skyward File injestions. Long term we want the script here to access the files from
#a server that has fresh files each night.


def coursesDF(workbookName,accountID):
    """
    Inputs: Name of a Google Spreadsheet that has been shared with
    the account whose Oauth Credentials are used in this script
    and an accountID for canvas.
    
    Variables needed for this function:
    Global Variables:
    columnsCoursesCSV: list of the column names needed for the Canvas import
    
    Helper Functions:
    importSheet()
    
    Returns: dataframe called courses that will be used for Canvas api
    """

    importedGoogleSheet = google_connect.importSheet(workbookName)
    
    #Next two lines make the columns names all lowercase
    lowercaseColumnNames = [x.lower() for x in importedGoogleSheet.columns.values]
    importedGoogleSheet.columns = lowercaseColumnNames
    
    index = 0
    courses = pd.DataFrame(data=np.zeros((0, len(canvas_api.columnsCoursesCSV))), columns=canvas_api.columnsCoursesCSV)
    spreadsheet_length = len(importedGoogleSheet.index)
    while index < spreadsheet_length and importedGoogleSheet.course_name[index] != '':
        courses = courses.append({'course_id':importedGoogleSheet.loc[index,"course_id"],
                                  'long_name':importedGoogleSheet.loc[index,"course_name"],
                                  'short_name':importedGoogleSheet.loc[index,"course_name"], 
                                  'account_id':accountID, 'status':'active'},ignore_index=True)
        index += 1
    return courses


def enrollmentsDF(workbookName):
    """
    Inputs: Name of a Google Spreadsheet that has been shared with the account
    whose Oauth Credentials are used in this script.
        
    Variables needed for this function:
    Global Variables:
    lowercaseColumnNames: this contains a list of the column names from the imported Google spreadsheet
    where all letters are converted to lowercase
    columnsEnrollmentCSV: list of the column names needed for the Canvas import
    
    Helper Functions:
    importSheet()
    
    Returns: dataframe called enrollments
    
    """
    index = 0
    importedGoogleSheet = google_connect.importSheet(workbookName)
    #Next two lines make the columns names all lowercase
    lowercaseColumnNames = [x.lower() for x in importedGoogleSheet.columns.values]
    importedGoogleSheet.columns = lowercaseColumnNames
    spreadsheet_length = len(importedGoogleSheet.index)
    #lowercaseColumnNames = importedGoogleSheet.columns
    #create an empty dataframe based on the required columns for a Canvas csv.
    enrollments = pd.DataFrame(data=np.zeros((0, len(canvas_api.columnsEnrollmentCSV))),
                               columns=canvas_api.columnsEnrollmentCSV)
        
    #For enrollments to be created for a course, the course must have a name given in the Google spreadsheet. 
    #Next line checks for blank course names.
    while index < spreadsheet_length and importedGoogleSheet.course_name[index] != '':
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
                    sis_id = canvas_api.find_sis_user_id(importedGoogleSheet.loc[index, possibleColumnName])
                    #sis_id = canvasStaffandStudentsIndexed.loc[importedGoogleSheet.loc[index,possibleColumnName],'user_id']
                    enrollments = enrollments.append({'course_id':importedGoogleSheet.loc[index,"course_id"],
                                                      'user_id':sis_id,'role':'Teacher',  'status':'active'},
                                                     ignore_index=True)
                except: 
                    if importedGoogleSheet.loc[index,possibleColumnName] != '': 
                        enrollments = enrollments.append({'course_id':importedGoogleSheet.loc[index,"course_id"],
                                                          'user_id':999998,'role':'Student',  'status':'active'},
                                                         ignore_index=True)
        
        for x in range(1,len(importedGoogleSheet.columns)):
            possibleColumnName = "teacher" + str(x)
            if possibleColumnName in lowercaseColumnNames:
                try:
                    sis_id = canvas_api.find_sis_user_id(importedGoogleSheet.loc[index, possibleColumnName])
                    enrollments = enrollments.append({'course_id':importedGoogleSheet.loc[index,"course_id"],
                                                      'user_id':sis_id,'role':'Teacher',  'status':'active'},
                                                     ignore_index=True)
                except:
                    if importedGoogleSheet.loc[index,possibleColumnName] != '':
                        enrollments = enrollments.append({'course_id':importedGoogleSheet.loc[index,"course_id"],
                                                          'user_id':999998,'role':'Student',  'status':'active'},
                                                         ignore_index=True)
        
        for x in range(1,len(importedGoogleSheet.columns)):
            possibleColumnName = "student" + str(x)
            if possibleColumnName in lowercaseColumnNames:
                try:
                    sis_id = canvas_api.find_sis_user_id(importedGoogleSheet.loc[index, possibleColumnName])
                    enrollments = enrollments.append({'course_id':importedGoogleSheet.loc[index,"course_id"],
                                                      'user_id':sis_id,'role':'Student',  'status':'active'},
                                                     ignore_index=True)
                except:
                    if importedGoogleSheet.loc[index,possibleColumnName] != '':
                        enrollments = enrollments.append({'course_id':importedGoogleSheet.loc[index,"course_id"],
                                                          'user_id':999998,'role':'Student',  'status':'active'},
                                                         ignore_index=True)
        
        #index counter takes us through each row of the dataframe
        index +=1
    
    
    return enrollments


def coursesVertDF(workbookName,accountID):
    """
    Inputs: Name of a Google Spreadsheet that has been shared with the account
    whose Oauth Credentials are used in this script
    and an accountID for canvas. The Google Spreadsheet needs to be organized in a vertical orientation.
    
    Variables needed for this function:
    Global Variables:
    columnsCoursesCSV: list of the column names needed for the Canvas import
    
    Helper Functions:
    importSheet()
    
    Returns: dataframe called courses
    """
    importedGoogleSheet = google_connect.importSheet(workbookName)
    importedGoogleSheet['Course_ID'] = importedGoogleSheet['Course_ID'].str.lower()
    index = 0
    courses = pd.DataFrame(data=np.zeros((0, len(canvas_api.columnsCoursesCSV))), columns=canvas_api.columnsCoursesCSV)
    importedGoogleSheet = importedGoogleSheet.set_index('Course_ID')
    
    for course in importedGoogleSheet.columns:
        if importedGoogleSheet.loc['course_name',course] != '':
            courses = courses.append({'course_id': course,
                                      'long_name':importedGoogleSheet.loc['course_name',course],
                                      'short_name':importedGoogleSheet.loc['course_name',course], 
                                      'account_id':accountID, 'status':'active'},ignore_index=True)
    return courses


def enrollmentsVertDF(workbookName):
    """
    Inputs: Name of a Google Spreadsheet that has been shared with the account
    whose Oauth Credentials are used in this script.
        
    Variables needed for this function:
    Global Variables:
    lowercaseColumnNames: this contains a list of the column names
    from the imported Google spreadsheet where all letters
    are converted to lowercase
    columnsEnrollmentCSV: list of the column names needed for the Canvas import
    
    Helper Functions:
    importSheet()
    
    Returns: dataframe called enrollments
    
    """
    index = 0
    importedGoogleSheet = google_connect.importSheet(workbookName)
    importedGoogleSheet['Course_ID'] = importedGoogleSheet['Course_ID'].str.lower()
    importedGoogleSheet = importedGoogleSheet.set_index('Course_ID')
    
    index = 0
    lowercaseRowNames = importedGoogleSheet.index.values.tolist()
    #lowercaseColumnNames = importedGoogleSheet.columns
    #create an empty dataframe based on the required columns for a Canvas csv.
    enrollments = pd.DataFrame(data=np.zeros((0, len(canvas_api.columnsEnrollmentCSV))),
                               columns=canvas_api.columnsEnrollmentCSV)
        
    #For enrollments to be created for a course, the course must have a name given in the Google spreadsheet. 
    #Next line checks for blank course names.
    for course in importedGoogleSheet.columns:
        if importedGoogleSheet.loc['course_name',course] != '':
            for x in range(1,len(importedGoogleSheet.index.values.tolist())):
                possibleRowName = "principal" + str(x)
                if possibleRowName in lowercaseRowNames and importedGoogleSheet.loc[possibleRowName,course] != '':
                    sis_id = canvas_api.find_sis_user_id(importedGoogleSheet.loc[possibleRowName, course])
                    
                    if sis_id != 'Unknown':
                        enrollments = enrollments.append({'course_id':course,
                                                          'user_id':sis_id,'role':'Teacher',
                                                          'status':'active'},
                                                         ignore_index=True)
                    else:
                        enrollments = enrollments.append({'course_id':course,
                                                          'user_id':999998,'role':'Student',
                                                          'status':'active'},
                                                         ignore_index=True)  
    
    for course in importedGoogleSheet.columns:
        if importedGoogleSheet.loc['course_name',course] != '':
            for x in range(1,len(importedGoogleSheet.index.values.tolist())):
                possibleRowName = "teacher" + str(x)
                if possibleRowName in lowercaseRowNames and importedGoogleSheet.loc[possibleRowName,course] != '':
                    sis_id = canvas_api.find_sis_user_id(importedGoogleSheet.loc[possibleRowName, course])
                    
                    if sis_id != 'Unknown':
                        enrollments = enrollments.append({'course_id':course,
                                                          'user_id':sis_id,'role':'Teacher',
                                                          'status':'active'},
                                                         ignore_index=True)
                    else:
                        enrollments = enrollments.append({'course_id':course,
                                                          'user_id':999998,'role':'Student',
                                                          'status':'active'},
                                                         ignore_index=True)  
    
    
    for course in importedGoogleSheet.columns:
        if importedGoogleSheet.loc['course_name',course] != '':
            for x in range(1,len(importedGoogleSheet.index.values.tolist())):
                possibleRowName = "student" + str(x)
                if possibleRowName in lowercaseRowNames and importedGoogleSheet.loc[possibleRowName,course] != '':
                    sis_id = canvas_api.find_sis_user_id(importedGoogleSheet.loc[possibleRowName, course])
                    
                    if sis_id != 'Unknown':
                        enrollments = enrollments.append({'course_id':course,
                                                          'user_id':sis_id,'role':'Student',
                                                          'status':'active'},
                                                         ignore_index=True)
                    else:
                        enrollments = enrollments.append({'course_id':course,
                                                          'user_id':999998,'role':'Student',
                                                          'status':'active'},
                                                         ignore_index=True)  
    
    return enrollments



def createCSVsCoursesEnrollmentsTerms(workbookName, AccountID):
    """
    This fuction will take in Google Spreadsheet name.
    Return: A list of lists composed of each row of the spread
    """   
    enrollments = enrollmentsDF(workbookName)
    courses = coursesDF(workbookName, AccountID)
    enrollments.to_csv(canvas_api.csvExportLocation + "enrollments.csv", index=False, float_format='%.0f')
    courses.to_csv(canvas_api.csvExportLocation + "courses.csv", index=False, float_format='%.0f')
    return print("Done with CSV Files. Files located in " + canvas_api.csvExportLocation)

def createCSVsCoursesEnrollmentsTermsVert(workbookName, AccountID):
    """
    This fuction will take in Google Spreadsheet name.
    Return: A list of lists composed of each row of the spread
    """   
    enrollments = enrollmentsVertDF(workbookName)
    courses = coursesVertDF(workbookName, AccountID)
    enrollments.to_csv(canvas_api.csvExportLocation + "enrollments.csv", index=False, float_format='%.0f')
    courses.to_csv(canvas_api.csvExportLocation + "courses.csv", index=False, float_format='%.0f')
    return print("Done with CSV Files. Files located in " + canvas_api.csvExportLocation)



