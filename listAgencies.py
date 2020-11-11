import requests

url = "http://localhost:5000/listAgencies"
x = requests.get(url)
print(x.text)