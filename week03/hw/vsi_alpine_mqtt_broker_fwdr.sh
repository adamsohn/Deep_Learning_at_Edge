#!/bin/bash
xhost + local:root
docker run --user=root --volume="/mnt/photobucket_hw03:/tmp/HW03/img_bucket" --name vsi_broker --volume "$PWD:/tmp/HW03" -p 1883:1883 -ti i_ubuntu_mqtt bash 
