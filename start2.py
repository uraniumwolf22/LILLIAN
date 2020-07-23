#Lillian GAN system by Logan Ross
#Requires Cuda 8.0
#Requires Cudnn Version 6 for Cuda 8.0
#Requires Tensorflow Version 1.4.0
#GPU toggle is found in model.py
#run from the python file "runner" in /python35
#Make sure runner is added to path

import os
import sys
import PIL
from PIL import Image
from getdata import getdata
import time
import pyautogui as gui
import datetime

user_present = True                     #set wheather a user is present
epoch_defualt = 5000                    #the default number of epoches
key_default = "stone"                   #Default key if user is not active

def verify_image(img_file):             #Checks wheather or not an image file is valid
     try:
        v_image = Image.open(img_file)
        v_image.verify()
        return False
        print("valid file: "+str(img_file))

     except OSError:
        return True                     #returns the state of the image file

def resize1():                          #resizes all the images in the complete directory
    print("Resizeing")
    while True:
        for image in os.listdir("complete/"): 
            basewidth = 1000
            if image.endswith(".jpg" or ".png"):                        #Check image type
                img = Image.open("complete/"+image+"/")
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth,hsize), Image.ANTIALIAS)    #Resize based on the base width
                img.save("complete/"+image)                             #save the image to the same directory

def main():
    if user_present == True:
        start = gui.confirm(text="WELCOME TO LILLIAN",                  #prompts the user if they would like to start or shutdown (default screen)
        title="LILLIAN",buttons=['start','shutdown'])
    else:
        start = "Started by machine"

    print("user:"+start)                                                #Continues based on user input
    if start == "shutdown":
        print("LILLIAN:Shutting Down")
        exit()
    else:
        print("LILLIAN:Starting")

    print("LILLIAN:Prompting for key")

    if user_present == True:                                        #set key to user input
        key = gui.prompt(text="search for",title="FCGAN")
    else:
        key = key_default                                           #set key to default if in headless mode


    if user_present == True:                                            #sets the number of epoches based on user input
        epoch = gui.prompt(text="Number of epoches",title="LILLIAN")
        epoch = int(epoch)
    else:
        epoch = epoch_defualt                                           #sets to default if in headless mode

    print("LILLIAN:Epoch set to "+str(epoch))
    print("LILLIAN:Key set to "+str(key))
    print("LILLIAN:Scanning Data")

    for thing in os.listdir("data/"+key+"/"):                                               #verify images in data directory
        if thing.endswith(".jpg" or ".png" or ".jpeg") & verify_image(thing) == False:
            os.remove("data/"+key+"/"+thing)                                                #Removes bad images

    xm,ym = getdata(key)
    xm = xm
    ym = ym
    
    print("LILLIAN:Current time is " +str(datetime.datetime.now()))
    os.system("runner.exe main.py --dataset "+key+" --input_height="+str(ym)+" --input_width="+str(xm)+
        " --output_height="+str(ym)+" --output_width="+str(xm)+" --epoch="+str(epoch)+" --generate_test_images=1 --batch_size=1 --visualize=True --train --crop")  #runs main program

    print("LILLIAN:Moving files")
    for samples in os.listdir("samples/"):                              #moves files
        os.rename("samples/"+samples,"complete/"+samples)

    print("LILLIAN:Time complete "+str(datetime.datetime.now()))
    print("LILLIAN:Complete!")

if __name__ == "__main__":                                              #Runs main program
    main()