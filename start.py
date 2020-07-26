import PySimpleGUI as sg
import os
import sys
import PIL
from PIL import Image
from getdata import getdata
import time
import pyautogui as gui
import datetime
import scipy.misc
import numpy as np
from model import DCGAN
from utils import pp, visualize, to_json, show_all_variables
import tensorflow as tf
import threading

sg.theme("Topanga")             #set theme


#Thread definitions
###########################################################################################
def network_thread():               #netwok start function
    tf.app.run()

def start_train_thread():                                       #start network thread
    threading.Thread(target=network_thread,daemon=True).start()

def time_thread():                              #thread to keep track of time
    print("Time:Time thread started")
    while True:
        window.FindElement('_time_').Update(getTime())
        time.sleep(1)
        
def start_time_thread():                                    #starts the time thread
    threading.Thread(target=time_thread,daemon=True).start()
###########################################################################################


#utility function definitions
###########################################################################################
def getTime():                                              #function to get the current time and format it
    return datetime.datetime.now().strftime('%H:%M:%S')

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
                img.save("complete/"+image)           

###########################################################################################


#Main network function
###########################################################################################
def main(_):                                                #main network initialization function
  print("LILLIAN:Initializing Network")
  pp.pprint(flags.FLAGS.__flags)

  if FLAGS.input_width is None:
    FLAGS.input_width = FLAGS.input_height
  if FLAGS.output_width is None:
    FLAGS.output_width = FLAGS.output_height

  if not os.path.exists(FLAGS.checkpoint_dir):
    os.makedirs(FLAGS.checkpoint_dir)
  if not os.path.exists(FLAGS.sample_dir):
    os.makedirs(FLAGS.sample_dir)

  gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1)
  run_config = tf.ConfigProto()
  run_config.gpu_options.allow_growth=True

  with tf.Session(config=run_config) as sess:               #configure network
    if FLAGS.dataset == 'mnist':
      print("LILLIAN:Flag is set to MNST")
      dcgan = DCGAN(
          sess,
          input_width=xm,
          input_height=ym,
          output_width=xm,
          output_height=ym,
          batch_size=batchsz,
          sample_num=batchsz,
          y_dim=10,
          z_dim=1,
          dataset_name=key,
          input_fname_pattern="*.jpg",
          crop=True,
          checkpoint_dir="checkpoint",
          sample_dir="samples",
          data_dir="./data")
    else:
      dcgan = DCGAN(
          sess,
          input_width=xm,
          input_height=ym,
          output_width=xm,
          output_height=ym,
          batch_size=batchsz,
          sample_num=batchsz,
          z_dim=1,
          dataset_name=key,
          input_fname_pattern="*.jpg",
          crop=True,
          checkpoint_dir="checkpoint",
          sample_dir="samples",
          data_dir="./data")

    show_all_variables()                #show all variables

    if FLAGS.train:
      dcgan.train(FLAGS)
    else:
      if not dcgan.load(FLAGS.checkpoint_dir)[0]:
        raise Exception("LILLIAN:Error:Train a model first, then run test mode")
      

    OPTION = 1
    visualize(sess, dcgan, FLAGS, OPTION)       #Visualize network
###########################################################################################


#UI function
###########################################################################################
layout = [                                                                          #UI Layout
          [sg.Text("key"),sg.Input(),sg.Image(filename="logo.png")],
          [sg.Text("Epoches"),sg.Slider(range=(1,500),orientation='h'),sg.Text('   Time: '),sg.Text('', key='_time_',size=(20,1))],
          [sg.Text('Batches '),sg.Slider(range=(1,64),orientation='h'),sg.Checkbox(text="USE GPU",default=True)],
          [sg.Button("Start"),sg.Text('LOG')],
          [sg.Output(size=(65,5))],
          [sg.Button("EXIT")]
          ]
window = sg.Window("LILIAN", layout)        #initialize the window

timeinitialized = False

while True:                                 #UI function
    event, value = window.read()
    if timeinitialized == False:        #check if the time thread has been started, if not start it
        start_time_thread()
        timeinitialized = True


    if event == sg.WIN_CLOSED:              #exit program if the window is closed
        exit()

    if event == "Start":                    #check for the start button to be pressed

        if timeinitialized == False:        #check if the time thread has been started, if not start it
            start_time_thread()
            timeinitialized = True


        print(value)
        key = value[0]                      #set network configuration based on UI input
        epoch = int(value[2])
        batchsz = int(value[3])

        if value[4] == False:                           #disable the GPU device if unchecked in UI
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
            print("Manager:USING CPU")

        print("Manager:USING GPU")
        print("Manager:Epoch set to "+str(epoch))
        print("Manager:Key set to "+str(key))
        print("Manager:Scanning Data")

        for thing in os.listdir("data/"+key+"/"):                                               #verify images in data directory
            if thing.endswith(".jpg" or ".png" or ".jpeg") & verify_image(thing) == False:
                os.remove("data/"+key+"/"+thing)                                                #Removes bad images

        xm,ym = getdata(key)
        xm = xm
        ym = ym
    
        print("Manager:Current time is " +str(datetime.datetime.now()))                         #get time and display in debug window


        flags = tf.app.flags                                                                    #set network flags
        flags.DEFINE_integer("epoch", epoch," ")
        flags.DEFINE_float("learning_rate", 0.0002," ")
        flags.DEFINE_float("beta1", 0.5," ")
        flags.DEFINE_float("train_size", np.inf," ")
        flags.DEFINE_integer("batch_size", batchsz,"")
        flags.DEFINE_integer("input_height", ym," ")
        flags.DEFINE_integer("input_width", xm," ")
        flags.DEFINE_integer("output_height", ym," ")
        flags.DEFINE_integer("output_width", xm," ")
        flags.DEFINE_string("dataset", key," ")
        flags.DEFINE_string("input_fname_pattern","*.jpg"," ")
        flags.DEFINE_string("checkpoint_dir", "checkpoint"," ")
        flags.DEFINE_string("data_dir", "./data"," ")
        flags.DEFINE_string("sample_dir", "samples"," ")
        flags.DEFINE_boolean("train", True," ")
        flags.DEFINE_boolean("crop", True," ")
        flags.DEFINE_boolean("visualize", True," ")
        flags.DEFINE_integer("generate_test_images", 1," ")
        FLAGS = flags.FLAGS

        start_train_thread()                                        #start the training thread
        print("Manager:function returned")


    if event == sg.WIN_CLOSED:              
        exit()
    if event == "EXIT":
        exit()

