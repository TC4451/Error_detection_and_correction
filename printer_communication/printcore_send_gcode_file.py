from printrun.printcore import printcore
from printrun import gcoder
import time
import sys
import json

print_core = printcore('COM3', 115200)
# gcode = [i.strip() for i in open('C:/Users/zdai2/Desktop/Vision_Based_3D_Printing/Error_detection_using_webcam/printer_communication/gcode/SmallBellow_0.4n_0.3mm_FLEX_MK3S_move.gcode')] # or pass in your own array of gcode lines instead of reading from a file
json_string = sys.argv[1]
received_list = json.loads(json_string)
# print("Received list:", received_list)
# print(sys.argv[1])


gcode = gcoder.LightGCode(received_list)

# startprint silently exits if not connected yet
while not print_core.online:
  time.sleep(0.1)
  # sys.exit()

print_core.startprint(gcode) # this will start a print

command = input()
while command != 'quit':
  command = input()

print_core.disconnect()
sys.exit()