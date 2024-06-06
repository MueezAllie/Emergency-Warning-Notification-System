import paho.mqtt.client as paho
import time
import random
import json

def is_alert():
    
    n = random.random()
    print(n)
    if (n<0.05):
        return True
    else:
        return False

def on_connect(client, userdata, flags, rc):
    print("CONNACK recieved with code %d." % (rc))
    

def on_publish(client, userdata, mid):
    print("mid: " + str(mid))
    

payload = {'username' : 'DMCT_FD_Lansdowne',
           'type' : 'Flood Detector'}


client = paho.Client()
client.username_pw_set("DMCT_FD_Lansdowne","raspberry")
client.on_publish = on_publish
client.connect("localhost",1883)
client.loop_start()

while True:
    alert = is_alert()
    payload["alert"] = alert
    print(payload)
    (rc,mid) = client.publish("alert", json.dumps(payload), qos=0)
    #print(alert)
    time.sleep(3)
