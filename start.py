import PySimpleGUI as sg
import os
import sys
import PIL
from PIL import Image
from getdata import getdata
from time import sleep
import pyautogui as gui
from datetime import datetime
import scipy.misc
import numpy as np
from model import DCGAN
from utils import pp, visualize, to_json, show_all_variables
import tensorflow as tf
import threading

sg.theme("Topanga")             #set theme


#Thread definitions
###########################################################################################

completed =False
def update_thread():
    while completed == False:
        time.sleep(10)
        if trainthread.is_alive() == False:
            print("Completed!")
            completed == True
            break

    return()

def start_update_thread():
    print("Update:update thread started")
    updatethread.start()

def network_thread():               #netwok start function
    tf.app.run()

def start_train_thread():                                       #start network thread
    print("Network:Network thread started")
    trainthread.start()


def time_thread():                              #thread to keep track of time
    print("Time:Time thread started")
    # while True:
    #     window.FindElement('_time_').Update(getTime())
    #     time.sleep(1)

def start_time_thread():                                    #starts the time thread
    threading.Thread(target=time_thread,daemon=True).start()

trainthread = threading.Thread(target=network_thread,daemon=True)
updatethread = threading.Thread(target=update_thread,daemon=True)
###########################################################################################


#utility function definitions
###########################################################################################



def getTime():                                              #function to get the current time and format it
    return datetime.now().strftime('%H:%M:%S')

def verify_image(img_file):             #Checks wheather or not an image file is valid
     try:
        v_image = Image.open(img_file)
        v_image.verify()
        return False
        print("valid file: "+str(img_file))

     except OSError:
        return True                     #returns the state of the image file

def resize1():                          #resizes all the images in the complete directory
    print("Resizing")
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

ui_back, ui_mid, ui_front, ui_text = '#373737', '#404040', '#505050', '#A4A4A4'
sg.theme_background_color(ui_mid)
sg.theme_button_color((ui_text, ui_back))
sg.theme_element_background_color(ui_mid)
sg.theme_input_background_color(ui_back)
sg.theme_text_element_background_color(ui_mid)      # Set up custom theme
sg.theme_element_text_color('white')
sg.theme_input_text_color('white')
sg.theme_text_color(ui_text)
sg.theme_element_text_color(ui_text)
sg.theme_input_text_color(ui_text)
# sg.theme('SystemDefaultForReal')

frame1 = [[sg.Text('Key:         '), sg.Input(size=(12,1))],
          [sg.Text('Epochs:     '), sg.Spin([i for i in range(1, 501)], 5, size=(10,1))],
          [sg.Text('Batch Size:'), sg.Spin([i for i in range(1, 65)], 1, size=(10,1))],
          [sg.Radio('CPU', 1), sg.Radio('GPU', 1, True)]]

frame2 = [[sg.ProgressBar(100, size=(52,8), bar_color=(ui_front, ui_back), key='prog')],
          [sg.Output((80,7))]]

layout = [[sg.Column([[sg.Frame('Setup', frame1)],
                      [sg.Button('Start', size=(8,1)),
                       sg.Button('Stop', size=(6,1), disabled=True),
                       sg.Button('Exit', size=(4,1))]]),
           sg.Frame('Status', frame2)],
          [sg.StatusBar('Start Time:         '+('    '*5)+'Elapsed Time:         ', size=(100,1), key='status')]]

window = sg.Window('LILLIAN', layout, icon='./icons/logo-flat.ico') #logo-flat2 for dark ico

def errorcheck():
    if value[0] == '':
        print('ERROR: Missing key')
        return ValueError
    if int(value[1]) <= 0:
        print('ERROR: Epochs must be >0')
        return ValueError
    if int(value[2]) <= 0:
        print('ERROR: Batch size must be >0')
        return ValueError

timeinitialized = False

while True:
    event, value = window.read()            #initialize the window

    if errorcheck() == ValueError: continue

    if event == sg.WIN_CLOSED:              #exit program if the window is closed
        window.close()
        exit()

    if event == "Start":                    #check for the start button to be pressed

        if timeinitialized == False:        #check if the time thread has been started, if not start it
            start_time_thread()
            timeinitialized = True

        try:
            key = value[0]                  #set network configuration based on UI input
            epoch = int(value[1])
            batchsz = int(value[2])
        except TypeError:
            print('ERROR: Epoch and batch must be integers.')
            continue

        if value[4] == False:
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"        #disable the GPU device if unchecked in UI
            print("Manager:USING CPU")
        else: print("Manager:USING GPU")

        print("Manager:Epoch set to "+str(epoch))
        print("Manager:Key set to "+str(key))
        print("Manager:Verifying data structure integrity")

        for thing in os.listdir("data/"+key+"/"):                                               #verify images in data directory
            if thing.endswith(".jpg" or ".png" or ".jpeg") & verify_image(thing) == False:
                os.remove("data/"+key+"/"+thing)                                                #Removes bad images

        xm,ym = getdata(key)
        xm = xm
        ym = ym

        print("Manager:Current time is " +str(datetime.now()))      #get time and display in debug window
        window['Start'].Update(disabled=True)
        window['Stop'].Update(disabled=False)                                # Update Buttons


        flags = tf.app.flags                                                 #set network flags
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
        print("Manager:Training thread returned")
        start_update_thread()

    if event in (sg.WIN_CLOSED, 'Exit'):
        window.close()
        exit()
