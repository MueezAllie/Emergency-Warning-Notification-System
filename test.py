import requests

url = "http://localhost:5000/addUser"
myObj = {"name": "Yaseen","surname": "Sulaiman","username": "Suly","email": "sulaimanyaseen@gmail.com","contactNumber": "0796944536","addressLine1": "59 Saturn Road","addressLine2":"Surrey Estate","addressLine3":"Cape Town", "postalCode": 7764,"longitude":"18.528240","latitude":"-33.968490","createdAt":"2020-10-17 21:00:00","updatedAt": "2020-10-17 21:00:00"}
x = requests.post(url,headers={"Content-Type":"application/json"}, json=myObj)
print(x.text)