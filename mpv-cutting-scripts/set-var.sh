#!/bin/bash
# the original idea was to run from $HOME and put all files there
#         however
# if a path is general - like /opt/ - we must create /tmp
#echo ... SETVAR...my PID = $$ parent has $PPID ... the latter is mpv

ARG2="$2"
DIRNAME=/tmp/tmp_mpv_$PPID
mkdir -p $DIRNAME
#echo "$2" > $(dirname "${BASH_SOURCE[0]}")/val-"$1"


# i need absolute path ================================
MDIR=""
if [ "$1" = "filename" ]; then
    echo ... Movie FILENAME EXTRACTION ...
    # .         easy
    # subdir/
    # /full/path
    MDIR=$(dirname $ARG2)
    echo ...directory is ${MDIR}
    if [ "$MDIR" = "." ]; then
	MDIR=${PWD}
	echo . ...replaced by ${MDIR}
    elif [ "${MDIR:0:1}" = "/" ]; then
	echo ...absolute ${MDIR}
    else
	echo ...relative path - i dont know ${MDIR}
    fi
    
    echo "${MDIR}/${ARG2}" > ${DIRNAME}/val-"$1"
else
    echo "${ARG2}" > ${DIRNAME}/val-"$1"
fi

# always copy Makefile...even 2 x ... from /opt
cp $(dirname "${BASH_SOURCE[0]}")/Makefile  ${DIRNAME}
echo $PWD > ${DIRNAME}/original-dir
#
echo ... content of $DIRNAME :
ls  $DIRNAME
