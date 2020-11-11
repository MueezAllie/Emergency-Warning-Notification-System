import requests

url = "http://localhost:5000/listUsers"
x = requests.get(url)
print(x.text)