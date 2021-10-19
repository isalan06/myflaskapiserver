from flask import Flask, request, jsonify
import os
import pymysql

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

    res = {}
    res['result']='success'
    res['errcode']=''
    return jsonify(res)

db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "alan",
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
            print(command)

            number = cursor.execute(command)
            print(number)


    except Exception as ex:
        print(ex)

    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)