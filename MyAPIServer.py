from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return "Base"

@app.route('/GoogleDriveAPI/')
def GoogleDriveAPIFun():
    return "Google Drive API"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)