#!/bin/bash
#DIRNAME=/tmp/tmp_mpv_$PPID
#echo ... ENCODE .. my parent PID would be ${DIRNAME} ... look
pwd
echo LOCAL:
ls
#echo and ${DIRNAME}
#ls ${DIRNAME}
sleep 1
#pushd $(dirname "${BASH_SOURCE[0]}")
######### NO DELETE ####
#rm -f *.log *.webm

start=$(<val-start)
end=$(<val-end)
length=$(python -c 'print("{:.1f}".format('$end-$start'))')


filename=$(<val-filename)
humanstart=$(<val-humanstart)
outname=$(basename "$filename")
outname="${outname%.*}_[$humanstart]_$length"
#ln -s "$outname".webm clip.webm
#ffmpeg -i clip.mkv -crf 10 -b:v 0 -c:v vp8 -speed 0 -an -pass 1 -f webm -y /dev/null
#ffmpeg -i clip.mkv -crf 10 -b:v 0 -c:v vp8 -speed 0 -an -pass 2 -metadata title="$outname" clip.webm

############
#
# faster compression
#
###########
ffmpeg  -loglevel panic -i clip.mkv -c:v libx264 -crf 23 -preset medium -c:a mp3 -b:a 128k -movflags +faststart -vf scale=-2:720,format=yuv420p  -threads 4 clip.mp4  

########################### clip.mkv is always deleted
#                           clipxxx.webm  NOT
#LN=`ls clip*.webm | grep -E '[0-9][0-9][0-9]\.webm' | cut -b 5-7 | sort | tail -1`
#if [ "$LN" = "" ]; then
#    LN=0
#fi
#CLIP=clip`seq -f %03g  $(( $LN + 1 )) 1 $(( $LN + 1 ))`.webm
#echo next name = $CLIP
##########################

echo ... moving clip.mp4 to  "$outname".mp4
mv clip.mp4 "$outname".mp4
ls -lh "$outname".mp4
ls -d -1 $PWD/"$outname".mp4

tmpdir=$PWD

origdir=$(<original-dir)
mv  "$outname".mp4 $origdir/
rm *.mkv
cd $origdir

if [ "${tmpdir:0:4}" = "/tmp" ]; then
    rm -rf $tmpdir
fi

#popd

