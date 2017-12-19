#!/usr/bin/python3

import argparse

import re

import difflib  # compare two strings

import subprocess
import time
import sys       # flush
import tempfile

import datetime

import os
import glob
#  check file existence
from pathlib import Path



def countdown(ti , ssi):
    global temp_name
    global args
    DEST='ztrans_'+temp_name+'_'+ssi
    print('i... saving {}.mp3    ( restart from={} line={} )'.format(DEST,argscontinu,int(ssi))  , end="\r")
    for i in range( int(ti) ):
        print('{:02d} '.format( ti-i ), end='\r')
        #sys.stdout.flush()
        time.sleep( 1 )
    #print('-'*ti, end='\r')
    #for i in range( int(ti) ):
    #    print('#', end='')
    #    sys.stdout.flush()
    #    time.sleep( 1 )
    #print("                    ",end="\r")



def run_cmd_with_wait( CMD ):
    ### HERE I have seen an error: I ADD TRY:
    # this waits finishing the call
    try:
        res=subprocess.check_call(CMD+' >/dev/null 2>&1', shell=True)
    except subprocess.CalledProcessError as e:
        print('!... command ERROR', e.output  )
        print('!...        ', CMD  )
        print('i... TRY ONCE MORE after 50 sec.')
        time.sleep( 50 )
        try:
            res=subprocess.check_call(CMD, shell=True)
        except subprocess.CalledProcessError as e:
            print( '!...trans command ERROR', e.output  )
            if argscontinu>0:
                print('i... INSTEAD OF QUIT - I RESTART')
                os.execv(__file__, sys.argv)
            quit()
            return 1
    
def say_trans( phrase, ssi ):
    global temp_name
    global args
    MEASURE=datetime.datetime.now()
    #trans -b -p -no-auto cs:cs "$PHRASE" -player "mpv --speed 0.9 --volume 100 -ao pcm:file=\"$DESTINATION/$PHRASE.wav\""
    #lame --scale 3 "$DESTINATION/$PHRASE.wav"
    #rm   "$DESTINATION/$PHRASE.wav"
    ###################################################
    DEST='ztrans_'+temp_name+'_'+ssi
    ###################################################
    ###print('i... saving',DEST+'.mp3         (',argscontinu, int(ssi),')' , end="\r")
    #print('i... saving {}.mp3    ( restart from={} line={} )'.format(DEST,argscontinu,int(ssi))  , end="\r")
    if argscontinu<=int(ssi):
        #########################    trans
        CMD='trans -b -p -no-auto cs:cs "'+phrase+'" -player "mpv --speed 1.3 --volume 100 -ao pcm:file='+DEST+'.wav"'
        CMDEN='trans -b -p -no-auto en:en "'+phrase+'" -player "mpv --speed 1.3 --volume 100 -ao pcm:file='+DEST+'.wav"'
        if args.english:
            CMD=CMDEN

        run_cmd_with_wait( CMD )
        my_file = Path(DEST+".wav")
        if not my_file.is_file():
            print('!... problem with wav file', DEST+".wav" )
            time.sleep(20)
            run_cmd_with_wait( CMD )
            if not my_file.is_file():
                print('!... 2nd problem with wav file', DEST+".wav" )
                quit()
        # ### HERE I have seen an error: I ADD TRY:
        # # this waits finishing the call
        # try:
        #     res=subprocess.check_call(CMD, shell=True)
        # except subprocess.CalledProcessError as e:
        #     print( '!...trans command ERROR', e.output  )
        #     print('i... TRY ONCE MORE after 30 sec.')
        #     time.sleep(30)
        #     try:
        #         res=subprocess.check_call(CMD, shell=True)
        #     except subprocess.CalledProcessError as e:
        #         print( '!...trans command ERROR', e.output  )
        #         quit()
        #         return 1
        ########################## LAME
        #CMD='lame --scale 2 '+DEST+'.wav  2>/dev/null'
        CMD='lame --scale 2 '+DEST+'.wav  '
        run_cmd_with_wait( CMD )
        ####res=subprocess.check_call(CMD, shell=True)
        #res=subprocess.check_call(CMD, shell=True)
        #if res!=0:
        #    print('!...LAME ERROR')
        #    quit()
        #    return 1
        #
        ########################## rm WAV
        DEST=re.sub('\s','',DEST)
        CMD='rm '+DEST+'.wav'
        #if DEST.find('/tmp')!=0:
        #    print('!... security error')
        #    quit()
        res=subprocess.check_call(CMD, shell=True)
        if res!=0:
            print("!... RM ERROR")
            quit()
            return 1

        remains=args.time - (datetime.datetime.now() - MEASURE).seconds
        if remains<0: remains=0
        #print('countdown:')
        countdown( remains ,ssi )
    
    return 0





def findlastnum( tmpl ):
    '''
    tmpl ... template like ztrans_nsdvtkqr_00000.mp3
    the function gives the last number existing
    to be able to continue with the same  hash
    '''
    print('i... analyzing the template filename: /'+tmpl+'/')
    dirn=os.path.dirname( tmpl ) 
    #if len(dirn)==0:
    #    tmpl='/tmp/'+tmpl
    #print( os.path.dirname( tmpl ) )
    #print( os.path.basename( tmpl ) )
    dirfil=os.path.splitext( tmpl )[0]
    bases='_'.join( dirfil.split('_')[0:-1] ) +"_"
    ##if len(bases)<2:
    ##    print("!... /"+dirfil+"/ doesnot look as ztrans_000000.mp3 ... quiting")
    ##    quit()
    print(bases)
    #import glob
    all=glob.glob( bases+'*mp3')
    if len(all)<1:
        print("!... no mp3 files like",bases)
        return 0,os.path.splitext( tmpl )[0].split('_')[-2]
    #print( sorted(all)[-1] )
    las=sorted(all)[-1] 
    lanum=os.path.splitext( las )[0].split('_')[-1]
    hash1=os.path.splitext( las )[0].split('_')[-2]
    print('i...   LSTNUMBER=',lanum)
    return int(lanum),hash1







############################################
#
#  M A I N
#
###########################################
############################################
#
#  M A I N
#
###########################################
############################################
#
#  M A I N
#
###########################################



parser=argparse.ArgumentParser(description="""
 ... 
""")

parser.add_argument('book',  default=""  )

#parser.add_argument('-c','--continu',  default='last',  help='-c ztrans_nsdvtkqr_00000.mp3  OR -c ')
parser.add_argument('-c','--continu',  default='',  help='-c ztrans_nsdvtkqr_00000.mp3  OR -c ', nargs="?")
# -- FROM NOW:   -c  ztrans_nsdvtkqr_00000.mp3 - finds automatic
parser.add_argument('-t','--time',  default=9, type=int, help='seconds between questions')
parser.add_argument('-p','--path_to_save',  default="./", help='')
parser.add_argument('-d','--dryrun', action="store_true", help='')
parser.add_argument('-e','--english', action="store_true", help='use english to english read')

args=parser.parse_args()


###### --- continuation from filename     tmp HASH #########
#   -c ztrans_00000.mp3
#   -c : this will read .read_book.last
argscontinu=0  # this is a number
exitme=0
if args.continu is None:
    print("i... No arguments added to -c: using .read_book.last")
    try:
        with open(".read_book.last", "r" ) as f:
            book1=f.readline()
            print('i... my book and the last book: /{}/ /{}/'.format(args.book,book1.rstrip() )  )
            if args.book!=book1.rstrip():
                print("!... .read_book.last filename and current filenames differ! \nFIRST: rm .read_book.last")
                exitme=1
            args.continu=f.readline().rstrip()
            print("i... new args.continu:",args.continu)
    except:
        print("!... file .read_book.last cannot be open")
    finally:
        if exitme==1: sys.exit(1)
        
  
if not (args.continu is None) and args.continu!='':   # if there os args.continu:  take it from that
    argscontinu,temp_name=findlastnum( args.continu)  # return number and hash
else:
    temp_name = next(tempfile._get_candidate_names())
    print("i... new hash name created")
print(  'i...   HASH NAME=',temp_name, ', number=', argscontinu )



with open(".read_book.last", "w" ) as f:
    f.write( args.book+"\n" )
    f.write( "ztrans_"+temp_name+"_00000.mp3" + "\n")
    print("i... .read_book.last was newly created")
#quit()
print("-----------------------------------------------------------------")
time.sleep(0.5)
    

with open( args.book, "r" ) as f:
    text=f.read()
#print(text)    

badfstp=re.findall(r'\.\w', text )
print( len(badfstp),'bad fullstops:' , badfstp)

#print(text)
print('=====================================================was orig')

##### upravy
text=re.sub(r' dr\. ',' dr.',   text)  # tituly
text=re.sub(r' (\w)\. ',' \\1.',text)  # jmena

text=re.sub(r'\n',' ...\n',text)  # silence

text=re.sub(r'\.\.\.\s+','...',text)  # silence

text=re.sub(r"`","'",text)  # bad apostrophes crashed
text=re.sub(r"/"," ",text)  # /NSA/ crashed trans


#print(text)
print('=====================================================was mod')



############################
#  DIRECT    for fun now
###########################
direct=re.findall(r'„.+?“', text )
print(len(direct), 'direct sentences==============================')
for i in range(len(direct)):
    direct[i]=direct[i].strip('„')
    direct[i]=direct[i].strip('“')
    direct[i]=direct[i].strip('"')
    print( i,' ',direct[i] )


    
############################
#  extrasct sentences #############################
###########################
MAXDISP=70
sentences=re.findall(r'([A-Z].+?[\.:?!])[\s"“\n]', text )
for i,v in enumerate( sentences ):
    if i+1<len(sentences):
        if len(v)+len(sentences[i+1])<99:
            sentences[i]=sentences[i]+' '+sentences[i+1]
            del sentences[i+1]
for i,v in enumerate( sentences ):
    if i+1<len(sentences):
        if len(v)+len(sentences[i+1])<99:
            sentences[i]=sentences[i]+' '+sentences[i+1]
            del sentences[i+1]
for i,v in enumerate( sentences ):
    if i+1<len(sentences):
        if len(v)+len(sentences[i+1])<99:
            sentences[i]=sentences[i]+' '+sentences[i+1]
            del sentences[i+1]
            
############################
# 
##############
print( len(sentences),'sentences:===============================' )
if not args.dryrun:
    for i in range(len(sentences)):
        print( "{:4d}".format(i),' ',sentences[i][0:MAXDISP] ,end='')
        if len(sentences[i])>MAXDISP:
            print('...')
        else:
            print()

text2="\n".join( sentences )

with open( args.book+'.v2', 'w' ) as fout:
    fout.write( text2 )
    
print('i...                 ...preparing diff............')
ndif=0
ndifim=0

#
#ndif=difflib.ndiff(  text, text2 )
#print( ''.join(ndif)   )
#for dif in difflib.context_diff( text, text2 ):
#    print( dif )
#
    #for i,s in enumerate( difflib.ndiff(text,text2)):
#    if s[0]==' ': continue
#    elif s[0]=='-' :
#        #print(u'Delete "{}" from position {}'.format(s[-1],i))
#        ndif=ndif+1
#    elif s[0]=='+' :
#        #print(u'Add "{}" to position {}'.format(s[-1],i))    
#        ndif=ndif+1
#    elif s[0]=='-' and len(s[-1])>1:
#        print(u'Delete "{}" from position {}'.format(s[-1],i))
#        ndifim=ndifim+1
#    elif s[0]=='+' and len(s[-1])>1:
#        print(u'Add "{}" to position {}'.format(s[-1],i))    
#        ndifim=ndifim+1
print('Differences:',ndif,' / important:',ndifim)
print()      





#####################################
#  FOR ALL SENTENCES
#
#####################################
#quit()



def parse_all_sentences( argsdryrun, TOTALLINES ):
    global sentences
    if TOTALLINES==0:
        TOTAL=len(sentences)
    else:
        TOTAL=TOTALLINES
    sumoflines=0
    ###print( 'TOTAL==', TOTAL )
    time.sleep(1)
    for i in range(len(sentences)):
        print( " "*int((99+2+9)),      end="\n" )  # \r


        
        sentences[i]=re.sub( '["]', '' ,sentences[i] )  # FIXME:  problem in google with unpaired "
        ####### IF SENTENCE IS LONGER THAN 99
        if len(sentences[i])>99:
            #print("multipart >99:")
            splisen=sentences[i].split()
            parts=''
            j=0
            ##### all parts
            for k,part in enumerate(splisen):
                if len(parts)+len(part)<99-2:
                    parts=parts+' '+part
                else:
                    j=j+1
                    if not argsdryrun:
                        print(  "{:5d}/{:5d} {:d} {}".format( sumoflines ,TOTAL,j, parts )  )
                        res=say_trans( parts,  '{:05d}'.format( sumoflines ) )
                        sumoflines=sumoflines+1
                    else:
                        print(  "{:5d}/{:5d} {:d} {}".format( sumoflines ,TOTAL,j, parts )  )
                        sumoflines=sumoflines+1
                    parts=part
            if len(parts)>0:
                if not argsdryrun:
                    print(   "{:5d}/{:5d} {:d} {}".format( sumoflines,TOTAL,j+1, parts )  )
                    res=say_trans( parts,  '{:05d}'.format( sumoflines ) )
                    sumoflines=sumoflines+1
                else:
                    print(   "{:5d}/{:5d} {:d} {}".format( sumoflines,TOTAL,j+1, parts )  )
                    sumoflines=sumoflines+1
                
        ###### SHORTER < 99
        else:
            #print("... <99")
               
            if not argsdryrun:
                print(  "{:5d}/{:5d} {}{}".format( sumoflines,TOTAL, ' ', sentences[i] ) )
                #print('...saying')
                res=say_trans( sentences[i],  '{:05d}'.format( sumoflines ) )
                #print('...said')
                sumoflines=sumoflines+1
            else:
                print(  "{:5d}/{:5d} {}{}".format( sumoflines,TOTAL, ' ', sentences[i] ) )
                sumoflines=sumoflines+1


                
        ### PERCENTAGE ###
        perc=args.time*sumoflines/3600 / ( args.time*TOTAL/3600 )
        if perc>1: perc=1
        future=datetime.datetime.now() + datetime.timedelta(seconds=args.time*TOTAL)
        ###print('FUTURE=',  future)
        # PROGRESS BAR
        print(" "*int(1*(99-10)), end="\r")
        print( "#"*int(perc*(99-10)),
               "{:.1f}/{:.1f} h (@{}) ".format( args.time*sumoflines/3600 , args.time*TOTAL/3600 ,future.strftime("%H:%M") )   , end="" )
                
        #print(end="\r")
        #time.sleep(0.005)
    return sumoflines






##########################################
#
# CONTINUATION OF MAIN 
#
##########################################

sumoflines=parse_all_sentences( True , 0 )
print()
print('-------------------------------------------------')            
print('total: {} lines   estimation:  {:.1f}'.format( sumoflines, args.time*sumoflines/3600 ) ,'hours' )

if args.dryrun: quit()
time.sleep(0.5)


START=datetime.datetime.now()
parse_all_sentences( False , sumoflines )

# SIMPLE  join        
print("\n\ncat ztrans_"+temp_name+"*.mp3 > \""+args.book+".mp3\"")
print("\n\nmp3val "+args.book+".mp3 -f -nb \n\n ")
print("\n\ncat ztrans_"+temp_name+"*.mp3 > \""+os.path.basename(args.book)+".mp3\"")
print("\n\nmp3val \""+os.path.basename(args.book)+".mp3\" -f -nb\n")

tmdelta=(datetime.datetime.now() - START)
print( str(tmdelta) , '  total time' )
