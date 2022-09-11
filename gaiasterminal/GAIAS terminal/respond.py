import sys
import time
import os
from gtts import gTTS
import numpy as np
import playsound


def flush(textfile):
    with open(textfile,"w") as some_file:
        some_file.close()

def dwrite(data):
    with open("output.txt","w") as some_file:
        some_file.write(data)

def tts(textin):
    language = 'en'
    sound = gTTS(text=textin,lang=language,slow=False)
    sound.save("tts.mp3")
    playsound.playsound("tts.mp3",True)

speechin = "speechout.txt"
speechout = "output.txt"

def command():
    with open("speechout.txt","r") as some_file:
        global out
        out = some_file.read()
    if(out == "can you hear me"):
        print("yes")
        dwrite("yes")
        tts("yes")
        flush(speechin)
    elif(out == "who am I"):
        print("admin")
        dwrite("admin")
        tts("admin")
        flush(speechin)
    elif(out == "who are you"):
         print("GAIAS")
         dwrite("GAIAS")
         tts("guias")
         flush(speechin)
         
    else:
        do = True
        return(do)
do = command()
loop = True
while loop == True:
    if(do == True):
        command()
