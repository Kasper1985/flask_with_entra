from flask import Flask, request, render_template, redirect, url_for
from status import Status
from deviceCode_response import DeviceCodeResponse
from urllib.parse import quote

import sys, requests
import configurations
import datetime

app = Flask(__name__)
status = None
access_token = None


# Index webpage as a start page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/device')
def deviceLogin():
    status = request.args.get('status')
    play = request.args.get('play')
    poling = request.args.get('poling')
    if play:
        status = Status()
        scope = quote("openid " + " ".join(configurations.SCOPE))
        url = f"{configurations.DEVICE_URL}?client_id={configurations.CLIENT_ID}&scope={scope}"
        writeLog("Request device code: " + url, status)
        result = requests.get(url)
        if result.status_code != 200:
            response = result.json()
            writeLog(f"Error: {response['error']} - {response['error_description']}", status)
            return render_template('device.html', status=status)
        else:
            response = DeviceCodeResponse.from_dict(result.json())
            writeLog(f"Response:\n{response}", status)
            return render_template('device.html', status=status, poling=response)
    if poling:
        result = devicePoling(poling.device_code)
        if result:
            return render_template(url_for('device', status=status))
        else:
            return render_template('device.html', status=status, poling=poling)
    return render_template('device.html', status=status)
    


def devicePoling(device_code: str) -> bool:
    global status
    global access_token
    body = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "client_id": configurations.CLIENT_ID,
        "device_code": device_code,
    }
    writeLog("Request token through poling", status)
    result = requests.post(configurations.TOKEN_URL, data=body)
    if result.status_code != 200:
        response = result.json()
        writeLog(f"Error: {response['error']} - {response['error_description']}", status)
        return False
    else:
        response = result.json()
        writeLog(f"Response:\n{response}", status)
        return True


@app.route('/code')
def codeLogin():
    return render_template('code.html')


def writeLog(log: str, status: Status = None):
    if status is not None:
        status.addEntry(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), log)
    print(log)
    

if __name__ == "__main__":
    is_debug = False
    for arg in sys.argv:
        if arg == "--debug":
            is_debug = True

    app.run(host='localhost', port=5000, debug=is_debug)