import os
import sys
import time as t
def formatf():
    with open("output.txt","r") as file:
            global filef
            filef = file.read()

    filef = filef.replace("{","")
    filef = filef.replace("}","")

    ffile = filef.replace("::"," ")

    ffile = ffile.replace(": ",":")

    ffile = ffile.replace(" ",":")

    ffile = ffile.replace("'","")

    global array
    array = ffile.split(":")
    
loop = True
while loop == True:
    formatf()
    global call
    call = input()
    if(call.find("is") != -1):
        callarray = call.split(" ")
        last = len(callarray)
        call = callarray[last-1]
        print(callarray[last-1] + " is")
    
    pos = array.index(call)
    output = array[pos+1]
    print(output)
