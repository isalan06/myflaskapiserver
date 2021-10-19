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
    args = request.args
    print(args)
    res = {}
    res['result']='success'
    res['errcode']=''
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)