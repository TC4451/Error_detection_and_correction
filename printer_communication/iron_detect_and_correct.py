import cv2
from defect_detection import DefectDetection
from gcode_ironing import generate_iron_layer
from camera_control import CameraControl
# from layer_parsing import parse_layer
from layer_parsing_triTip import parse_layer_tip
from gcode_nozzle_move_config import add_nozzle_movement
from gcode_sender import GcodeSender
from printrun.printcore import printcore
from printrun import gcoder
import time

gcode_path = 'printer_communication/gcode/SmallBellow_withTri_Oct14_0.2mm.gcode'
move_gcode_path = 'printer_communication/gcode/SmallBellow_withTri_Oct14_0.2mm_move.gcode'
gcode_noTri_path = 'printer_communication/gcode/SmallBellow_withTri_Oct14_0.2mm_noTri.gcode'
img_dir_path = 'printer_communication/images/elp_test_1014/'
move_X = 176.8
move_Y = 148.2
total_layer = 144
defect_threshold = 5
img_taken_position = [move_X, move_Y]
layer_height = 0.2
delay_time = 5

# layer_gcode_dir = 'printer_communication/layerwise_gcode_file/'
layer_gcode_dir = 'printer_communication/test_parsing/'
cor_gcode_dir = 'printer_communication/iron_layer_gcode_file/'

# send gcode to printer
# def print_gcode(path):
#     print_core = printcore('COM3', 115200)
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
# parse_layer(move_gcode_path, layer_gcode_dir)
parse_layer_tip(move_gcode_path, layer_gcode_dir)
print("Layers parsed")

camera = CameraControl(1)
gcode_sender = GcodeSender("COM3")
print("Camera opened")
gcode_sender.send_gcode(layer_gcode_dir + "layer_0.gcode")

defect_detector = DefectDetection(gcode_noTri_path, img_dir_path, img_taken_position, layer_height)


for i in range(1, total_layer+1):
    layer_gcode = layer_gcode_dir + "layer_{}.gcode".format(i)
    gcode_sender.send_gcode(layer_gcode)
    time.sleep(delay_time)
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
gcode_sender.send_gcode(layer_gcode_dir + "layer_146.gcode")
