import cv2
from projection_elp import get_defect_positions
from gcode_ironing import generate_iron_layer
from camera_control import take_pic
from printrun.printcore import printcore
from printrun import gcoder
import time

gcode_path = 'printer_communication/gcode/SmallBellow_newwoutTri.gcode'
layer_gcode_dir = 'printer_communication/layerwise_gcode_file/'
cor_gcode_dir = 'printer_communication/iron_layer_gcode_file/'
img_dir_path = 'printer_communication/elp_test/'
total_layer = 239
defect_threshold = 100

# send gcode to printer
def print_gcode(path):
    print_core = printcore('COM3', 115200)
    gcode0 = [i.strip() for i in open(path)]
    gcode = gcoder.LightGCode(gcode0)

    while not print_core.online:
        time.sleep(0.1)

    print_core.startprint(gcode)
    while print_core.printing == True:
        pass
    print_core.disconnect()

print_gcode(layer_gcode_dir + "layer_0.gcode")
# print('printer_communication/gcode/test.gcode')
# print('printer_communication/gcode/test2.gcode')


for i in range(1, total_layer):
    layer_gcode = layer_gcode_dir + "layer_{}.gcode".format(i)
    print_gcode(layer_gcode)
    img_path = img_dir_path + 'layer_{}.jpg'.format(i)
    take_pic(img_dir_path, i)
    coord_list = get_defect_positions(img_path, gcode_path, i, type=2)
    coord_list=[element for sublist in coord_list for element in sublist]
    if len(coord_list) < defect_threshold:
        pass
    else:
        print("fixing")
        output_path = cor_gcode_dir + "layer_{}_cor.gcode".format(i)
        generate_iron_layer(layer_gcode, output_path)
        print_gcode(output_path)







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
