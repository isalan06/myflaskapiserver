from flask import Flask, request, jsonify

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
    print(_sn)
    print(_filename)
    print(_datetime)

    res = {}
    res['result']='success'
    res['errcode']=''
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)