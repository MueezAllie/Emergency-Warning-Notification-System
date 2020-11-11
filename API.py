from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pymysql
import os

# Initiate application
app = Flask(__name__)
CORS(app)
# Connecting to the Database
connection = pymysql.connect(host="localhost", user="phpmyadmin", passwd="raspberry", database="phpmyadmin")

# Creating Routes using flask_cors
@app.route('/addUser', methods=['POST'])
def add_user():
    user = None
    try:
        print(request.json)
        
        name = request.json['name']
        #print(name)
        surname = request.json['surname']
        username = request.json['username']
        email = request.json['email']
        contactNumber = request.json['contactNumber']
        addressLine1 = request.json['addressLine1']
        addressLine2 = request.json['addressLine2']
        addressLine3 = request.json['addressLine3']
        postalCode = request.json['postalCode']
        longitude = request.json['longitude']
        latitude = request.json['latitude']
        createdAt = request.json['createdAt']
        updatedAt = request.json['updatedAt']
        print("data mapped")
        with connection.cursor() as cur:

            cur.execute("INSERT INTO `users` (`name`,`surname`,`username`,`email`,`contactNumber`,`addressLine1`,`addressLine2`,`addressLine3`,`postalCode`,`longitude`,`latitude`,`createdAt`,`updatedAt`) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)", 
                (name,surname,username,email,contactNumber,addressLine1,addressLine2,addressLine3,postalCode,longitude,latitude,createdAt,updatedAt)) 
            connection.commit()
            print('new user inserted')

        user = jsonify(request.json)
        print(user)
    except:
        print('an error took place')
        user = "an Error Occured"
        
    finally:
        print('connection closed')
        print(user)
        return user

@app.route('/addDevice', methods=['POST'])
def add_device():
    device = None
    try:
        print(request.json)
        
        Type = request.json['type']
        #print(name)
        username = request.json['username']
        user = request.json['user']
        createdAt = request.json['createdAt']
        updatedAt = request.json['updatedAt']
        longitude = request.json['longitude']
        latitude = request.json['latitude']

        print("data mapped")
        with connection.cursor() as cur:

            cur.execute("INSERT INTO `devices` (`type`,`username`,`user`,`createdAt`,`updatedAt`,`longitude`,`latitude`) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                (Type,username,user,createdAt,updatedAt,longitude,latitude)) 
            connection.commit()
            print('new device inserted')
            
        
            
        device = jsonify(request.json)
        print(device)
    except:
        print('an error took place')
        device = "an Error Occured"
        
    finally:
        print('connection closed')
        print(device)
        return device

@app.route('/addAgency', methods=['POST'])
def add_agency():
    user = None
    try:
        print(request.json)
        
        name = request.json['name']
        #print(name)
        departmentType = request.json['type']
        email = request.json['email']
        contactNumber = request.json['contactNumber']
        addressLine1 = request.json['addressLine1']
        addressLine2 = request.json['addressLine2']
        addressLine3 = request.json['addressLine3']
        postalCode = request.json['postalCode']
        longitude = request.json['longitude']
        latitude = request.json['latitude']
        createdAt = request.json['createdAt']
        updatedAt = request.json['updatedAt']
        print("data mapped")
        with connection.cursor() as cur:
            sqlquery = f"INSERT INTO `{departmentType}` (`name`,`email`,`contactNumber`,`addressLine1`,`addressLine2`,`addressLine3`,`postalCode`,`longitude`,`latitude`,`createdAt`,`updatedAt`) VALUES ('{name}', '{email}', '{contactNumber}','{addressLine1}', '{addressLine2}', '{addressLine3}','{postalCode}', '{longitude}', '{latitude}','{createdAt}', '{updatedAt}')"
            print(sqlquery)
            cur.execute(sqlquery) 
            connection.commit()
            print('new user inserted')

        user = jsonify(request.json)
        print(user)
    except:
        print('an error took place')
        user = "an Error Occured"
        
    finally:
        print('connection closed')
        print(user)
        return user

@app.route('/listAll', methods=['GET'])
def list_all():
    data = {}
    try:
        cursor = connection.cursor()
        print('start')
        print(request.json)
        retrieve = f"SELECT * FROM devices;"
        cursor.execute(retrieve)
        devices = cursor.fetchall()
        print('devices: ')
        print(devices)
        
        retrieve = f"SELECT * FROM users;"
        cursor.execute(retrieve)
        users = cursor.fetchall()
        print('users: ')
        print(users)

        retrieve = f"SELECT * FROM FireDepartmentDB;"
        cursor.execute(retrieve)
        FireDepartmentDB = cursor.fetchall()
        print('FireDepartmentDB: ')
        print(FireDepartmentDB)
        
        retrieve = f"SELECT * FROM EmergencyMedicalServicesDB;"
        cursor.execute(retrieve)
        EmergencyMedicalServicesDB = cursor.fetchall()
        print('EmergencyMedicalServicesDB: ')
        print(EmergencyMedicalServicesDB)
        
        retrieve = f"SELECT * FROM PoliceDepartmentDB;"
        cursor.execute(retrieve)
        PoliceDepartmentDB = cursor.fetchall()
        print('PoliceDepartmentDB: ')
        print(PoliceDepartmentDB)
        
        data['devices'] = devices
        data['users'] = users
        data['FireDepartmentDB'] = FireDepartmentDB
        data['EmergencyMedicalServicesDB'] = EmergencyMedicalServicesDB
        data['PoliceDepartmentDB'] = PoliceDepartmentDB
        print('data: ')
        print(data)        
        data = jsonify(data)

    except:
        print('an error took place')
        data = "an Error Occured"
        
    finally:
        print('connection closed')
        return data

@app.route('/listUsers', methods=['GET'])
def list_users():
    data = {}
    try:
        cursor = connection.cursor()
        
        retrieve = f"SELECT * FROM users;"
        cursor.execute(retrieve)
        users = cursor.fetchall()
        print('users: ')
        print(users)

        data['users'] = users

        print('data: ')
        print(data)        
        data = jsonify(data)

    except:
        print('an error took place')
        data = "an Error Occured"
        
    finally:
        print('connection closed')
        return data

@app.route('/listAgencies', methods=['GET'])
def list_agencies():
    data = {}
    try:
        cursor = connection.cursor()
        
        retrieve = f"SELECT * FROM FireDepartmentDB;"
        cursor.execute(retrieve)
        FireDepartmentDB = cursor.fetchall()
        print('FireDepartmentDB: ')
        print(FireDepartmentDB)
        
        retrieve = f"SELECT * FROM EmergencyMedicalServicesDB;"
        cursor.execute(retrieve)
        EmergencyMedicalServicesDB = cursor.fetchall()
        print('EmergencyMedicalServicesDB: ')
        print(EmergencyMedicalServicesDB)
        
        retrieve = f"SELECT * FROM PoliceDepartmentDB;"
        cursor.execute(retrieve)
        PoliceDepartmentDB = cursor.fetchall()
        print('PoliceDepartmentDB: ')
        print(PoliceDepartmentDB)
        
        data['FireDepartmentDB'] = FireDepartmentDB
        data['EmergencyMedicalServicesDB'] = EmergencyMedicalServicesDB
        data['PoliceDepartmentDB'] = PoliceDepartmentDB

        print('data: ')
        print(data)        
        data = jsonify(data)

    except:
        print('an error took place')
        data = "an Error Occured"
        
    finally:
        print('connection closed')
        return data


@app.route('/listDevices/<id>', methods=['GET'])
def list_devices(id):
    data = {}
    try:
        cursor = connection.cursor()
        
        retrieve = f"SELECT * FROM devices WHERE user='{id}';"
        cursor.execute(retrieve)
        devices = cursor.fetchall()
        print('devices: ')
        print(devices)

        data['devices'] = devices

        print('data: ')
        print(data)        
        data = jsonify(data)
    except:
        print('an error took place')
        data = "an Error Occured"
        
    finally:
        print('connection closed')
        return data


@app.route('/deleteFD/<id>', methods=['DELETE'])
def delete_fireDepartment(id):
    data = {}
    try:
        print(id)
        with connection.cursor() as cur:
            sqlquery = f"DELETE FROM `FireDepartmentDB` WHERE id = '{id}';"
            #sqlquery = f"INSERT INTO `{departmentType}` (`name`,`email`,`contactNumber`,`addressLine1`,`addressLine2`,`addressLine3`,`postalCode`,`longitude`,`latitude`,`createdAt`,`updatedAt`) VALUES ('{name}', '{email}', '{contactNumber}','{addressLine1}', '{addressLine2}', '{addressLine3}','{postalCode}', '{longitude}', '{latitude}','{createdAt}', '{updatedAt}')"
            print(sqlquery)
            cur.execute(sqlquery) 
            connection.commit()
            print('deleted')

        data['FireDepartmentDB'] = id

        print('data: ')
        print(data)        
        data = jsonify(data)
    except:
        print('an error took place')
        data = "an Error Occured"
        
    finally:
        print('connection closed')
        return data


@app.route('/deleteEMS/<id>', methods=['DELETE'])
def delete_EmergencyMedicalServices(id):
    data = {}
    try:
        print(id)
        with connection.cursor() as cur:
            sqlquery = f"DELETE FROM `EmergencyMedicalServicesDB` WHERE id = '{id}';"
            #sqlquery = f"INSERT INTO `{departmentType}` (`name`,`email`,`contactNumber`,`addressLine1`,`addressLine2`,`addressLine3`,`postalCode`,`longitude`,`latitude`,`createdAt`,`updatedAt`) VALUES ('{name}', '{email}', '{contactNumber}','{addressLine1}', '{addressLine2}', '{addressLine3}','{postalCode}', '{longitude}', '{latitude}','{createdAt}', '{updatedAt}')"
            print(sqlquery)
            cur.execute(sqlquery) 
            connection.commit()
            print('deleted')

        data['EmergencyMedicalServicesDB'] = id

        print('data: ')
        print(data)        
        data = jsonify(data)
    except:
        print('an error took place')
        data = "an Error Occured"
        
    finally:
        print('connection closed')
        return data

@app.route('/deletePD/<id>', methods=['DELETE'])
def delete_PoliceDepartment(id):
    data = {}
    try:
        print(id)
        with connection.cursor() as cur:
            sqlquery = f"DELETE FROM `PoliceDepartmentDB` WHERE id = '{id}';"
            #sqlquery = f"INSERT INTO `{departmentType}` (`name`,`email`,`contactNumber`,`addressLine1`,`addressLine2`,`addressLine3`,`postalCode`,`longitude`,`latitude`,`createdAt`,`updatedAt`) VALUES ('{name}', '{email}', '{contactNumber}','{addressLine1}', '{addressLine2}', '{addressLine3}','{postalCode}', '{longitude}', '{latitude}','{createdAt}', '{updatedAt}')"
            print(sqlquery)
            cur.execute(sqlquery) 
            connection.commit()
            print('deleted')

        data['PoliceDepartmentDB'] = id

        print('data: ')
        print(data)        
        data = jsonify(data)
    except:
        print('an error took place')
        data = "an Error Occured"
        
    finally:
        print('connection closed')
        return data

@app.route('/deleteUser/<id>', methods=['DELETE'])
def delete_users(id):
    data = {}
    try:
        print(id)
        with connection.cursor() as cur:
            sqlquery = f"DELETE FROM `users` WHERE id = '{id}';"
            #sqlquery = f"INSERT INTO `{departmentType}` (`name`,`email`,`contactNumber`,`addressLine1`,`addressLine2`,`addressLine3`,`postalCode`,`longitude`,`latitude`,`createdAt`,`updatedAt`) VALUES ('{name}', '{email}', '{contactNumber}','{addressLine1}', '{addressLine2}', '{addressLine3}','{postalCode}', '{longitude}', '{latitude}','{createdAt}', '{updatedAt}')"
            print(sqlquery)
            cur.execute(sqlquery) 
            connection.commit()
            print('deleted')

        data['users'] = id

        print('data: ')
        print(data)        
        data = jsonify(data)
    except:
        print('an error took place')
        data = "an Error Occured"
        
    finally:
        print('connection closed')
        return data
        
@app.route('/deleteDevice/<id>', methods=['DELETE'])
def delete_devices(id):
    data = {}
    try:
        print(id)
        with connection.cursor() as cur:
            sqlquery = f"DELETE FROM `devices` WHERE id = '{id}';"
            #sqlquery = f"INSERT INTO `{departmentType}` (`name`,`email`,`contactNumber`,`addressLine1`,`addressLine2`,`addressLine3`,`postalCode`,`longitude`,`latitude`,`createdAt`,`updatedAt`) VALUES ('{name}', '{email}', '{contactNumber}','{addressLine1}', '{addressLine2}', '{addressLine3}','{postalCode}', '{longitude}', '{latitude}','{createdAt}', '{updatedAt}')"
            print(sqlquery)
            cur.execute(sqlquery) 
            connection.commit()
            print('deleted')

        data['devices'] = id

        print('data: ')
        print(data)        
        data = jsonify(data)
    except:
        print('an error took place')
        data = "an Error Occured"
        
    finally:
        print('connection closed')
        return data

# Run Server
if __name__ == '__main__':
  app.run(host='0.0.0.0')
