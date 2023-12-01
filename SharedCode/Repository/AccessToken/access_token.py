import time
from fyers_apiv3 import fyersModel
from urllib.parse import urlparse, parse_qs
import base64
import time
from urllib.parse import urlparse, parse_qs
import struct
import hmac
import requests
from ..Logger.logger_service import LoggerService
from ...Utils.constants import Constants

response_type = "code"
state = "sample_state"
grant_type = "authorization_code"

telemetry = LoggerService()

def totp(key, time_step=30, digits=6, digest="sha1"):
    key = base64.b32decode(key.upper() + "=" * ((8 - len(key)) % 8))
    counter = struct.pack(">Q", int(time.time() / time_step))
    mac = hmac.new(key, counter, digest).digest()
    offset = mac[-1] & 0x0F
    binary = struct.unpack(">L", mac[offset : offset + 4])[0] & 0x7FFFFFFF
    return str(binary)[-digits:].zfill(digits)


def get_token(details, tel_props):
    # Extracting details
    username = details[Constants.fyers_username]
    totp_key = details[Constants.fyers_totp_secret_key]
    client_id = details[Constants.client_id]
    pin = details[Constants.fyers_pin]
    secret_key = details[Constants.secret_key]
    redirect_uri = details[Constants.redirect_uri]
    
    telemetry.event("get_token called", tel_props)
    
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }

    s = requests.Session()
    s.headers.update(headers)

    data1 = f'{{"fy_id":"{base64.b64encode(f"{username}".encode()).decode()}","app_id":"2"}}'
    r1 = s.post("https://api-t2.fyers.in/vagator/v2/send_login_otp_v2", data=data1)
    
    max_retries = 3
    attempts = 0
    while attempts < max_retries:
        request_key = r1.json()["request_key"]
        data2 = f'{{"request_key":"{request_key}","otp":{totp(totp_key)}}}'
        r2 = s.post("https://api-t2.fyers.in/vagator/v2/verify_otp", data=data2)
        if r2.status_code == 200:
            break
        else:
            time.sleep(10)
            attempts += 1
            telemetry.warning(f"r2 failed {username}, Attempt {attempts}.. Error in r2:\n {r2.text}", tel_props)
                # Some other error, raise an exception
               
    if attempts == max_retries:
        message = f"Max retries reached. Error in r2:\n {r2.text}"
        telemetry.error(message, tel_props)
        raise Exception(message)
    
    request_key = r2.json()["request_key"]
    data3 = f'{{"request_key":"{request_key}","identity_type":"pin","identifier":"{base64.b64encode(f"{pin}".encode()).decode()}"}}'
    r3 = s.post("https://api-t2.fyers.in/vagator/v2/verify_pin_v2", data=data3)
    assert r3.status_code == 200, f"Error in r3:\n {r3.json()}"

    headers = {"authorization": f"Bearer {r3.json()['data']['access_token']}", "content-type": "application/json; charset=UTF-8"}
    data4 = f'{{"fyers_id":"{username}","app_id":"{client_id[:-4]}","redirect_uri":"{redirect_uri}","appType":"100","code_challenge":"","state":"abcdefg","scope":"","nonce":"","response_type":"code","create_cookie":true}}'
    r4 = s.post("https://api.fyers.in/api/v2/token", headers=headers, data=data4)
    assert r4.status_code == 308, f"Error in r4:\n {r4.json()}"

    parsed = urlparse(r4.json()["Url"])
    auth_code = parse_qs(parsed.query)["auth_code"][0]

    session = fyersModel.SessionModel(client_id=client_id, secret_key=secret_key, redirect_uri=redirect_uri, response_type="code", grant_type="authorization_code")
    session.set_token(auth_code)
    response = session.generate_token()
    return response["access_token"]


def get_fyers_access_token(details, tel_props):
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            telemetry.event("Starting token retrieval process", properties=tel_props)
            access_token = get_token(details, tel_props)
            telemetry.event(f"Access token fetched: {access_token}", properties=tel_props)
            return access_token
        except Exception as e:
            telemetry.warning(f"Error in fetching access token attempt no. {attempt}.\nError: {e}", properties=tel_props)
            time.sleep(10)
            continue
    
    message = f"Max retries reached. Error in fetching access token for {details['FyersUserName']}.\nError: {e}"
    telemetry.exception(message, properties=tel_props)
    raise Exception(message)