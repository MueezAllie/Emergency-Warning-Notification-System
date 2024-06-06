import pymysql
import os

# Connecting to the PyMySQL database
connection = pymysql.connect(host="localhost", user="phpmyadmin", passwd="raspberry", database="phpmyadmin")
cursor = connection.cursor()

print("")
# Registering the Online Server using os commands
os.system(f"sudo mosquitto_passwd -c /etc/mosquitto/passwd server")

# Retrieving all the device data from the "devices" database
retrieve = "SELECT * FROM devices;"
cursor.execute(retrieve)
data = cursor.fetchall()
print("Devices = ", data[0])

count = 1

# Using a for loop to register all the devices according to their given "username" using os commands
for i in data:
    print(count)
    username = i[2]
    user = i[3]
    print(str(username)+" "+str(user))
    os.system(f"sudo mosquitto_passwd -b /etc/mosquitto/passwd {username} raspberry")
    print("DONE")
    
    count+=1