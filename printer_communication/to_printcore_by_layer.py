import sys
import json

def send_gcode(file_path):
    gcode = [i.strip() for i in open(file_path)]

    # Convert the list to a JSON string
    list_as_json = json.dumps(gcode)

    # Pass the JSON string as a command-line argument
    sys.argv.append(list_as_json)

    # Execute the second script
    exec(open('printer_communication/printcore_send_gcode_file.py').read())

    sys.exit()

# send_gcode('printer_communication/gcode/test.gcode')


# 'printer_communication/correction_gcode_file/layer_1_cor.gcode'
# os.system(f"c:/Users/zdai2/AppData/Local/anaconda3/envs/cv/python.exe printcore_command_line.py")
