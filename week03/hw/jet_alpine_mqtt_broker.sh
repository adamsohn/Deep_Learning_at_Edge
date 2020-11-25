#!/bin/bash

#Execute on root priv
xhost + local:root

#Spinning up Container
docker run --user=root --name jet_broker --network face_brg -p :1883 -v "$PWD":/HW03 -d i_alpine_mqtt sh -c "mosquitto -c /HW03/jet_alpine_mqtt_broker.conf"
