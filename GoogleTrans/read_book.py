#!/usr/bin/python3

import argparse

import re

import difflib  # compare two strings

import subprocess
import time
import sys       # flush
import tempfile

import datetime
parser=argparse.ArgumentParser(description="""
 ... 
""")


parser.add_argument('-b','--book',  default="", help='',required=True)

parser.add_argument('-c','--continu',  default=0,type=int, help='')
parser.add_argument('-t','--time',  default=14, type=int, help='seconds between questions')
parser.add_argument('-p','--path_to_save',  default="./", help='')
parser.add_argument('-d','--dryrun', action="store_true", help='')

args=parser.parse_args() 

temp_name = next(tempfile._get_candidate_names())
print(  temp_name )


def countdown(ti):
    global temp_name
    global args
    print('-'*ti, end='\r')
    for i in range( int(ti) ):
        print('#', end='')
        sys.stdout.flush()
        time.sleep( 1 )
    print()



    
def say_trans( phrase, ssi ):
    global temp_name
    global args
    MEASURE=datetime.datetime.now()
    #trans -b -p -no-auto cs:cs "$PHRASE" -player "mpv --speed 0.9 --volume 100 -ao pcm:file=\"$DESTINATION/$PHRASE.wav\""
    #lame --scale 3 "$DESTINATION/$PHRASE.wav"
    #rm   "$DESTINATION/$PHRASE.wav"
    ###################################################
    DEST='/tmp/trans_'+temp_name+'_'+ssi
    ###################################################
    print('i... saving',DEST,' / ',args.continu, int(ssi) )
    if args.continu<=int(ssi):
        #########################    trans
        CMD='trans -b -p -no-auto cs:cs "'+phrase+'" -player "mpv --speed 1.3 --volume 100 -ao pcm:file='+DEST+'.wav"'

        ### HERE I have seen an error: I ADD TRY:
        # this waits finishing the call
        try:
            res=subprocess.check_call(CMD, shell=True)
        except subprocess.CalledProcessError, e:
            print( '!...trans command ERROR', e.output  )
            print('i... TRY ONCE MORE after 30 sec.')
            time.sleep(30)
            try:
                res=subprocess.check_call(CMD, shell=True)
            except subprocess.CalledProcessError, e:
                print( '!...trans command ERROR', e.output  )
                quit()
                return 1
        ########################## LAME
        #CMD='lame --scale 2 '+DEST+'.wav  2>/dev/null'
        CMD='lame --scale 2 '+DEST+'.wav  '
        #res=subprocess.check_call(CMD, shell=True)
        res=subprocess.check_call(CMD, shell=True)
        if res!=0:
            print('!...LAME ERROR')
            quit()
            return 1
    
        ########################## rm WAV
        DEST=re.sub('\s','',DEST)
        CMD='rm '+DEST+'.wav'
        if DEST.find('/tmp')!=0:
            print('!... security error')
            quit()
        res=subprocess.check_call(CMD, shell=True)
        if res!=0:
            print("!... RM ERROR")
            quit()
            return 1

        remains=args.time - (datetime.datetime.now() - MEASURE).seconds
        if remains<0: remains=0
        print('countdown:')
        countdown( remains )
    
    return 0









############################################
#
#  M A I N
#
###########################################
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

text=re.sub(r"`","'",text)  # silence

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
            print("... >99")
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
            print("... <99")
               
            if not argsdryrun:
                print(  "{:5d}/{:5d} {}{}".format( sumoflines,TOTAL, ' ', sentences[i] ) )
                print('...saying')
                res=say_trans( sentences[i],  '{:05d}'.format( sumoflines ) )
                print('...said')
                sumoflines=sumoflines+1
            else:
                print(  "{:5d}/{:5d} {}{}".format( sumoflines,TOTAL, ' ', sentences[i] ) )
                sumoflines=sumoflines+1

        ### PERCENTAGE ###
        perc=args.time*sumoflines/3600 / ( args.time*TOTAL/3600 )
        if perc>1: perc=1
        future=datetime.datetime.now() + datetime.timedelta(seconds=args.time*TOTAL)
        ###print('FUTURE=',  future)
        print( "#"*int(perc*(99-10)),
               "{:.1f}/{:.1f} h (@{})".format( args.time*sumoflines/3600 , args.time*TOTAL/3600 ,future.strftime("%H:%M") ),
               end="\n" )
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
time.sleep(5)


START=datetime.datetime.now()
parse_all_sentences( False , sumoflines )

# SIMPLE  join        
print("\n\n cat trans_*.mp3 > out.mp3 \n\n  mp3val out.mp3 -f -nb \n\n ")
print( (datetime.datetime.now() - START).seconds , 's  total time' )
