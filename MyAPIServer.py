from flask import flask
from flask import request

app = Flask(__name__)

@app.route('/GoogleDriveAPI/')
def GoogleDriveAPIFun():
    return "Hello"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)