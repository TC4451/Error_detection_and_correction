import cv2
# from to_printcore_by_layer import send_gcode
from projection_elp import get_defect_positions
from gcode_ironing import generate_iron_layer
from printrun.printcore import printcore
from printrun import gcoder
import time
import json
import sys

gcode_path = 'printer_communication/gcode/SmallBellow_newwoutTri.gcode'
layer_gcode_path = 'printer_communication/layerwise_gcode_file/'
cor_gcode_path = 'printer_communication/correction_gcode_file/'
total_layer = 239

# open camera
# cap = cv2.VideoCapture(1)

def print(path):
    print_core = printcore('COM3', 115200)
    gcode0 = [i.strip() for i in open(path)]
    gcode = gcoder.LightGCode(gcode0)

    while not print_core.online:
        time.sleep(0.1)

    print_core.startprint(gcode)
    while print_core.printing == True:
        pass
    print_core.disconnect()

print('printer_communication/gcode/test.gcode')
print('printer_communication/gcode/test2.gcode')



# while(cap.isOpened()):






# while(cap.isOpened()): # check camera status
#     send_gcode("printer_communication/layerwise_gcode_file/layer_{}.gcode".format(0))
#     for layer in range(total_layer):
#         gcode_path = "printer_communication/layerwise_gcode_file/layer_{}.gcode".format(layer)
#         send_gcode(gcode_path)
#         ret_flag,Vshow = cap.read()
#         img_path = 'printer_communication/elp_test/layer_{}.jpg'.format(layer)
#         # save image
#         cv2.imwrite(img_path,Vshow)
#         cor_gcode_dir = "printer_communication/iron_layer_gcode_file/"
#         output_path = cor_gcode_dir + "layer_{}_cor.gcode".format(layer)
#         coord_list = get_defect_positions(img_path, gcode_path, layer, type=2)
#         coord_list=[element for sublist in coord_list for element in sublist]
#         if len(coord_list) < 300:
#             pass
#         else:
#             generate_iron_layer(gcode_path, layer, output_path)
#             send_gcode(output_path)
#     break
# cap.release() # release storage

# for testing
# layer = 1
# layer_gcode_path = "printer_communication/layerwise_gcode_file/layer_{}.gcode".format(layer)
# send_gcode("printer_communication/layerwise_gcode_file/layer_{}.gcode".format(0))
# send_gcode("printer_communication/layerwise_gcode_file/layer_{}.gcode".format(layer))
# # take picture
# img_path = 'printer_communication/elp_test/layer_{}.jpg'.format(layer)
# cor_gcode_dir = "printer_communication/iron_layer_gcode_file/"
# output_path = cor_gcode_dir + "layer_{}_cor.gcode".format(layer)
# coord_list = get_defect_positions(img_path, gcode_path, layer, type=2)
# coord_list=[element for sublist in coord_list for element in sublist]
# if len(coord_list) < 300:
#     pass
# else:
#     generate_iron_layer(layer_gcode_path, layer, output_path)
#     send_gcode(output_path)
