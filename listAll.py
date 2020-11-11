import requests

url = "http://localhost:5000/listAll"
x = requests.get(url)
print(x.text)