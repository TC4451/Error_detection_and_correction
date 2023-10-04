import projection_elp

def generate_correction_gcode(img_path, gcode_path, layer_ID, output_path):
    coord_list = projection_elp.get_defect_positions(img_path, gcode_path, layer_ID)
    gcode_list = []
    e_vals = ['E.3449', 'E.04645']

    for i in range(len(coord_list)):
        shape = coord_list[i]
        # sets the acceleration for printing moves
        gcode_list.append('M204 S1000')
        # sets the feed rate to 1500
        # gcode_list.append('G1 E1 F1500')
        for j in range(len(shape)):
            x = round(shape[j][0], 3)
            y = round(shape[j][1], 3)
            gcode = "G1 X{} Y{} {}".format(x, y, e_vals[j%2])
            # print(gcode)
            gcode_list.append(gcode)
    
    # !!! change this
    gcode_list.append("G1 E-2.5 F3600")
    gcode_list.append("G1 X168 Y165")
        

    file = open(output_path, "w")
    for line in gcode_list:
        file.write(line + "\n")
    

# sample movement from the originl gcode
# M204 S1000
# G1 X112.564 Y104.558 F10800
# G1 E-2.5 F3600
# G1 X127.987 Y103.046 F10800
# G1 E2.5 F1500
# M204 S800
# G1 F448.08