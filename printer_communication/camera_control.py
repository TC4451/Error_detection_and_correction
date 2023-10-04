import cv2
from PIL import Image, ImageOps, ImageFilter
import matplotlib.pyplot as plt
import numpy as np
from transitions import Machine

def take_picture(img_dir, layerID):
    cap = cv2.VideoCapture(1)
    Vshow = cap.read() # get img
    cv2.imwrite(img_dir + "layer_{}.jpg".format(layerID),Vshow) #route
    print("success to save layer_{}.jpg".format(layerID))
    cap.release() # release storage

def camera(img_dir, layerID):
    cap = cv2.VideoCapture(1)
    while(cap.isOpened()): # check camera status
        ret_flag,Vshow = cap.read() # get img
        # cv2.imshow("Capture_Test",Vshow) # display img
        # k = cv2.waitKey(1) & 0xFF
        # if k == ord('s'): # press S to save
        cv2.imwrite(img_dir+str(layerID)+".jpg",Vshow) #route
        # elif k == ord(' '): #press ' ' to exit
        break

    cap.release() # release storage
    # cv2.destroyAllWindows() # exit and close all window

# take_picture("", 1)
camera("", 1)