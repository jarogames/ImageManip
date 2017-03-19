#!/bin/bash
#pushd $(dirname "${BASH_SOURCE[0]}")
rm -f *.mkv *.ass
echo ... CLIP.SH ... I am already in tmp:
pwd
sleep 1
start=$(<val-start)
end=$(<val-end)
filename=$(<val-filename)
length=$(python -c 'print('$end-$start')')
rm -rf ~/.fonts/tmp
mkdir -p ~/.fonts/tmp
pushd ~/.fonts/tmp
ffmpeg -loglevel panic  -dump_attachment:t "" -i "$filename"
popd
ffmpeg -loglevel panic -i "$filename" subs.ass
ffmpeg -loglevel panic -ss $start -i "$filename" -t $length -vf colormatrix=bt709:bt601 -c:v ffvhuff -c:a flac -sn clip0.mkv
if [ "$?" = "0" ]; then
    echo ... ffmpeg ok
else
    echo ... clip0.mkv ............. NOT CREATED
    exit
fi
if [ $(cat subs.ass | wc -c) -eq "0" ]; then
    mv clip0.mkv clip.mkv
else
    ffmpeg -loglevel panic -itsoffset $start -i clip0.mkv -vf ass=subs.ass,setpts=PTS-$start -c:v ffvhuff -an video.mkv
    ffmpeg -loglevel panic -i video.mkv -i clip0.mkv -c copy clip.mkv
fi
if [ -e  ~/.fonts/tmp ] ; then
    rm -r ~/.fonts/tmp
fi
#popd

