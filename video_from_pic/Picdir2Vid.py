#!/usr/bin/python3
import glob
import os
import datetime
import cv2
import numpy as np
import argparse


#####################################
#  ARGUMENTS
#####################################
parser=argparse.ArgumentParser(description="")
parser.add_argument('-d','--diveinto', required=True, help='')
parser.add_argument('--debug', action="store_true", help='')#,required=True
args=parser.parse_args()


def ConvertDir2Avi( dirn ):
    jpgs=sorted( glob.glob(dirn+"/*.jpg" ) )
    if len(jpgs)<3:
        print("+... not enough jpgs")
        return
    print("i... checking    ", dirn," ",len(jpgs),"images")
    j=0
    hmax,wmax=0,0
    for i in jpgs:
        j=j+1
        if j%5!=0:continue
        print(wmax,hmax," ...",i,j,"/",len(jpgs)," ", end="\r")
        image = cv2.imread(i)
        height = np.size(image, 0)
        width =  np.size(image, 1)
        if wmax<width:wmax=width
        if hmax<height:hmax=height
    print("\nWxH = ",wmax,"x",hmax)


    dirnavi=dirn+".avi"
    print("i... converting to  ", dirnavi," ",len(jpgs),"images")
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter( dirnavi, fourcc, 10, 
                         (wmax,hmax) )
    
    j=0
    for i in jpgs:
        j=j+1
        print(" ...",i,j,"/",len(jpgs)," ", end="\r")
        image = cv2.imread(i)
        out.write(  image )

    out.release()
    print("\n")



    
TODAY=datetime.datetime.now()
TODAY=TODAY.strftime("%Y%m%d")

PATH="~/.motion/*"
PATH=args.diveinto
PATH=os.path.expanduser(PATH)
if PATH[-1]!="/": PATH=PATH+"/"

print("i... ready to convert @",PATH,"  now=",TODAY)

for i in glob.glob(PATH+"*"):
    if os.path.isdir(i):
        if os.path.isfile( i+".avi" ):
            print("|... AVI already exists",i)
            continue
        if i.find( TODAY )>=0:
            print("|--- not this",i)
            continue
        ConvertDir2Avi( i )
