from flask import Flask, request, render_template, redirect, url_for
from flask_session import Session
from status import Status
from deviceCode_response import DeviceCodeResponse
from token_response import TokenResponse
from urllib.parse import quote

import sys, requests
import configurations
import datetime

app = Flask(__name__)
app.config['SESSION_TYPE'] = configurations.SESSION_TYPE
Session(app)

status = Status()
access_token = None
state = 'FsGJ0xp85jGVHhlLEU72XRS3oSQSkBwk'


# Index webpage as a start page
@app.route('/')
def index():
    global status, access_token
    status = Status()
    access_token = None
    return render_template('index.html')


@app.route('/get_data')
def getData():
    user = requests.get(configurations.API_ENDPOINT_USER, headers={'Authorization': f'Bearer {access_token}'}).json()
    messages = requests.get(configurations.API_ENDPOINT_MESSAGES, headers={'Authorization': f'Bearer {access_token}'}).json()
    return render_template('get_data.html', user=user, messages=messages)


@app.route('/device')
def deviceLogin():
    global status, access_token
    play = request.args.get('play')
    device_code = request.args.get('device_code')
    if play:
        scope = quote("openid " + " ".join(configurations.SCOPE))
        url = f"{configurations.DEVICE_URL}?client_id={configurations.CLIENT_ID}&scope={scope}"
        writeLog("Request device code: " + url, status)
        result = requests.get(url)
        if result.status_code != 200:
            response = result.json()
            writeLog(f"Error: {response['error']} - {response['error_description']}", status)
            return render_template('device.html', status=status)
        else:
            result = DeviceCodeResponse.from_dict(result.json())
            writeLog(f"Response:\n{result}", status)
            device_code = result.device_code
            return render_template('device.html', status=status, device_code=device_code)
    if device_code:
        result = devicePoling(device_code)
        if result:
            return render_template('device.html', status=status, access_token=access_token)
        else:
            return render_template('device.html', status=status, device_code=device_code)
    if access_token:
        return render_template('device.html', status=status, access_token=access_token)
    return render_template('device.html', status=status)


def devicePoling(device_code: str) -> bool:
    global status
    global access_token
    body = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "client_id": configurations.CLIENT_ID,
        "device_code": device_code,
    }
    result = requests.post(configurations.TOKEN_URL, data=body)
    if result.status_code != 200:
        response = result.json()
        writeLog(f"Error: {response['error']} - {response['error_description']}", status)
        return False
    else:
        response = result.json()
        token_response = TokenResponse.from_dict(response)
        writeLog(f"Response:\n{token_response}", status)
        access_token = token_response.access_token
        return True


@app.route('/code')
def codeLogin():
    global status, access_token, state
    play = request.args.get('play')
    if play:
        scope = quote("openid " + " ".join(configurations.SCOPE))
        url = f"""{configurations.AUTHORIZE_URL}?
        response_type=code&
        scope={scope}&
        client_id={configurations.CLIENT_ID}&
        state={state}&
        redirect_uri={quote(f"{configurations.HOST_URL}/callback", safe='')}"""
        writeLog("Navigate to: " + url, status)
        return redirect(url.replace("\n", ""))
    if access_token:
        return render_template('code.html', status=status, access_token=access_token)
    return render_template('code.html', status=status)


@app.route('/callback')
def callback():
    global status, access_token, state
    if request.args.get('state') != state:
        writeLog("Error: State does not match", status)
        return redirect(url_for('codeLogin'))
    code = request.args.get('code')
    if code:
        token = get_token(code)
        if token:
            access_token = token.access_token
        else:
            writeLog("Error: Could not get token", status)
    return redirect(url_for('codeLogin'))


def get_token(code: str):
    global status
    body = {
            "grant_type": "authorization_code",
            "client_id": configurations.CLIENT_ID,
            "client_secret": configurations.CLIENT_SECRET,
            "code": code,
            "redirect_uri": f"{configurations.HOST_URL}/callback",
        }
    writeLog(f"Request token:\n{'\n'.join(key + ': ' + str(value) for key, value in body.items()).replace(configurations.CLIENT_SECRET, configurations.CLIENT_SECRET[:4] + '*' * (len(configurations.CLIENT_SECRET) - 4))}", status)
    response = requests.post(configurations.TOKEN_URL, data=body)
    if response.status_code != 200:
        response = response.json()
        writeLog(f"Error: {response['error']} - {response['error_description']}", status)
        return None
    else:
        response = response.json()
        token_response = TokenResponse.from_dict(response)
        writeLog(f"Response:\n{token_response}", status)
        return token_response


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