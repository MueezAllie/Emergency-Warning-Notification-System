import paho.mqtt.client as paho
import time
import random
import json
# Function to simulate device states using a random number generator
def is_alert():
    
    n = random.random()
    print(n)
    if (n<0.1):
        return True
    else:
        return False
    
# Creating a Client instance using default parameters given
def on_connect(client, userdata, flags, rc):
    print("CONNACK recieved with code %d." % (rc))
# Creating a publish callback
def on_publish(client, userdata, mid):
    print("mid: " + str(mid))
    
# Creating a payload for the sensor according to device details
payload = {'username' : 'Boet_CEB_SurreyEstate',
           'type' : 'Critical Emergency Button'}

# Starting the device connection
client = paho.Client()
client.username_pw_set("Boet_CEB_SurreyEstate","raspberry")
client.on_publish = on_publish
client.connect("localhost",1883)
client.loop_start()

# Sitting in a loop to read from an imaginary sensor every 3 seconds
while True:
    alert = is_alert()
    payload["alert"] = alert
    print(payload)
    (rc,mid) = client.publish("alert", json.dumps(payload), qos=0)
    time.sleep(3)