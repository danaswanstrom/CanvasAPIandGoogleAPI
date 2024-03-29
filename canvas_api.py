import zipfile
import requests
import config
from os.path import basename
import json

# Configuration information needs to be in a config.py file in the same directory

# Post csv or zip file for Sis Import. Just change the file name.


def create_zip(subAccountNumber):
    canvas_zipfile = zipfile.ZipFile('{}canvasUpload-{}.zip'
                                    .format(config.csvExportLocation, subAccountNumber), 'w')

    canvas_zipfile.write('{}courses.csv'.format(config.csvExportLocation),
                         arcname=basename('{}courses.csv'.format(config.csvExportLocation)),
                         compress_type=zipfile.ZIP_DEFLATED)

    canvas_zipfile.write('{}enrollments.csv'.format(config.csvExportLocation),
                         arcname=basename('{}enrollments.csv'.format(config.csvExportLocation)),
                         compress_type=zipfile.ZIP_DEFLATED)
    canvas_zipfile.close()
    return print("Zip file created")


def sisIMPORT(subAccountNumber):
    path = 'v1/accounts/{account_id}/sis_imports'
    url = config.Canvas_base_api_url_write + path.format(account_id=config.Canvas_account_id)
    files = {'attachment': open('{csvExportLocation}canvasUpload-{subAccountNumber}.zip'
                                .format(csvExportLocation=config.csvExportLocation,
                                        subAccountNumber=subAccountNumber), 'rb')}
    headers = {'Authorization': 'Bearer {token}'.format(token=config.CanvasSISImportToken)}
    res = requests.post(url, files=files, headers=headers)
    return print('SIS Import Complete')


def sis_import_status():
    """
    Will give the status of the last sis Import
    """
    # Get status of last SIS imports
    path = 'v1/accounts/{account_id}/sis_imports'
    url = config.Canvas_base_api_url_write + path.format(account_id=config.Canvas_account_id)
    headers = {'Authorization': 'Bearer {token}'.format(token=config.CanvasSISImportToken)}
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
    url = config.Canvas_base_api_url + path.format(
        account_id=config.Canvas_account_id) + '?search_term={search_term}'.format(search_term=search_term)
    headers = {'Authorization': 'Bearer {token}'.format(token=config.CanvasSISImportToken)}
    r = requests.get(url, headers=headers)
    rJson = r.json()
    try:
        sis_id = int(rJson[0]['sis_user_id'])
    except:
        sis_id = 'Unknown'
    return sis_id
