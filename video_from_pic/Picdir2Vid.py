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
parser=argparse.ArgumentParser(description="",usage="", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-d','--diveinto', required=True, help='')
parser.add_argument('-o','--overwrite_today',action="store_true" , help='')
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
        #print(i)
        try:
            image = cv2.imread(i)
        except:
            print("CORRUPT")
        height = np.size(image, 0)
        width =  np.size(image, 1)
        if wmax<width:wmax=width
        if hmax<height:hmax=height
    print("\nWxH = ",wmax,"x",hmax)
    img_black=np.zeros( (hmax,wmax,3),dtype=np.uint8)
    

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
        height = np.size(image, 0)
        width =  np.size(image, 1)
        ###print("PIC ",i,width,"x",height," ")
        if height<hmax or width<wmax:
            #print("error",width,height)
            img_black[0:0+image.shape[0], 0:0+image.shape[1]] = image
            out.write(  img_black )
        else:
            #print("D... writing c",image.shape[0], image.shape[1]," ")
            try:
                out.write(  image )
            except:
                print("!... error when writing frame",image.shape[0], image.shape[1]," ")

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
    #print( i )
    if os.path.isdir(i):
        if os.path.isfile( i+".avi" ):
            print("|... AVI already exists",i)
            continue
        if i.find( TODAY )>=0 and not args.overwrite_today:
            print("|--- not this {}, it is today, try -o".format(i))
            continue
        ConvertDir2Avi( i )
