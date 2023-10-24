def parse_layer_tip(gcode_file, file_dir, next_line_num):
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
        if ";Z:" in line:       
            line_dict[0] = temp_list
            file_name = file_dir + "layer_0.gcode"
            file = open(file_name, "w")
            for l in temp_list:
                file.write(l + "\n")
            temp_list = []
            break

    l = list(map(lambda x: x.replace('\n', ''), all_lines))
    all_lines = list(filter(None, l))

    deretract_line = "G1 E1."
    
    # write to file until the end gcode
    all_lines = iter(all_lines)
    for line in all_lines:
        if line.strip():           
            line = line.strip()
            temp_list.append(line)
            if "; printing object wiping_pattern_z" in line:
            # if "; printing object support_triangle" in line:
                # for i in range(next_line_num):
                #     next_line = all_lines.__next__()
                #     temp_list.append(next_line)
                file_name = file_dir + "layer_{}.gcode".format(layer_num)
                file = open(file_name, "w")
                for l in temp_list:
                    file.write(l + "\n")
                temp_list = []
                for i in range(next_line_num):
                    next_line = all_lines.__next__()
                    temp_list.append(next_line)
                temp_list.append(deretract_line + "\n")
                layer_num += 1
            elif "; Filament-specific end gcode" in line:
                file_name = file_dir + "layer_{}.gcode".format(layer_num)
                file = open(file_name, "w")
                for l in temp_list:
                    file.write(l + "\n")
                temp_list = []
                layer_num += 1
                break
    # write the last layer
    file_name = file_dir + "layer_{}.gcode".format(layer_num)
    file = open(file_name, "w")
    for l in temp_list:
        file.write(l + "\n")

# def parse_layer_tip(gcode_file, file_dir):
#     all_lines = []
#     temp_list = []
#     line_dict = {}
#     layer_num = 1

#     # read in all lines
#     with open(gcode_file, "r") as f: 
#         all_lines = f.readlines()

#     # get the preset layer
#     for line in all_lines:
#         line = line.strip()
#         temp_list.append(line)
#         all_lines = all_lines[1:]
#         if ";Z:" in line:       
#             line_dict[0] = temp_list
#             file_name = file_dir + "layer_0.gcode"
#             file = open(file_name, "w")
#             for l in temp_list:
#                 file.write(l + "\n")
#             temp_list = []
#             break

#     for i in range(len(all_lines)):
#         line = all_lines[i].strip()
#         temp_list.append(line)
#         if "; printing object support_triangle" in line or "; Filament-specific end gcode" in line:
#             next_line = all_lines[i+1]
#             temp_list.append(next_line)
#             file_name = file_dir + "layer_{}.gcode".format(layer_num)
#             file = open(file_name, "w")
#             for l in temp_list:
#                 file.write(l + "\n")
#             temp_list = []
#             layer_num += 1
        

# def parse_layer_tip(gcode_file, file_dir, Y_tip):
#     all_lines = []
#     temp_list = []
#     line_dict = {}
#     layer_num = 1

#     # read in all lines
#     with open(gcode_file, "r") as f: 
#         all_lines = f.readlines()

#     # get the preset layer
#     for line in all_lines:
#         line = line.strip()
#         temp_list.append(line)
#         all_lines = all_lines[1:]
#         if ";Z:" in line:       
#             line_dict[0] = temp_list
#             temp_list = []
#             break

#     first_half = []
#     second_half = []
#     for line in all_lines:
#         line_num = 0
#         line = line.strip()
#         temp_list.append(line)
#         all_lines = all_lines[1:]
#         if ";Z:" in line or "; Filament-specific end gcode" in line:
#             for ln in range(len(temp_list)):
#                 curl = temp_list[ln]
#                 if ' Y' in curl and curl.split(" ")[2][0] == 'Y' and abs(float(curl.split(" ")[2][1:]) - Y_tip) < 1:
#                     line_num = ln
#                     first_half = temp_list[:line_num]
#                     line_dict[layer_num] = second_half + first_half
#                     second_half = temp_list[line_num:]
#                     temp_list = []
#                     layer_num += 1
#                     break

#     for i in range(len(line_dict)):
#         file_name = file_dir + "layer_{}.gcode".format(i)
#         file = open(file_name, "w")
#         for line in line_dict[i]:
#             file.write(line + "\n")

# parse_layer_tip('printer_communication/gcode/SmallBellow_Nearest_Oct15.gcode', 'printer_communication/test_parsing/', 8)

            