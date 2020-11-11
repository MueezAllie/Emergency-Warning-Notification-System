import paho.mqtt.client as paho
import json
import pymysql
import haversine as hs
import os
from datetime import datetime
import requests

# Connecting to the pymysql database
connection = pymysql.connect(host="localhost", user="phpmyadmin", passwd="raspberry", database="phpmyadmin")
cursor = connection.cursor()
alertUrl = "http://localhost:5000/alert"

print("")

# Send Email function for nearby users
def send_emails(user, email, sensor, address, gpsLoc, timestamp, emer_serv):
#     print("\n\nEnter Send Email for Nearby Users")
    
    if sensor == "Fire Detector":
        typ = "A Fire has been detected at"
    
    elif sensor == "Flood Detector":
        typ = "A Flood is expected to occur in"
        
    elif sensor == "Wind Disaster Detector":
        typ = "A Wind related disaster is expected to occur in"
        
    elif sensor == "Security Alarm":
        typ = "A breach in the security system has been detected at"
        
    elif sensor == "Critical Emergency Button":
        typ = "A Critical Emergency has been logged at"
        
#     f=open("email.txt","w+")

#     f.write(f"To: {email}\n")
#     f.write(f"From: mueez.allie@gmail.com\n")
#     f.write(f"Subject: EMERGENCY ALERT!\n")
#     f.write(f"To {user}\n\nEMERGENCY ALERT!\n{typ}:\n\n{address}.\n\nThe GPS Co-ordinates are:\n{gpsLoc} \n\nThe Sensors were triggered at {timestamp}.\n\n{emer_serv} have been contacted.")

#     f.close()

#     os.system(f"cat email.txt | msmtp -a default {email}")
#     print("\n\nExit Send Email for Nearby Users")

    #return "sent email"

# Send Email function for user where emergency was logged
def send_email(user, email, sensor, address, gpsLoc, timestamp, emer_serv, dummy):
#     print("\n\nEnter Send Email for User of sensor")

    
    if sensor == "Fire Detector":
        typ = "A Fire has been detected at"
    
    elif sensor == "Flood Detector":
        typ = "A Flood is expected to occur in"
        
    elif sensor == "Wind Disaster Detector":
        typ = "A Wind related disaster is expected to occur in"
        
    elif sensor == "Security Alarm":
        typ = "A breach in the security system has been detected at"
        
    elif sensor == "Critical Emergency Button":
        typ = "A Critical Emergency has been logged at"
        
    '''f=open("email.txt","w+")

    f.write(f"To: {email}\n")
    f.write(f"From: mueez.allie@gmail.com\n")
    f.write(f"Subject: EMERGENCY ALERT!\n")
    f.write(f"\nEMERGENCY ALERT for {user}! \n{typ} your premises:\n\n{address}.\n\nThe GPS Co-ordinates are:\n{gpsLoc} \n\nThe Sensors were triggered at {timestamp}.\n\n{emer_serv} have been contacted.")

    f.close()

    os.system(f"cat email.txt | msmtp -a default {email}")
#     print("\n\nExit Send Email for User of sensor")
    return "sent email"'''

# Send Email function for emergency services
def email_emer_serv(email, sensor, address, gpsLoc, timestamp, emer_serv):
#     print("\n\nEnter Send Email for Emergency Services")

    
    if sensor == "Fire Detector":
        typ = "A Fire has been detected at"
    
    elif sensor == "Flood Detector":
        typ = "A Flood is expected to occur in"
        
    elif sensor == "Wind Disaster Detector":
        typ = "A Wind related disaster is expected to occur in"
        
    elif sensor == "Security Alarm":
        typ = "A breach in the security system has been detected at"
        
    elif sensor == "Critical Emergency Button":
        typ = "A Critical Emergency has been logged at"
        
    '''f=open("email.txt","w+")

    f.write(f"To: {email}\n")
    f.write(f"From: mueez.allie@gmail.com\n")
    f.write(f"Subject: EMERGENCY ALERT!\n")
    f.write(f"\nEMERGENCY ALERT for {emer_serv}! \n{typ}:\n\n{address}.\n\nThe GPS Co-ordinates are:\n{gpsLoc} \n\nThe Sensors were triggered at {timestamp}.")

    f.close()

    os.system(f"cat email.txt | msmtp -a default {email}")
#     print("\n\nExit Send Email for Emergency Services")

    return "sent email"'''

# Function to get sensing device information from the devices database
def get_device(device):
#     print("\n\nEnter get_device")

    # Retrieving the information
    retrieve = f"SELECT * FROM devices WHERE username='{device}';"
    cursor.execute(retrieve)
    # Getting the information of the sensing device that was triggered
    data = cursor.fetchall()[0]
#     print("\n\nExit get_device")
    return data

# Function to pull the information of the entire users database
def get_users():
#     print("\n\nEnter get_users")
    retrieve = "SELECT * FROM users;"
    cursor.execute(retrieve)
    data = cursor.fetchall()
#     print("\n\nUsers = ", data)
#     print("\n\nExit get_users")
    return data

# Function to get and store all the relevant emergency related details for later use and storage
def get_emer_det(payload, timestamp):
#     print("\n\nEnter get_emer_det")

    users = get_users()
    
#   Getting device data using the payload received from the triggered sensing device
    deviceData = get_device(payload['username'])
    sensor = deviceData[1]
    loc1=(float(deviceData[-1]),float(deviceData[-2]))

#   Getting the user of the triggered sensor
    if sensor == 'Flood Detector' or sensor == 'Wind Disaster Detector':
        user = users[3]
        area = deviceData[2]
        area = area.split("_")
        area = area[2]
        address = (area + "\n\nMessage from:\n" + user[1] + " " + user[2])
    
    else:
        for fd in users:
            if loc1 == (float(fd[-3]),float(fd[-4])):
                user = fd
                address = (user[6] + "\n" + user[7] + "\n" + user[8] + "\n" + user[9])
                break
    
#   Getting the address of the user
    
#     print("\n\nUser = ", user)
#     print("\n\naddress = ", address)
    
#   Storing all the relevant values in an array and returning the array
    emer_det = [user, sensor, loc1, address, timestamp]
#     print("\n\nExit get_emer_det")

    return emer_det

# Function to alert the fire department
def alert_fire(payload, timestamp):
#     print("\n\nEnter alert_fire")
#   Fetching all the data from FD database and storing in a variable
    retrieve = "SELECT * FROM FireDepartmentDB;"
    cursor.execute(retrieve)
    data = cursor.fetchall()
#     print("\n\n Fire Data = ", data)

#   Fetching the emergency details and storing relevant data in variables to represent the data
    emer_det = get_emer_det(payload, timestamp)
    
    sensor = emer_det[1]
    loc1 = emer_det[2]
    address = emer_det[3]
    
#   Finding the closest fire department
    fireDepartmentIndex = 0
    currentClosest = 10000000000
    i = 0
    
    for fd in data:
        loc2=(float(fd[-3]),float(fd[-4]))
        dist = hs.haversine(loc1,loc2)
        
        if (dist < currentClosest):
            currentClosest = dist
            fireDepartmentIndex = i
        
        i = i + 1
    
#   Storing the name and email of the closest fire department for use in other functions
    FD = data[fireDepartmentIndex][1]
    email = data[fireDepartmentIndex][2]
    print("\nFire Department to Contact = ", FD)
#     print("Fire Department Email = ", email)
#     print("Fire Department Distance = ", currentClosest, "km")

    
    
#   Sending the email to the fire department and returning the name of the nearest fire department
    email_emer_serv(email, sensor, address, loc1, timestamp, FD)
#     print("\n\nExit alert_fire")

    return FD

# Function to alert the police department
def alert_police(payload, timestamp):
#     print("\n\nEnter alert_police")

#   Fetching all the data from PD database and storing in a variable
    retrieve = "SELECT * FROM PoliceDepartmentDB;"
    cursor.execute(retrieve)
    data = cursor.fetchall()
#     print("\n\nPolice Data = ", data)
    
#   Fetching the emergency details and storing relevant data in variables to represent the data
    emer_det = get_emer_det(payload, timestamp)
    
    sensor = emer_det[1]
    loc1 = emer_det[2]
    address = emer_det[3]
    
#   Finding the closest police department
    policeDepartmentIndex = 0
    currentClosest = 10000000000
    i = 0
    
    for fd in data:
        loc2=(float(fd[-3]),float(fd[-4]))
        dist = hs.haversine(loc1,loc2)
#         print("\n\nPolice dist: "+ str(dist) + " index: " + str(i) )
        if (dist < currentClosest):
            currentClosest = dist
            policeDepartmentIndex = i
        
        i = i + 1
    
#   Storing the name and email of the closest police department for use in other functions
    PD = data[policeDepartmentIndex][1]
    email = data[policeDepartmentIndex][2]
    
    print("\nPolice Department to contact = ", PD)
#     print("Police Department Email = ", email)
#     print("Police Department Distance = ", currentClosest, "km")


    
#   Sending the email to the police department and returning the name of the nearest police department
    email_emer_serv(email, sensor, address, loc1, timestamp, PD)
#     print("\n\nExit alert_police")

    return PD

# Function to alert the EMS
def alert_EMS(payload, timestamp):
#     print("\n\nEnter alert_EMS")

#   Fetching all the data from EMS database and storing in a variable
    retrieve = "SELECT * FROM EmergencyMedicalServicesDB;"
    cursor.execute(retrieve)
    data = cursor.fetchall()
#     print("\n\nEMS Data = ", data)

#   Fetching the emergency details and storing relevant data in variables to represent the data
    emer_det = get_emer_det(payload, timestamp)
    
    sensor = emer_det[1]
    loc1 = emer_det[2]
    address = emer_det[3]
    
#   Finding the closest EMS
    emsIndex = 0
    currentClosest = 10000000000
    i = 0
    
    for fd in data:
        loc2=(float(fd[-3]),float(fd[-4]))
        dist = hs.haversine(loc1,loc2)
#         print("EMS dist: "+ str(dist) + " index: " + str(i) )
        if (dist < currentClosest):
            currentClosest = dist
            emsIndex = i
        
        i = i + 1
    
#   Storing the name and email of the closest EMS for use in other functions
    EMS = data[emsIndex][1]
    email = data[emsIndex][2]

    print("\nEMS to contact = ", EMS)
#     print("EMS Email = ", email)
#     print("EMS Distance = ", currentClosest, "km")
    
#   Sending the email to the EMS and returning the name of the nearest EMS
    email_emer_serv(email, sensor, address, loc1, timestamp, EMS)
#     print("\n\nExit alert_EMS")

    return EMS

# Function to alert the nearby users
def alert_users(payload, timestamp, emer_serv):
#     print("\n\nEnter alert_users")
    contactedUsers = []
#   Fetching all the users in the users database and storing them in a variable
    users = get_users()
#   Fetching the emergency details and storing relevant data in variables to represent the data
    emer_det = get_emer_det(payload, timestamp)

    sensor = emer_det[1]
    loc1 = emer_det[2]
    address = emer_det[3]
    user = ""
#     print("\n\nAll Users = ",users)
#     print("\n\nSensor = ", sensor)
    
#   Finding all the users within a specified radius of the emergency and notifying them
    for fd in users:
        loc2=(float(fd[-3]),float(fd[-4]))
        dist = hs.haversine(loc1,loc2)
        
        if (sensor != "Flood Detector" and sensor != "Wind Disaster Detector"):
            if (dist <= 0.6 and dist != 0):
                user_email = fd[4]
                contactedUsers.append(fd[3])
                print("\nUser to Notify = ", fd[3])
#                 print("User Email = ", user_email)
#                 print("User Distance = ", dist, "km")

                send_emails(fd[3], user_email, sensor, address, loc1, timestamp, emer_serv)
            
            elif dist == 0:
                Suser_email = fd[4]
                user = fd[3]
                contactedUsers.append(fd[3])
                distance = dist
#                 print("\nUser of Triggered Sensor = ", user)
#                 print("User of Triggere Sensor Email = ", Suser_email)
#                 print("User of Triggered Sensor Distance = ", dist, "km")
                send_email(user, Suser_email, sensor, address, loc1, timestamp, emer_serv, dist)
                
        elif (sensor == "Flood Detector" or sensor == "Wind Disaster Detector"):
            if (dist <= 3 and dist != 0):
                user_email = fd[4]
                contactedUsers.append(fd[3])
                print("\nUser to Notify = ", fd[3])
#                 print("User Email = ", user_email)
#                 print("User Distance = ", dist, "km")

                send_emails(fd[3], user_email, sensor, address, loc1, timestamp, emer_serv)
    if user != "":          
        print('\n------------------------------------------------------------------------------------------------------------------')
        print("User of Triggered Sensor = ", user)
#         print("User of Triggered Sensor Email = ", Suser_email)
#         print("User of Triggered Sensor Distance = ", distance, "km")
        print('------------------------------------------------------------------------------------------------------------------')
#     print('structure return')
    returnContactedUsers = ",".join(contactedUsers)
#     print(returnContactedUsers)
    return returnContactedUsers
#     print("\n\nExit alert_users")

def update_emerLog(payload, timestamp, esContacted , usersContacted):
    emer_det = get_emer_det(payload, timestamp)
    
    username = emer_det[0][3]
    sensor = emer_det[1]
    loc1 = emer_det[2]
    timestamp = str(timestamp)
    
    longitude = str(loc1[1])
    latitude = str(loc1[0])
   
#     print(username)
#     print(sensor)
#     print(timestamp)
#     print(longitude)
#     print(latitude)
#     print("check 1")
    createdAt = datetime.now()
    createdAt = createdAt.strftime("%Y-%m-%d %H:%M:%S")
    with connection.cursor() as cur:
# (username,sensor,longitude,latitude,esContacted,timestamp,createdAt)
            cur.execute("INSERT INTO `EmergencyLogDB`(`username`, `sensor`, `longitude`, `latitude`,`usersContacted` ,`esContacted`, `timeTriggered`, `createdAt`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (username,sensor,longitude,latitude,usersContacted,esContacted,timestamp,createdAt)) 
            connection.commit()
    
    print("Information added to EmergencyLogDB:")
    print('')
    print(username,sensor,longitude,latitude,usersContacted,esContacted,timestamp,createdAt)

# Creating a client instance using default parameters
# Assigns a callback to be called when a succesful connection has occurred
def on_connect(client, userdata, flags, rc):
    print("CONNACK recieved with code %d." % (rc))
    
# Defining the on_subscribe callback
# Only called once broker has responded to a subscription request
def on_subscribe(client, userdata,mid,granted_qos):
    print("Subscribed: " +str(mid)+" "+str(granted_qos))
  
# Defining the on_message callback
# msg variable is an MQTTMessage class
def on_message(client, userdata, msg):
    print('------------------------------------------------------------------------------------------------------------------')
    print('Start')
    print('------------------------------------------------------------------------------------------------------------------')
#   Printing msg data for coding purposes
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    print('')
#   Storing the msg payload in a variable and converting it from json to python format
    myData = json.loads(msg.payload)
    
#   Checking for a triggered sensor
    if(myData['alert']):
        
#       Getting the exact time a triggered sensor was registered
        timestamp = datetime.now()
        timestamp1 = timestamp
        timestamp = timestamp.strftime("%H:%M:%S on %d/%m/%Y")
        timestamp1 = timestamp1.strftime("%Y-%m-%d %H:%M:%S")

        print('An Emergency Alert has been detected at: ', timestamp)
        
#       Checking which type of emergency was triggered
        if(myData['type'] == "Fire Detector"):
            print('Fire Detector')
            fireDepartment = alert_fire(myData, timestamp)
            esContacted = fireDepartment
            usersContacted = alert_users(myData, timestamp, esContacted)
            
        if(myData['type'] == "Flood Detector"):
            print('Flood Detector')
            fireDepartment = alert_fire(myData, timestamp)
            policeDepartment = alert_police(myData, timestamp)
            EMS = alert_EMS(myData, timestamp)
            
            esContacted = (fireDepartment + ", " + policeDepartment + ", " + EMS)
            
            usersContacted = alert_users(myData, timestamp, fireDepartment)
            
        if(myData['type'] == "Wind Disaster Detector"):
            print('Wind Disaster Detector')
            fireDepartment = alert_fire(myData, timestamp)
            policeDepartment = alert_police(myData, timestamp)
            EMS = alert_EMS(myData, timestamp)
            
            esContacted = (fireDepartment + ", " + policeDepartment + ", " + EMS)
            
            usersContacted = alert_users(myData, timestamp, esContacted)
            
        if(myData['type'] == "Security Alarm"):
            print('Security Alarm')
            policeDepartment = alert_police(myData, timestamp)
            
            esContacted = policeDepartment

            usersContacted = alert_users(myData, timestamp, policeDepartment)
            
        if(myData['type'] == "Critical Emergency Button"):
            print('Critical Emergency Button')
            EMS = alert_EMS(myData, timestamp)
            
            esContacted = EMS

            usersContacted = alert_users(myData, timestamp, EMS)
    

        update_emerLog(myData, timestamp1, esContacted,usersContacted)
    print('\nend')
    print('------------------------------------------------------------------------------------------------------------------')


client = paho.Client()
# Connecting with username and password
client.username_pw_set("server","1234")
client.on_subscribe = on_subscribe
# On message callback is called for each message received
client.on_message = on_message
# Starting the MQTT connection
client.connect("localhost",1883)
client.subscribe([('alert',0)])
# Looping forever
client.loop_forever()
