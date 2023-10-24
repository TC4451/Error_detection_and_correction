# 0: Prep, 1: bellow, 2: triangle
state = 0

def parse_layer(gcode_file, bellow_dir, triangle_dir):
    all_lines = []
    temp_list = []
    line_dict = {}
    layer_num = 1

    # read in all lines
    with open(gcode_file, "r") as f: 
        all_lines = f.readlines()

    # get the preset layer
    for line in all_lines:
        line = line.strip()
        temp_list.append(line)
        all_lines = all_lines[1:]
        if "M107" in line:       
            line_dict[0] = temp_list
            file_name = bellow_dir + "layer_0.gcode"
            file = open(file_name, "w")
            for l in temp_list:
                file.write(l + "\n")
            temp_list = []
            break

    # remove all empty lines
    l = list(map(lambda x: x.replace('\n', ''), all_lines))
    all_lines = list(filter(None, l))

    all_lines = iter(all_lines)
    for line in all_lines:
        if line.strip():
            line = line.strip()
            temp_list.append(line)
            if "; stop printing object SmallBellow" in line:
                file_name = bellow_dir + "layer_{}.gcode".format(layer_num)
                file = open(file_name, "w")
                for l in temp_list:
                    file.write(l + "\n")
                temp_list = []
            elif "; stop printing object wiping_pattern_z" in line:
                file_name = triangle_dir + "layer_{}.gcode".format(layer_num)
                file = open(file_name, "w")
                for l in temp_list:
                    file.write(l + "\n")
                temp_list = []
                layer_num += 1

    # write the last layer
    file_name = bellow_dir + "end.gcode"
    file = open(file_name, "w")
    for l in temp_list:
        file.write(l + "\n")

# gcode_file = "printer_communication/gcode/SmallBellow_Zwiping_Oct23.gcode"
# bellow_dir = "printer_communication/bellow_layer_gcode_file/"
# tri_dir = "printer_communication/triangle_layer_gcode_file/"

# parse_layer(gcode_file, bellow_dir, tri_dir)