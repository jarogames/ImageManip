#!/bin/bash
########### PPID IS a problem, we are child of Makefile ......
#DIRNAME=/tmp/tmp_mpv_$PPID
#echo ... encode2 :  I am still at ${DIRNAME}
#pwd
#sleep 5
#pushd $(dirname "${BASH_SOURCE[0]}")
make clip.webm
# I dont know what to play. Maybe linl clip.webm to $output.mp4....
#if [ -f clip.webm ]; then
#    mpv -loop inf clip.webm
#else
#    zenity --error --text 'Encoding failed'
#fi
#popd

