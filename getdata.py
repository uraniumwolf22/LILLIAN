
import os
from PIL import Image
import sys

def getdata(key):

   xt = 100000
   yt = 100000
   dir = os.listdir("data/"+key+"/")

   for images in dir:                       #remove thumbnail files
      if images.endswith(".db") == False:
          try:
            im = Image.open("data/"+key+"/"+images)
          except(OSError) as e:
              print(e)

      x,y = im.size  #look for largest image
      if x < xt:
         xt = x
      if y < yt:
         yt = y
   return xt,yt
