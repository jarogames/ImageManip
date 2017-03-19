#!/bin/bash
#################
#
# this is run directly after F3 is pressed
#
################
#pushd $(dirname "${BASH_SOURCE[0]}")
#
DIRNAME=/tmp/tmp_mpv_$PPID
#### I go into tmp where Makefile copy should be
pushd ${DIRNAME}
echo ... clipping - using the content of $DIRNAME :
ls $DIRNAME
make clip.mkv
sleep 1
echo ............ DO NOT QUIT THIS CLIP ...... press F4 ..........
if [ -f clip.mkv ]; then
    mpv -loop inf clip.mkv
else
    zenity --error --text 'Cutting failed'
fi
popd

