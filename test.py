import time

def gettimefromfile():
    while True:
        with open("datapipe.txt","r") as file:
            file = file.read()
            if file == "":
                file = '__keeplast__'

            if time.localtime().tm_sec % 2 == 1:
                break
    return(file)
while True:
    print(gettimefromfile())