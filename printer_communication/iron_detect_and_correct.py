import cv2
from defect_detection import DefectDetection
from gcode_ironing import generate_iron_layer
from camera_control import CameraControl
from layer_parsing import parse_layer
from gcode_nozzle_move_config import add_nozzle_movement
from gcode_sender import GcodeSender
from printrun.printcore import printcore
from printrun import gcoder
import time

gcode_path = 'printer_communication/gcode/SmallBellow_0.3mm_Oct12.gcode'
move_gcode_path = 'printer_communication/gcode/SmallBellow_0.3mm_Oct12_move.gcode'
gcode_noTri_path = 'printer_communication/gcode/SmallBellow_0.3mm_Oct12_noTri.gcode'
img_dir_path = 'printer_communication/images/elp_test_1012/'
move_X = 174
move_Y = 148
total_layer = 120
defect_threshold = 5

layer_gcode_dir = 'printer_communication/layerwise_gcode_file/'
cor_gcode_dir = 'printer_communication/iron_layer_gcode_file/'

# send gcode to printer
# def print_gcode(path):
#     print_core = printcore('/dev/tty.usbmodem14201', 115200)
#     # print_core = printcore('COM3', 115200)
#     gcode0 = [i.strip() for i in open(path)]
#     gcode = gcoder.LightGCode(gcode0)

#     while not print_core.online:
#         time.sleep(0.1)

#     print_core.startprint(gcode)
#     while print_core.printing == True:
#         time.sleep(1)
#     print("layer done")
#     print_core.disconnect()

add_nozzle_movement(gcode_path, move_gcode_path, move_X, move_Y)
print("Movement modified")
parse_layer(move_gcode_path)
print("Layers parsed")

camera = CameraControl(1)
print("Camera opened")
print_gcode(layer_gcode_dir + "layer_0.gcode")

img_taken_position = [173, 156]
layer_height = 0.1
defect_detector = DefectDetection(gcode_noTri_path, img_dir_path, img_taken_position, layer_height)


for i in range(1, total_layer+1):
    layer_gcode = layer_gcode_dir + "layer_{}.gcode".format(i)
    print_gcode(layer_gcode)
    time.sleep(12)
    print("start taking picture")
    img_path = img_dir_path + 'layer_{}.jpg'.format(i)
    camera.take_pic(img_dir_path, i)
    img = cv2.imread(img_path)
    coord_list = defect_detector.get_defect_positions(img, i, type=1)
    # coord_list=[element for sublist in coord_list for element in sublist]
    print(len(coord_list))
    if len(coord_list) < defect_threshold:
        pass
    else:
        print("fixing")
        # output_path = cor_gcode_dir + "layer_{}_cor.gcode".format(i)
        # generate_iron_layer(layer_gcode, output_path)
        # print_gcode(output_path)
print_gcode(layer_gcode_dir + "layer_{}.gcode".format(total_layer+1))







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
