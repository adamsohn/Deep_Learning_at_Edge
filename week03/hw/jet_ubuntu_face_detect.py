import numpy as np
import cv2 as cv
import time 
import paho.mqtt.client as mqtt

#Face classifier (already trained)
face_cascade=cv.CascadeClassifier('haarcascade_frontalface_default.xml')

#Command for capturing photos from camera. 0 corresponds to the USB camera. This may be 1 depending upon your installation.
cap = cv.VideoCapture(0)

#Mosquitto config. Web broker found at https://github.com/mqtt/mqtt.github.io/wiki/public_brokers
#web_broker = test.mosquitto.org
web_broker = "5.196.95.208" #IP address for test.mosquitto.org
MQTT_TOPIC = "face_tpc"
MQTT_PORT = 1883

def on_connect_local(local_mqttclient, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc), ". Note: 0 is successful!")
    local_mqttclient.subscribe(MQTT_TOPIC)
    print("subscribed")
    return

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(web_broker, MQTT_PORT, 60)

time.sleep(4) #Giving connection time to setup before proceeding

# mqtt into a loop
local_mqttclient.loop_start()

#Below is image capture logic

def timestamp():
    #Print timestamp
    return time.strftime("%m_%d_%y_%H_%M_%S", time.gmtime())

def crop(x,y,w,h,face_uncrop):
    """
    Input face defined by rectangle & x,y,w,h coordinates. Output cropped face.
    Source: https://gist.github.com/tilfin/98bbba47fdc4ac10c4069cce5fabd834
    """
    r = max(w,h)/2
    centerx = x+w/2
    centery = y+h/2
    nx=int(centerx-r)
    ny=int(centery-r)
    nr=int(r*2)
    faceimg=face_uncrop[ny:ny+nr,nx:nx+nr]
    return faceimg

def loop_break():
    """
    No inputs. Checking for 'q' to be pressed. When 'q' pressed, loop exits.
    Source: https://stackoverflow.com/questions/13180941/how-to-kill-a-while-loop-with-a-keystroke
    """
    if cv.waitKey(1) & 0xFF == ord('q'):
        return "break" #Stopping OpenCV
    else:
        return "keep_going"

while(True): #looping
    time.sleep(2) #throttling by adding 2 second pause between captures.
    #Capture frame by frame
    ret,frame = cap.read()
    print("Captured Something", timestamp()) 
    #We don't use the color information, so might as well save space
    gray_img = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)  # convert the frame to grayscale
    print("Converted to grayscale", timestamp())
    #Detect face
    faces=face_cascade.detectMultiScale(gray_img,1.3,5)
    print("Classified", timestamp())
    for(x,y,w,h) in faces:
        print("Start face loop", timestamp())
        face_uncrop = cv.rectangle(gray_img,(x,y),(x+w,y+h),(255,0,0),2)  # set bounds of the face from the frame
        print("Set bounds", timestamp())
        face_crop = crop(x,y,w,h,face_uncrop) # cut out the face from the frame
        print("Cropped face", timestamp())
        ret,face_crop_png = cv.imencode('.png', face_crop) #encode as .png
        print("Encoded png", timestamp())
        msg = face_crop_png.tobytes()  # changing image to bytes
        print("Encode bytes", timestamp())
        local_mqttclient.publish(MQTT_TOPIC, payload = msg, qos=1, retain = False) #mqtt publishing
        print("Published", timestamp())
        if loop_break() == "break": #check if loop should break by user pressing 'q'
            break

#After loop is terminated, releasing resources
cap.release() #Releasing camera
cv.destroyAllWindows() #Closing any windows opened by cv
local_mqttclient.loop_stop() #Stopping mosquitto loop
local_mqttclient.disconnect() #Disconnecting mosquitto from host.
