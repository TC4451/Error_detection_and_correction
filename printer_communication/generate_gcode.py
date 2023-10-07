import numpy as np



LINE_WIDTH = 0.4
FILAMENT_DIAMETER = 1.85

def path_to_gcode(path):
    gcode = []
    # set Z if exist
    if path.shape[1] == 3:
        gcode.append(f"G1 Z{path[0,2]}")
    gcode.append(f"G1 X{path[0,0]} Y{path[0,1]}")
    for ii in range(path.shape[0]-1):
        start = path[ii]
        end = path[ii+1]
        e_length = get_E(start, end)

        gcode_line = f"G1 X{end[0]} Y{end[1]} E"
        gcode.append(gcode_line)

    return gcode


def get_E(start, end, line_width=LINE_WIDTH):
    dist = np.linalg.norm(start - end)
    # assume both are circles
    e_length = dist * line_width**2 / FILAMENT_DIAMETER**2

    return e_length