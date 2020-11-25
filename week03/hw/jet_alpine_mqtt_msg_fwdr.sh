#!/bin/bash

#Execute on root priv
xhost + local:root

#Spinning up Container
docker run --user=root --name jet_fwd --network face_brg -v "$PWD":/HW03 -d i_alpine_mqtt sh -c "mosquitto -c /HW03/jet_alpine_mqtt_msg_fwdr.conf"
