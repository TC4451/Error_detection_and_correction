from printrun.printcore import printcore
from printrun import gcoder
import time


class GcodeSender:
    def __init__(self, port = '/dev/tty.usbmodem14201'):
        self.print_core = printcore(port, 115200)

    def disconnect(self):
        self.print_core.disconnect()

    def send_gcode(self, gcode_path):
        gcode0 = [i.strip() for i in open(gcode_path)]
        gcode = gcoder.LightGCode(gcode0)

        while not self.print_core.online:
            time.sleep(0.1)

        self.print_core.startprint(gcode)
        while (self.print_core.printing == True) or (not self.print_core.priqueue.empty()):
        # while (self.print_core.printing == True) or (self.print_core.send_thread != None):
        # while self.print_core.printing == True:
            time.sleep(0.1)
        # print("layer done")


        

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

