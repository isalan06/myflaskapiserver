import os.path
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refresh Creds")
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        q="mimeType = 'application/vnd.google-apps.folder' and '0ALNhV0hP-QYDUk9PVA' in parents",
        pageSize=100, fields="nextPageToken, files(id, name, parents)").execute()
    items = results.get('files', [])

    pic_id = ''

    if not items:
        print('No files found.')
    else:
        print('1st Files:')
        for item in items:
            if item['name']=='KIOSK Picture':
                pic_id = item['id']
            print(u'{0} ({1}) - {2}'.format(item['name'], item['id'], item['parents']))
    #print(pic_id)

    # Check Machine ID
    q_str = "mimeType = 'application/vnd.google-apps.folder' and '" + str(pic_id) +"' in parents"
    #print(q_str)
    results = service.files().list(
        q=q_str, #"mimeType = 'application/vnd.google-apps.folder' and '" + str(pic_id) +"' in parents",
        pageSize=10, fields="nextPageToken, files(id, name, parents)").execute()
    items = results.get('files', [])

    bHasBaseFolder = False
    sMachineID = 'Test_MachineID'
    sMachineID_ID = ''
    if not items:
        print('No files found.')
    else:
        print('2nd Files:')
        for item in items:
            if item['name']==sMachineID:
                bHasBaseFolder = True
                sMachineID_ID = item['id']
            print(u'{0} ({1}) - {2}'.format(item['name'], item['id'], item['parents']))
    
    if bHasBaseFolder == False:
        file_metadata = {
            'name': sMachineID,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [str(pic_id)]
        }
        file = service.files().create(body=file_metadata,
                                    fields='id').execute()
        sMachineID_ID = str(file.get('id'))
        print('Folder ID: %s' % file.get('id'))

    #print(sMachineID_ID)        

    # Check Date Folder
    sTodayDateString = datetime.now().strftime("%Y%m%d")	
    sTodayDate_ID = ''
    bHasBaseFolder = False
    q_str = "mimeType = 'application/vnd.google-apps.folder' and '" + str(sMachineID_ID) +"' in parents"
    results = service.files().list(
        q=q_str,
        pageSize=10, fields="nextPageToken, files(id, name, parents)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('3nd Files:')
        for item in items:
            if item['name']==sTodayDateString:
                bHasBaseFolder = True
                sTodayDate_ID = item['id']
            print(u'{0} ({1}) - {2}'.format(item['name'], item['id'], item['parents']))
    if bHasBaseFolder == False:
        file_metadata = {
            'name': sTodayDateString,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [str(sMachineID_ID)]
        }
        file = service.files().create(body=file_metadata,
                                    fields='id').execute()
        sTodayDate_ID = str(file.get('id'))
        print('Folder ID: %s' % file.get('id'))

    #Check Test Location
    sTestLocation='我是測試考場(真的是測試用)'
    sTestLocation_ID = ''
    bHasBaseFolder = False
    q_str = "mimeType = 'application/vnd.google-apps.folder' and '" + str(sTodayDate_ID) +"' in parents"
    results = service.files().list(
        q=q_str,
        pageSize=10, fields="nextPageToken, files(id, name, parents)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('4nd Files:')
        for item in items:
            if item['name']==sTestLocation:
                bHasBaseFolder = True
                sTestLocation_ID = item['id']
            print(u'{0} ({1}) - {2}'.format(item['name'], item['id'], item['parents']))
    if bHasBaseFolder == False:
        file_metadata = {
            'name': sTestLocation,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [str(sTodayDate_ID)]
        }
        file = service.files().create(body=file_metadata,
                                    fields='id').execute()
        sTestLocation_ID = str(file.get('id'))
        print('Folder ID: %s' % file.get('id'))

    sTestLocation_ID = CreateGoogleDriveFolder(service, sTestLocation, sTodayDate_ID)
    print('Check Function')
    print(sTestLocation_ID)

def CreateGoogleDriveFolder(service, titlestring, folderid):
    returnfolderid=''

    bHasFolder = False
    q_str = "mimeType = 'application/vnd.google-apps.folder' and '" + str(folderid) +"' in parents"
    results = service.files().list(
        q=q_str,
        pageSize=10, fields="nextPageToken, files(id, name, parents)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        for item in items:
            if item['name']==titlestring:
                bHasFolder = True
                returnfolderid = item['id']
            print(u'{0} ({1}) - {2}'.format(item['name'], item['id'], item['parents']))
    if bHasFolder == False:
        try:
            file_metadata = {
                'name': titlestring,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [str(folderid)]
            }
            file = service.files().create(body=file_metadata,
                                        fields='id').execute()
            returnfolderid = str(file.get('id'))
            print('Folder ID: %s' % file.get('id'))
        except Exception as ex:
            print(ex)

    return returnfolderid
    

if __name__ == '__main__':
    main()