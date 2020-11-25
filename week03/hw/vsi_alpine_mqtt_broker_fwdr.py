import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as mqtt
import sys
    
#Mosquitto config. Web broker found at https://github.com/mqtt/mqtt.github.io/wiki/public_brokers
#web_broker = test.mosquitto.org
web_broker = "5.196.95.208" #IP address for test.mosquitto.org
MQTT_TOPIC = "face_tpc" 
MQTT_PORT = 1883
output_dir = "/tmp/HW03/img_bucket"

def on_connect_local(local_mqttclient, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        local_mqttclient.subscribe(MQTT_TOPIC)

#Generating unique string identifier
def get_date():
    return time.strftime("%m_%d_%y_%H_%M_%S", time.gmtime())

def on_message(local_mqttclient, userdata, msg):
    # Aknowledge reception of image
    print("Image captured!")
    
    # De-encode message
    f = np.frombuffer(msg.payload, dtype='uint8')
    img = cv.imdecode(f, flags=1)
    print(img.shape)
    
    # Save messages
    img_name = output_dir + "/img_" + get_date() + ".png"
    print(img_name)
    
    # Write image in Object Storage
    cv.imwrite(img_name, img)
    
# Connect to MQTT client
local_mqttclient = mqtt.Client()
local_mqttclient.connect(web_broker, MQTT_PORT, 60)
local_mqttclient.on_connect = on_connect_local
time.sleep(4) #Giving connection time to setup before proceeding
local_mqttclient.on_message = on_message

# MQTT into loop
local_mqttclient.loop_forever()
