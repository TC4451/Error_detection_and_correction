import cv2
from defect_detection import DefectDetection
from gcode_ironing import generate_iron_layer
from camera_control import CameraControl
from layer_parsing_separate import parse_layer
from gcode_nozzle_move_config_filewise import add_nozzle_movement
from gcode_sender import GcodeSender
from printrun.printcore import printcore
from printrun import gcoder
import time

gcode_path = 'printer_communication/gcode/SmallBellow_Zwiping_Oct24.gcode'
gcode_noTri_path = 'printer_communication/gcode/SmallBellow_manualSeam_Rear_extrusion1_1_Oct20_noTri.gcode'
img_dir_path = 'printer_communication/images/elp_1024_3_uf/'
log_dir_path = 'printer_communication/logs/'
log_file_name = '1024_wiping_pattern_z_unfix_3.txt'
parse_support_line = 1
move_X = 180
# move_X = 177.5
move_Y = 152
total_layer = 120
defect_threshold = 2
binary_threshold = 85
img_taken_position = [move_X, move_Y]
layer_height = 0.2
delay_time = 3
enable_correction = False
fixing_E_proportion = 0.2
fixing_S_proportion = 0.6

# layer_gcode_dir = 'printer_communication/layerwise_gcode_file/'
bellow_dir = "printer_communication/bellow_layer_gcode_file/"
tri_dir = "printer_communication/triangle_layer_gcode_file/"
cor_gcode_dir = 'printer_communication/iron_layer_gcode_file/'

with open(log_dir_path + log_file_name, 'a') as f:
    f.write("Gcode path: {}\n".format(gcode_path))
    f.write("Image folder path: {}\n".format(img_dir_path))
    f.write("Picture taking position: {}\n".format(img_taken_position))
    f.write("Total layer: {}\n".format(total_layer))
    f.write("Defect binary threshold: {}\n".format(binary_threshold))
    f.write("Defect number threshold: {}\n".format(defect_threshold))
    f.write("Layer height: {}\n".format(layer_height))
    f.write("Correction enabled: {}\n".format(enable_correction))
    f.write("Ironing layer extrusion ratio: {}\n".format(fixing_E_proportion))
    f.write("Ironing layer speed ratio: {}\n".format(fixing_S_proportion))
    f.write("---------------------------------------------------------\n")

# parse_layer(move_gcode_path, layer_gcode_dir)
parse_layer(gcode_path, bellow_dir, tri_dir)
print("Layers parsed")

add_nozzle_movement(bellow_dir, move_X, move_Y)
print("Movement modified")

camera = CameraControl(1)
print("Camera opened")

gcode_sender = GcodeSender("COM3")
print("Connected to printer")
gcode_sender.send_gcode(bellow_dir + "layer_0.gcode")
print("Start heating")

defect_detector = DefectDetection(gcode_noTri_path, img_dir_path, img_taken_position, layer_height)
fixed_layer_list = []

for i in range(1, total_layer+1):
    layer_gcode = bellow_dir + "layer_{}.gcode".format(i)
    gcode_sender.send_gcode(layer_gcode)
    print("finished printing layer {}".format(i))
    time.sleep(delay_time)
    print("start taking picture")
    img_path = img_dir_path + 'layer_{}.jpg'.format(i)
    camera.take_pic(img_dir_path, i)
    img = cv2.imread(img_path)
    coord_list = defect_detector.get_defect_positions(img, i, type=1, binary_threshold=binary_threshold)
    # coord_list=[element for sublist in coord_list for element in sublist]
    print("layer {} defect: {}".format(i, len(coord_list)))
    line = "layer {}, num of defect: {}".format(i, len(coord_list))
    # print the Z supplement
    z_gcode = tri_dir + "layer_{}.gcode".format(i)
    gcode_sender.send_gcode(z_gcode)

    if len(coord_list) < defect_threshold:
        with open(log_dir_path + log_file_name, 'a') as f:
            f.write(line + '\n')
    else:
        print("start fixing")
        fixed_layer_list.append(i)
        with open(log_dir_path + log_file_name, 'a') as f:
            f.write(line + ' FIXED\n')
        if enable_correction:
            output_path = cor_gcode_dir + "layer_{}_cor.gcode".format(i)
            generate_iron_layer(layer_gcode, output_path, 
                                E_proportion = fixing_E_proportion, 
                                S_proportion = fixing_S_proportion)
            gcode_sender.send_gcode(output_path)
            print("finished fixing layer {}".format(i))
            # print the Z supplement
            z_gcode = tri_dir + "layer_{}.gcode".format(i)
            gcode_sender.send_gcode(z_gcode)

gcode_sender.send_gcode(bellow_dir + "end.gcode")

with open(log_dir_path + log_file_name, 'a') as f:
    f.write("TOTAL NUM OF FIXED LAYER: {}\n".format(len(fixed_layer_list)))
    f.write("Fixed layer list: {}".format(fixed_layer_list))