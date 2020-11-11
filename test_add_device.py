import requests

url = "http://localhost:5000/addDevice"
myObj = {"type": "Fire Detector","username": "device1","user": 7,"longitude":"18.528240","latitude":"-33.968490","createdAt":"2020-10-17 21:00:00","updatedAt": "2020-10-17 21:00:00"}
x = requests.post(url,headers={"Content-Type":"application/json"}, json=myObj)
print(x.text)
