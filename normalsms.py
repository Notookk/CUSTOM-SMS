import requests
import json

url = 'http://202.51.182.198:8181/nbp/sms/code'
headers = {
    'User-Agent': 'okhttp/3.11.0',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer',  # You should put the actual token here if you have one
    'language': 'en',
    'timeZone': 'Asia/Dhaka'
}

receiver = input("Enter the receiver's phone number: ")
captcha_code = input("Enter Massage: ")
custom_text = f"{captcha_code}"
title = "Register Account"

data = {
    "receiver": receiver,
    "text": custom_text,
    "title": title
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.status_code)
print(response.json())
