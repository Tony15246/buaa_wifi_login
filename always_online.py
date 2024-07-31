import os
import sys
import time
import json
import requests
from buaa_wifi_login import ensure_login

def is_connect_internet(testurl):
    try:
        headers = {'Cache-Control': 'no-cache'}
        response = requests.get(testurl, headers=headers, timeout=5)
        if response.status_code == 200 and response.text and "gw.buaa.edu.cn" not in response.text:
            return True
        elif response.status_code == 304 and "gw.buaa.edu.cn" not in response.text:
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Error during connectivity check: {e}")
        return False

def always_login(username, password, testurl, checkinterval):
    timestamp = lambda : print(time.asctime(time.localtime(time.time())))

    timestamp()
    try:
        ensure_login(username, password)
    except Exception as e:
        print(f"Error during initial login: {e}")
    while 1:
        try:
            time.sleep(checkinterval)
            if not is_connect_internet(testurl):
                timestamp()
                ensure_login(username, password)
            else:
                print("Internet connection is stable.")
        except KeyboardInterrupt:
            print("User Exit.")
            sys.exit(0)
        except Exception as e:
            print(f"Error during reconnect: {e}")
        
if __name__ == "__main__":
    with open('config.json', 'r') as file:
        config = json.load(file)
    username = config['username']
    password = config['password']

    testurl = "https://www.baidu.com"
    checkinterval = 5 * 60

    always_login(username, password, testurl, checkinterval)