#!/usr/bin/python3

import argparse

import re

import difflib  # compare two strings

import subprocess
import time
import sys       # flush
import tempfile

parser=argparse.ArgumentParser(description="""
 ... 
""")


parser.add_argument('-b','--book',  default="", help='',required=True)
parser.add_argument('-c','--cross',   action="store_true" , help='')
parser.add_argument('-t','--time',  default=9, type=int, help='seconds between questions')
parser.add_argument('-p','--path_to_save',  default="./", help='')
parser.add_argument('-d','--dryrun', action="store_true", help='')
args=parser.parse_args() 

temp_name = next(tempfile._get_candidate_names())
print(  temp_name )


def countdown(ti):
    global temp_name
    global args
    print('-'*ti, end='\r')
    for i in range(ti):
        print('#', end='')
        sys.stdout.flush()
        time.sleep( 1 )
    print()



    
def say_trans( phrase, ssi ):
    global temp_name
    global args
    #trans -b -p -no-auto cs:cs "$PHRASE" -player "mpv --speed 0.9 --volume 100 -ao pcm:file=\"$DESTINATION/$PHRASE.wav\""
    #lame --scale 3 "$DESTINATION/$PHRASE.wav"
    #rm   "$DESTINATION/$PHRASE.wav"
    ###################################################
    DEST='/tmp/trans_'+temp_name+'_'+ssi
    ###################################################
    print('i... saving',DEST)
    CMD='trans -b -p -no-auto cs:cs "'+phrase+'" -player "mpv --speed 1.3 --volume 100 -ao pcm:file='+DEST+'.wav"'
    res=subprocess.check_call(CMD, shell=True)
    if res!=0:
        quit()
        return 1
    ##########################
    CMD='lame --scale 2 '+DEST+'.wav'
    res=subprocess.check_call(CMD, shell=True)
    if res!=0:
        quit()
        return 1
    
    ##########################
    DEST=re.sub('\s','',DEST)
    CMD='rm '+DEST+'.wav'
    if DEST.find('/tmp')!=0:
        print('!... security error')
        quit()
    res=subprocess.check_call(CMD, shell=True)
    if res!=0:
        quit()
        return 1


    countdown( args.time )
    
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
print( len(sentences),'sentences:===============================' )
if not args.dryrun:
    for i in range(len(sentences)):
        #if i in direct:
        #print('=DIR: =',end="")
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
for i in range(len(sentences)):
    #if i in direct:
        #print('=DIR: =',end="")
    #print( "{:4d}  L:{:3d}".format(i,len(sentences[i])),' ',sentences[i][0:MAXDISP] ,end='')
    if len(sentences[i])>MAXDISP:
        print('...')
    else:
        print()
    sentences[i]=re.sub( '["]', '' ,sentences[i] )  # FIXME:  problem in google with unpaired "
    ####### IF SENTENCE IS LONGER THAN 99
    if len(sentences[i])>99:
        splisen=sentences[i].split()
        parts=''
        j=0
        for k,part in enumerate(splisen):
            if len(parts)+len(part)<99-2:
                parts=parts+' '+part
            else:
                j=j+1
                print(i,'/',j,' ',parts)
                if not args.dryrun:
                    res=say_trans( parts,  '{:05d}'.format(i) )
                else:
                    print(parts)
                parts=''
        if len(parts)>0:
            if not args.dryrun:
                res=say_trans( parts,  '{:05d}'.format(i) )
            else:
                print(parts)
            
    ###### SHORTER 99
    else:
        if not args.dryrun:
            res=say_trans( sentences[i],  '{:05d}'.format(i) )
        else:
            print( sentences[i] )

# SIMPLE  join        
#cat trans_rxu4l70y_0* > out.mp3   ; mp3val out.mp3 -f -nb 
