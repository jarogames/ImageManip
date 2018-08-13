#!/usr/bin/python3
##########################################
#
# https://www.linux.com/learn/how-sort-and-remove-duplicate-photos-linux
# du -sh Pictures/
# find . -type f | wc -l 
# find . -type f -exec md5sum '{}' ';' | sort | uniq --all-repeated=separate -w 15 > dupes.txt
#
#import exifread # problem to pip3  thread/threading
#import piexif # same
#from IPTC import IPTCInfo # same

import argparse
import PIL.ExifTags
import PIL.Image
import os
import pprint

import subprocess as sp

priwi=57

def CALL_BASH( CMD ):
    print( "i... {CMD:{priwi}s}  ".format(priwi=priwi,CMD=CMD) ,  end="" )
    res=""
    try:
        res=sp.check_output( CMD.split() ).decode("utf8")
        print(" ... [ok]")
    except:
        print(" ... [ERROR]")
    return res

        
#####################################
#  ARGUMENTS
#####################################
parser=argparse.ArgumentParser(description="",usage="""
-p ~/04_MEDIA/PICTURES
""", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-p','--path_name', default=".", help='path of the picture repository')
#parser.add_argument('-p','--path_name', required=True, help='path of the picture repository')

parser.add_argument('-f','--file_name', default=".", help='If none, we search all jpg JPG')
parser.add_argument('--debug', action="store_true", help='')#,required=True
args=parser.parse_args()

args.file_name=os.path.expanduser( args.file_name )


if args.file_name==".":
    import glob
    jpgfiles1=glob.glob("*.jpg")
    jpgfiles2=glob.glob("*.JPG")
    jpgfiles=[]
    if not jpgfiles1 is None:jpgfiles=jpgfiles+ jpgfiles1 
    if not jpgfiles2 is None:jpgfiles=jpgfiles+ jpgfiles2 
    print( jpgfiles )
else:
    jpgfiles=[  args.file_name ]

maxfiles=len(jpgfiles)


#=============== LOOP =================================#
count=0
for file_name in jpgfiles:
    count+=1
    pic_desc={}
    ################################
    # Image open
    ################################
    img = PIL.Image.open( file_name )
    exif_data = img._getexif()
    exif_info = img.info['exif']  # FOR SAVE
    #print( exif_info )
    ######print( exif_data )
    ######print("------")
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
    }



    
    exif['MakerNote']="" # Kill a mess
    #
    #pprint.pprint( exif )  # =========================++>>>>
    #




    # ------ based on earlier experience----- DATE
    if "DateTime" in exif.keys():
        DATE=exif["DateTime"]
    elif "DateTimeOriginal" in exif.keys():
        DATE=exif["DateTimeOriginal"]
    elif "DateTime(original)" in exif.keys():
        DATE=exif["DateTime(original)"]

    pic_desc['date']=DATE
    pic_desc['year']=DATE.split(":")[0]
    pic_desc['month']=DATE.split(":")[1]



    #--------------------------------------- SIZE
    width, height = img.size
    ew,eh=0,0
    RATIO=width/height

    print("----------------------------------------------------------------   {}/{}".format(count,maxfiles))
    print( "     {CMD:{priwi}s}   {width}x{height} ".format(priwi=priwi,
                                                            CMD=file_name,
                                                            width=width,height=height)  )

    
    if "ExifImageHeight" in exif.keys(): eh=exif["ExifImageHeight"]
    if "ExifImageWidth"  in exif.keys(): ew=exif["ExifImageWidth"]

    pic_desc['w']=width
    pic_desc['h']=height
    pic_desc['r']=RATIO
    ####print( "i... {CMD:{priwi}s}  ".format(priwi=priwi,CMD="resizing ?") ,  end="" )
    if (ew>0) and (eh>0) and ((ew!=width) or (eh!=height)):
        print( "i... {CMD:{priwi}s}  ".format(priwi=priwi,CMD="       ") ,  end="" )
        print(" ... [was RESIZED earlier]")
        pic_desc['resized']="was RESIZED"
    else:
        pic_desc['resized']="was not resized"
        #print(" ... [not resized]")

    
    
    ##### THIS IS TAKEN FROM  foto_sort ################
    #CMD='identify -format "%[IPTC:2:25]"  {}'.format( file_name )
    CMD='identify -format %[IPTC:2:25]  {}'.format( file_name )
    res=""
    pic_desc['tags']=CALL_BASH( CMD )
    #pprint.pprint( pic_desc )


    pic_desc['pano']=""
    if pic_desc['r']>3:
        pic_desc['pano']="_pano"


    ############################## NEW DIRECTORY ###################    
    #        y  m  t pano
    YEARDIR="{}_{}".format( pic_desc['tags'] ,  pic_desc['year'] )
    NEWDIR="{}_{}_{}{}".format( pic_desc['year'],pic_desc['month'],pic_desc['tags'],pic_desc['pano'] )
    NEWDIR="{}/{}/{}".format( args.path_name, YEARDIR, NEWDIR )

    #print( "i... {}".format(NEWDIR ) , end="")
    print( "i... {CMD:{priwi}s}  ".format(priwi=priwi,CMD=NEWDIR) ,  end="" )
    if not os.path.exists( NEWDIR ):
        print(" ... [CREATING]")
        os.makedirs( NEWDIR )
    else:
        print(" ... [exists]")


        
    OUTNAME=NEWDIR+"/"+file_name
    ############################### RESIZE #######################
    if pic_desc['w']>2500:
        print( "i... {CMD:{priwi}s}  ".format(priwi=priwi,CMD="resizing") ,  end="" )
        basewidth = 2272
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        print(" ... [resized]")
        #####img.save( "test.jpg",optimize=True,quality=95  ) 
        ######exif = im.info['exif']
        #####im.save('P4072956_thumb.jpg', exif=exif)  )
        img.save( OUTNAME, optimize=True,quality=95, exif=exif_info )  # 50kB+ of crap
    else:
        CMD="cp "+file_name+" "+OUTNAME
        CALL_BASH( CMD )

        
    #CMD="jpegoptim -p -m50 {}".format( file_name  )
    CMD="jpegoptim -p -m50 {}".format( OUTNAME  )
    CALL_BASH( CMD )
####===================================== END OF LOOP ======================


