from google.cloud import vision
from google.cloud.vision_v1 import types
import cv2 
import pandas as pd
from web import web_stuff
l_label,df_web,my_confidence,annotations = web_stuff('photos\image1.jpg')

from loc import localize_objects,find_prop
objects = localize_objects('photos\image1.jpg')
image,df_location = find_prop('photos\image1.jpg',objects)
print(df_location)