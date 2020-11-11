import requests

url = "http://localhost:5000/listDevices/8"
x = requests.get(url)
print(x.text)