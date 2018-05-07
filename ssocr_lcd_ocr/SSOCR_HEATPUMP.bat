#!/bin/bash


for ((i=0;i<99999999;i++)); do

    
wget "http://localhost:8080/?action=snapshot" -O temp.jpg

#till 20180418
#T=`./ssocr-2.16.3/ssocr -r 1 -v    -D r_threshold  -t 29 -a  -d -1   crop 250 60 320 240 make_mono invert  erosion dilation temp.jpg`
# genius facepalm 2020 camera
T=`./ssocr-2.16.3/ssocr -r 1 -v  -D    -d -1   crop 280 120 120 100    make_mono  -t 63  make_mono invert erosion dilation  temp.jpg`


echo run ${i}. t= $T
mymongo.py -w test -c heatpumpdisp -v temp=$T

sleep 60

done



