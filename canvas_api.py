### Code to import CSV files into Canvas
from config import *
import requests
import json
import zipfile

#csvExportLocation = "X:/Inbox/"
#token = "***REMOVED***"
#account_id = 1
#base_api_url = 'https://ecasd.test.instructure.com/api/'

### Post csv or zip file for Sis Import. Just change the file name.
def createZip(subAccountNumber):
    canvasZipfile = zipfile.ZipFile('{csvExportLocation}canvasUpload-{subAccountNumber}.zip'.format(csvExportLocation = csvExportLocation,
                                                                                            subAccountNumber = subAccountNumber), 'w')
    #canvasZipfile.write('{csvExportLocation}courses.csv'.format(csvExportLocation = csvExportLocation)[,
     #                   os.path.basename(canvasZipfile)[,compress_type=zipfile.ZIP_DEFLATED]])
    #canvasZipfile.write('{csvExportLocation}enrollments.csv'.format(csvExportLocation = csvExportLocation)[,
     #                   os.path.basename(canvasZipfile)[, compress_type=zipfile.ZIP_DEFLATED]])
    canvasZipfile.write('{csvExportLocation}courses.csv'.format(csvExportLocation = csvExportLocation),compress_type=zipfile.ZIP_DEFLATED)
    canvasZipfile.write('{csvExportLocation}enrollments.csv'.format(csvExportLocation = csvExportLocation),
                        compress_type=zipfile.ZIP_DEFLATED)
    canvasZipfile.close()
    return print("Zip file created")
    


def sisIMPORT(subAccountNumber):
    path = 'v1/accounts/{account_id}/sis_imports'
    url = Canvas_base_api_url_write + path.format(account_id=Canvas_account_id)
    files = {'attachment': open('{csvExportLocation}canvasUpload-{subAccountNumber}.zip'.format(csvExportLocation = csvExportLocation,
                                                                                            subAccountNumber = subAccountNumber), 'rb')}
    headers = {'Authorization':'Bearer {token}'.format(token=CanvasSISImportToken)}
    res = requests.post(url, files=files, headers = headers)
    return print('SIS Import Complete')
    
    
def sis_import_status():
    """
    Will give the status of the last sis Import
    """
    ### Get status of last SIS imports
    path = 'v1/accounts/{account_id}/sis_imports'
    url = Canvas_base_api_url_write + path.format(account_id=Canvas_account_id)
    headers = {'Authorization':'Bearer {token}'.format(token=CanvasSISImportToken)}
    r = requests.get(url, headers=headers)
    rJson = r.json()
    print(rJson['sis_imports'][0])
    return print('Thats It')

def find_sis_user_id(search_term):
    """
    Queries by administrative users will search on SIS ID, name, or email address; non- administrative queries will 
    only be compared against name. Used to return the sis_user_id.
    In most cases, the search_term will be the login_id.
    """
    path = 'v1/accounts/1/users'
    url = Canvas_base_api_url + path.format(account_id=Canvas_account_id) + '?search_term={search_term}'.format(search_term=search_term)
    headers = {'Authorization':'Bearer {token}'.format(token=CanvasSISImportToken)}
    r = requests.get(url, headers=headers)
    rJson = r.json()
    return int(rJson[0]['sis_user_id'])
    
    
    
    
    
    
    
    
    
    
    
    