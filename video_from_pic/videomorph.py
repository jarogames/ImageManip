#!/usr/bin/python3
from shlex import quote
import shutil
import subprocess as s
import glob
import os
import time

#
#  ls temp_fin/*.jpg -1 | xargs -n 1 -I III  convert III -gravity center -background black  -extent 800x800  temp_fin8/III
#
#ls temp_fin/*.jpg -1 | xargs -n 1 -I III  convert III -gravity center -background black  -extent 800x800  XIII
#
#
#

SIX="%06d"

def prepare_morph(a,b, delay ):
    cmd='convert  "{}" "{}"  -delay {} -morph {} temp_one/%06d.jpg'.format( a,b , delay , delay )
    print( "# CMD : ",cmd )
    r=s.Popen( cmd, shell=True,  stdout=s.PIPE, stdin=s.PIPE)
    r.communicate()


def copyall():
    #sorted(glob.glob('*.png'), key=os.path.getmtime)
    #sorted(glob.glob('*.png'), key=os.path.getsize)
    src=sorted( glob.glob("temp_one/*.jpg") )
    #print('src=',src)
    dst=sorted( glob.glob("temp_fin/*.jpg") )
    #print('dst=',dst)
    if len(dst)==0:
        print("i... INITIAL COPY TO temp_fin")
        for i in src: shutil.copy(i , "temp_fin/"+os.path.basename(i))
    else:
        base=os.path.basename(dst[-1]) # 000001.jpg
        bas=os.path.splitext(base)[0]  # 000001 
        six=len(bas) # number of letters in 000001
        j=1
        print("i... last dst in temp_fin/ :{}   #letters=={}".format(base,six) )
        for i in src:
            tgt="{num:0{width}d}".format( num=int(bas)+j, width=six )
            j=j+1
            print( "i...     src=",i,"target==",tgt )
            shutil.copy(i , "temp_fin/"+tgt+'.jpg')


def run_shell_cmd( RMCMD ):  # rm temp/*
    p=s.Popen( RMCMD, shell=True,  stdout=s.PIPE, stdin=s.PIPE)
    rrr,err=p.communicate()
    rrr=  rrr.decode('utf8').rstrip() .split("\n")
    print(rrr)
    return rrr








###################################################
#
#  MAIN
#
##
##################################################
import argparse
parser = argparse.ArgumentParser(description='This is a videomorph.py program based on imagemagick')


parser.add_argument('-s','--staticframes',    default=20)
parser.add_argument('-t', '--transframes',action="store", default=10 )
parser.add_argument('-g', '--geometry',action="store", default="800x600" )


args=parser.parse_args()
delaySTAT=args.staticframes
delayTRAN=args.transframes


RMCMD="rm temp_fin Xtemp_fin temp_one -r"
print(RMCMD)
time.sleep(4)
try:
    res=s.check_call( RMCMD.split() )
except:
    print("X... DIDnt work")

cmd='ls -1 *.jpg *.JPG *.jpeg *.JPEG *.png *.PNG'
#cmd='ls -1 *.jpg '
rrr=run_shell_cmd( cmd )
#res=s.Popen( cmd , shell=True, stdout=s.PIPE, stdin=s.PIPE)
#rrr,err=res.communicate()
#rrr=  rrr.decode('utf8').rstrip() .split("\n")
#------------------------------
#print(rrr)

print( "# NUM  of files =",len(rrr) )
try:
    os.mkdir("temp_one")
except:
    print()
try:    
    os.mkdir("temp_fin")
except:
    print()
try:    
    os.mkdir("Xtemp_fin")
except:
    print()


    
    
RMCMD="rm  temp_one/*.jpg"
for i in range(len(rrr)-1):
    print("{:4d}-----------------".format(i) )
    run_shell_cmd( RMCMD ) # clean 
    prepare_morph( rrr[i],rrr[i] ,   delaySTAT )
    copyall()
    run_shell_cmd( RMCMD ) # clean 
    prepare_morph( rrr[i],rrr[i+1] , delayTRAN )
    copyall()
prepare_morph( rrr[i+1],rrr[i+1] , delaySTAT )
copyall()

#####
#
#   maybe RESIZE would be faster to do earlier....
#
####
#===========  resize to the same  geometry    
CMDresize="time mogrify -resize "+args.geometry+"  temp_fin/*.jpg"
print("O...   RESIZE\n",CMDresize)
run_shell_cmd( CMDresize )
#=========== this places the pic on  black canvas    
CMDconv="ls temp_fin/*.jpg -1 | xargs -n 1 -I III  convert III -gravity center -background black  -extent   "+args.geometry+"  XIII"
print("O...  PLACE ON CANVAS\n",CMDconv)
run_shell_cmd( CMDconv )

#================
CMDvid="time ffmpeg -r 5   -i Xtemp_fin/%06d.jpg output`date +%Y%m%d_%H%M%S`.mp4"
print("O...   VIDEO\n",CMDvid)
run_shell_cmd( CMDvid )
