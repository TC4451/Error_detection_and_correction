def parse_layer(gcode_file):
    lines = []
    layer_num = 0
    file_dir = "printer_communication/layerwise_gcode_file/"
    for line in open(gcode_file):
        line = line.strip()
        lines.append(line)
        if ";Z:" in line or "; Filament-specific end gcode" in line:       
            # layer_height = float(line.strip().split(':')[1])
            # file_name = file_dir + "layer_" + str(layer_num) + "_" + str(layer_height) + ".gcode"
            file_name = file_dir + "layer_{}.gcode".format(layer_num)
            layer_num += 1
            file = open(file_name, "w")
            for line in lines:
                file.write(line + "\n")
            lines = []
            if "; Filament-specific end gcode" in line:
                break


parse_layer('printer_communication/gcode/SmallBellow_Oct8_Tri_move.gcode')