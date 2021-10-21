from flask import Flask, request, jsonify
import os
import pymysql
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

app = Flask(__name__)

@app.route('/')
def index():
    return "Base"

@app.route('/GoogleDriveAPI/')
def GoogleDriveAPIFun():
    return "Google Drive API"

@app.route('/GoogleDriveAPI/UpdateRegularImage', methods=['POST'])
def GDA_UpdateRegularImage():
    print('Update Regular Image')
    _sn = request.args['sn']
    _filename= request.args['filename']
    _datetime = request.args['datetime']
    #print(_sn)
    #print(_filename)
    #print(_datetime)
    
    baseFolderString = os.path.join(os.sep, 'D:' + os.sep, 'Data', 'IoTGateway', str(_sn))
    #print(baseFolderString) 
    if not os.path.isdir(baseFolderString):
        os.mkdir(baseFolderString)
    imageFolderString = os.path.join(os.sep, baseFolderString, 'Image')
    #print(imageFolderString)
    if not os.path.isdir(imageFolderString):
        os.mkdir(imageFolderString)
    timeFolderString = os.path.join(os.sep, imageFolderString, str(_datetime)[:8])
    #print(timeFolderString)
    if not os.path.isdir(timeFolderString):
        os.mkdir(timeFolderString)
    saveFileNameString = os.path.join(os.sep, timeFolderString, _filename)
    #print(saveFileNameString)

    f = request.data
    #print(f)
    with open(saveFileNameString, "wb") as binary_file:
        binary_file.write(f)

    image_code = getUpdateGDImageCode(_sn)
    if image_code != '':
        try:
            cred_folderString = os.path.join(os.sep, os.path.abspath(os.path.dirname(__file__)), 'iotgwgoogledrive')
            #print(cred_folderString)
            cred_filenameString = os.path.join(os.sep, cred_folderString, 'token.json')
            #print(cred_filenameString)
            clientcred_filenameString = os.path.join(os.sep, cred_folderString ,'client_secrets.json')

            creds = None

            if os.path.exists(cred_filenameString):
                #print("GD1")
                creds = Credentials.from_authorized_user_file(cred_filenameString, SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                #print("GD2")
                if creds and creds.expired and creds.refresh_token:
                    #print("GD3")
                    creds.refresh(Request())
                else:
                    #print("GD4")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        clientcred_filenameString, SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(cred_filenameString, 'w') as token:
                    token.write(creds.to_json())

            service = build('drive', 'v3', credentials=creds)

            folder_id = image_code
            file_metadata = {
                'name': _filename,
                'parents': [folder_id]
            }

            media = MediaFileUpload(saveFileNameString,
                        mimetype='image/jpeg',
                        resumable=True)
            
            _file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()

            print('Update Image To Google Drive Success')


        except Exception as ex:
            print(ex)
            res2 = {}
            res2['result']='failure'
            res2['errcode']='Update Image To Google Drive happen error:' + str(ex)
            return jsonify(res2)
    res = {}
    res['result']='success'
    res['errcode']=''
    return jsonify(res)

@app.route('/TABFKIOSKAPI/GetGoogleDriveFolderID', methods=['GET'])
def TABF_GetGoogleDriveFolderID():
    print('Get Google Drive Folder ID')
    _machineid = request.args['MachineID']
    _testtime= request.args['TestTime']
    _testlocation = request.args['TestLocation']
    _result_id = ''

    print(_machineid)
    print(_testtime)
    print(_testlocation)

    res = {}
    res['result']='success'
    res['errcode']=''
    res['folderid']=_result_id
    
    return jsonify(res)


db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "db": "gd_db",
    "charset": "utf8"
}


def getUpdateGDImageCode(machineid):
    result = ''

    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:
            command = 'SELECT image_code FROM table_googledrivecode WHERE machine_id = \'' + str(machineid) + '\''
            #print(command)

            number = cursor.execute(command)
            #print(number)

            if number > 0:
                data = cursor.fetchone()
                result = data[0]
                #print(result)
    except Exception as ex:
        print(ex)

    return result

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)