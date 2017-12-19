#!/usr/bin/python3
######################################
# OPTIMIZE JPG AND PNG PICTURES
# in a subdir /**/
#######################################

import argparse
import os
import glob
import subprocess
parser=argparse.ArgumentParser(description="""
 ... 
""")

parser.add_argument('-d','--diveinto', default="", help='', required=True)
args=parser.parse_args()


jpg= glob.glob(os.path.expanduser(args.diveinto)+"/**/*.[Jj][Pp][Gg]", recursive=True)
png= glob.glob(os.path.expanduser(args.diveinto)+"/**/*.[Pp][Nn][Gg]", recursive=True)
pics=jpg+png
print( "i... found {} pics total".format(len(pics)) )#print( "\n".join(pics) )

for i in jpg:
    CMD='jpegoptim -m85 "'+i+'"'
    print("X... ",CMD)
    p=subprocess.check_call( CMD , shell=True)
for i in png:
    # -o 7 max, but 6 is time shorter. strip metadata??
    CMD='optipng -o 6 -strip all  "'+i+'"'
    print("X... ",CMD)
    p=subprocess.check_call( CMD , shell=True)
