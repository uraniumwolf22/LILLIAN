import speech_recognition as sr
import sys
import os
loop = True
while loop == True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("-")
        audio = r.listen(source)
 

    try:
        global output
        output = ""
        output = r.recognize_google(audio)
        print(output)
        file = open("speechout.txt","w")
        file.write(output)
    except sr.UnknownValueError:
        print(".")
    except sr.RequestError as e:
        print("service down")
    with open('speechout.txt', 'w') as the_file:
        output = output.lower()
        the_file.write(output)
