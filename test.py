import requests
import pyotp

BASE = "http://127.0.0.1:5000/"
totp = pyotp.TOTP('base32secret3232')

username = "trump"
otp = totp.now()
print(otp)
payload = {"name": "donald trump", "password": "USA", "otp": otp}
response = requests.put(BASE + "user/" + str(username), payload)
print(response.json())

username = "modi"
otp = totp.now()
print(otp)
payload = {"name": "narendra modi", "password": "INDIA", "otp": otp}
response = requests.put(BASE + "user/" + str(username), payload)
print(response.json())

response = requests.get(BASE + "user/modi")
print(response.json())

username = "trump"
otp = totp.now()
payload = {"name": "joe biden"}
response = requests.patch(BASE + "user/" + str(username), payload)
print(response.json())
