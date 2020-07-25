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

sg.theme("Topanga")

def network_thread():
    tf.app.run()

def start_train_thread():
    threading.Thread(target=network_thread,daemon=True).start()




def time_thread():
    while True:

        
        window.FindElement('_time_').Update(getTime())
        time.sleep(1)


def start_time_thread():
    threading.Thread(target=time_thread,daemon=True).start()



def getTime():
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



def main(_):
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

  with tf.Session(config=run_config) as sess:
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

    show_all_variables()

    if FLAGS.train:
      dcgan.train(FLAGS)
    else:
      if not dcgan.load(FLAGS.checkpoint_dir)[0]:
        raise Exception("LILLIAN:Error:Train a model first, then run test mode")
      

    OPTION = 1
    visualize(sess, dcgan, FLAGS, OPTION)



layout = [[sg.Text("key"),sg.Input(),sg.Text("Epoches"),sg.Slider(range=(1,500),orientation='h'),sg.Image(filename="logo.png")],
          [sg.Text('Batch Size'),sg.Slider(range=(1,64),orientation='h')],
          [sg.Checkbox(text="USE GPU",default=True)],
          [sg.Button("Start"),sg.Text('Time: '), sg.Text('', key='_time_',size=(20,1)),sg.Text('LOG')],
          #[sg.Output(size=(110,5))],
          [sg.Button("EXIT")]
          ]
window = sg.Window("LILIAN", layout)

while True:
    event, value = window.read()
    
    if event == sg.WIN_CLOSED:
        exit()

    if event == "Start":
        print(value)
        key = value[0]
        epoch = int(value[1])
        batchsz = int(value[3])

        if value[4] == False:
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
            print("LILLIAN:USING CPU")

        print("LILLIAN:USING GPU")
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



        flags = tf.app.flags
        flags.DEFINE_integer("epoch", epoch," ")
        flags.DEFINE_float("learning_rate", 0.0002," ")
        flags.DEFINE_float("beta1", 0.5," ")
        flags.DEFINE_float("train_size", np.inf," ")
        flags.DEFINE_integer("batch_size", 1,"")
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

        start_train_thread()
        print("LILLIAN:function returned")
        start_time_thread()


    if event == sg.WIN_CLOSED:
        exit()
    if event == "EXIT":
        exit()


#print("LILLIAN:Moving files")
#for samples in os.listdir("samples/"):                              #moves files
    #os.rename("samples/"+samples,"complete/"+samples)

#print("LILLIAN:Time complete "+str(datetime.datetime.now()))
#print("LILLIAN:Complete!")

