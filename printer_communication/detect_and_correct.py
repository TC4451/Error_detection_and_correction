from to_printcore_by_layer import send_gcode
from gcode_layer_correction import generate_correction_gcode
from camera_control import take_picture

gcode_path = 'printer_communication/gcode/SmallBellow_newwoutTri.gcode'
layerID = 1

def detect_error(layer_num):
    send_gcode("printer_communication/layerwise_gcode_file/layer_{}.gcode".format(layer_num))
    # take_picture()
    # !!! need to think about how to take picture while it is waiting

def correct_error(gcode_path, layerID):
    img_path = 'printer_communication/elp_test/layer_{}.jpg'.format(layerID)
    cor_gcode_dir = "printer_communication/correction_gcode_file/"
    output_path = cor_gcode_dir + "layer_{}_cor.gcode".format(layerID)
    generate_correction_gcode(img_path, gcode_path, layerID, output_path)
    send_gcode(output_path)

# send_gcode("printer_communication/layerwise_gcode_file/layer_{}.gcode".format(0))
# detect_error(1)
# correct_error(gcode_path, 1)
import cv2
from PIL import Image, ImageOps, ImageFilter
import matplotlib.pyplot as plt
import numpy as np
from transitions import Machine
cap = cv2.VideoCapture(1)
# !!!change this
total_layer = 239
while(cap.isOpened()): # check camera status
    layerID = 1
    send_gcode("printer_communication/layerwise_gcode_file/layer_{}.gcode".format(0))
    for layer in range(total_layer):
        send_gcode("printer_communication/layerwise_gcode_file/layer_{}.gcode".format(layer))
        ret_flag,Vshow = cap.read()
        img_path = 'printer_communication/elp_test/layer_{}.jpg'.format(layer)
        # save image
        cv2.imwrite(img_path,Vshow)
        cor_gcode_dir = "printer_communication/correction_gcode_file/"
        output_path = cor_gcode_dir + "layer_{}_cor.gcode".format(layer)
        # !!! go in this function to change gcode
        generate_correction_gcode(img_path, gcode_path, layer, output_path)
        send_gcode(output_path)
    break
cap.release() # release storage