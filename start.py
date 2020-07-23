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

sg.theme("dark")
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


layout = [[sg.Text("key"),sg.Input(),sg.Text("Epoches"),sg.Input(),sg.Image(filename="logo.png")],
          [sg.Button("Start")],[sg.Output(size=(120,20))],
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
        break

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
#os.system("runner.exe main.py --dataset "+key+" --input_height="+str(ym)+" --input_width="+str(xm)+
#    " --output_height="+str(ym)+" --output_width="+str(xm)+" --epoch="+str(epoch)+" --generate_test_images=1 --batch_size=1 --visualize=True --train --crop")  #runs main program



flags = tf.app.flags
flags.DEFINE_integer("epoch", epoch, "Epoch to train [25]")
flags.DEFINE_float("learning_rate", 0.0002, "Learning rate of for adam [0.0002]")
flags.DEFINE_float("beta1", 0.5, "Momentum term of adam [0.5]")
flags.DEFINE_float("train_size", np.inf, "The size of train images [np.inf]")
flags.DEFINE_integer("batch_size", 1, "The size of batch images [64]")
flags.DEFINE_integer("input_height", ym, "The size of image to use (will be center cropped). [108]")
flags.DEFINE_integer("input_width", xm, "The size of image to use (will be center cropped). If None, same value as input_height [None]")
flags.DEFINE_integer("output_height", ym, "The size of the output images to produce [64]")
flags.DEFINE_integer("output_width", xm, "The size of the output images to produce. If None, same value as output_height [None]")
flags.DEFINE_string("dataset", key, "The name of dataset [celebA, mnist, lsun]")
flags.DEFINE_string("input_fname_pattern", "*.jpg", "Glob pattern of filename of input images [*]")
flags.DEFINE_string("checkpoint_dir", "checkpoint", "Directory name to save the checkpoints [checkpoint]")
flags.DEFINE_string("data_dir", "./data", "Root directory of dataset [data]")
flags.DEFINE_string("sample_dir", "samples", "Directory name to save the image samples [samples]")
flags.DEFINE_boolean("train", True, "True for training, False for testing [False]")
flags.DEFINE_boolean("crop", True, "True for training, False for testing [False]")
flags.DEFINE_boolean("visualize", True, "True for visualizing, False for nothing [False]")
flags.DEFINE_integer("generate_test_images", 1, "Number of images to generate during test. [100]")
FLAGS = flags.FLAGS

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
          input_width=FLAGS.input_width,
          input_height=FLAGS.input_height,
          output_width=FLAGS.output_width,
          output_height=FLAGS.output_height,
          batch_size=FLAGS.batch_size,
          sample_num=FLAGS.batch_size,
          y_dim=10,
          z_dim=FLAGS.generate_test_images,
          dataset_name=FLAGS.dataset,
          input_fname_pattern=FLAGS.input_fname_pattern,
          crop=FLAGS.crop,
          checkpoint_dir=FLAGS.checkpoint_dir,
          sample_dir=FLAGS.sample_dir,
          data_dir=FLAGS.data_dir)
    else:
      dcgan = DCGAN(
          sess,
          input_width=FLAGS.input_width,
          input_height=FLAGS.input_height,
          output_width=FLAGS.output_width,
          output_height=FLAGS.output_height,
          batch_size=FLAGS.batch_size,
          sample_num=FLAGS.batch_size,
          z_dim=FLAGS.generate_test_images,
          dataset_name=FLAGS.dataset,
          input_fname_pattern=FLAGS.input_fname_pattern,
          crop=FLAGS.crop,
          checkpoint_dir=FLAGS.checkpoint_dir,
          sample_dir=FLAGS.sample_dir,
          data_dir=FLAGS.data_dir)

    show_all_variables()

    if FLAGS.train:
      dcgan.train(FLAGS)
    else:
      if not dcgan.load(FLAGS.checkpoint_dir)[0]:
        raise Exception("LILLIAN:Error:Train a model first, then run test mode")
      

    OPTION = 1
    visualize(sess, dcgan, FLAGS, OPTION)

tf.app.run()

print("LILLIAN:Moving files")
for samples in os.listdir("samples/"):                              #moves files
    os.rename("samples/"+samples,"complete/"+samples)

print("LILLIAN:Time complete "+str(datetime.datetime.now()))
print("LILLIAN:Complete!")

while True:
    if event == sg.WIN_CLOSED:
        exit()
    if event == "EXIT":
        exit()