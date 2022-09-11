import playsound
from gtts import gTTS
import os
loop = True
while loop == True:
    try:
        def flush(textfile):
            with open(textfile,"w") as some_file:
                some_file.close()
        with open("output.txt","r") as some_file:
                global response
                response = some_file.read()
        print(response)
        language = 'en'

        myobj = gTTS(text=response, lang=language, slow=False)
        myobj.save("welcome.mp3")


        playsound.playsound("welcome.mp3",True)
        flush("output.txt")
    except:
        pass
