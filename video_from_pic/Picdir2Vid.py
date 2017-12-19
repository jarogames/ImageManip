#!/usr/bin/python3
import glob
import os
import datetime
import cv2
import numpy as np

def ConvertDir2Avi( dirn ):
    jpgs=sorted( glob.glob(dirn+"/*.jpg" ) )
    print("i... converting ", dirn," ",len(jpgs),"images")
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
    print("WxH = ",wmax,"x",hmax)

    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter( dirn+".avi", fourcc, 10, 
                         (wmax,hmax) )
    j=0
    for i in jpgs:
        j=j+1
        print(" ...",i,j,"/",len(jpgs)," ", end="\r")
        image = cv2.imread(i)
        out.write(  image )

    out.release()
    print("\n")



    
print("i... ")
TODAY=datetime.datetime.now()
TODAY=TODAY.strftime("%Y%m%d")

PATH="~/.motion/*"
PATH=os.path.expanduser(PATH)

for i in glob.glob(PATH):
    if os.path.isdir(i) and len(i)>7:
        if os.path.isfile( i+".avi" ):
            print("!... AVI already exists",i)
            continue
        if i.find( TODAY )>=0:
            print("!... not this",i)
            continue
        ConvertDir2Avi( i )
        
