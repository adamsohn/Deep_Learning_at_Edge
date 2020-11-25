#!/bin/bash
xhost + local:root
docker run \
--user=root \
--env="DISPLAY" \
--name jet_detect --privileged --network face_brg -v "$PWD":/HW03 -ti i_jet_ubuntu_face_detect bash
