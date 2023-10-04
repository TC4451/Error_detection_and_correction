def get_layer_coordinates(gcode_path, target_layer = 1, target_type = 2):
    import matplotlib.pyplot as plt
    # get the number of layers
    num_layer = 0
    # type of layer (1: Perimeter, 2: External Perimeter, 3: Overhang perimeter, 4: Internal infill, 5: Solid infill, 6: Top solid infill,
    # 7: Bridge infill, 8: Skirt/Brim, 9: Custom)
    layer_type = 0
    layer_number_list = []
    layer_type_list = []
    layer_code_list = []
    z_val_dict = {}

    # Gcode parsing linking each line to layer number and layer type
    with open(gcode_path, 'r') as f:
        for line in f.readlines():
            # ignore empty & comments line
            if line == '\n' or line.startswith(';'):
                pass     
            else:
                layer_number_list.append(num_layer)
                layer_type_list.append(layer_type)
                layer_code_list.append(line.strip())
            
            # set layer type and layer number with comments
            if line.strip() == ";LAYER_CHANGE":
                num_layer += 1
                layer_type = 0
            elif line.strip().startswith(";Z:"): 
                z_val_dict[num_layer] = float(line.strip()[3:])
            elif line.strip() == ";TYPE:Perimeter":
                layer_type = 1
            elif line.strip() == ";TYPE:External perimeter":
                layer_type = 2
            elif line.strip() == ";TYPE:Overhang perimeter":
                layer_type = 3
            elif line.strip() == ";TYPE:Internal infill":
                layer_type = 4
            elif line.strip() == ";TYPE:Solid infill":
                layer_type = 5
            elif line.strip() == ";TYPE:Top solid infill":
                layer_type = 6
            elif line.strip() == ";TYPE:Bridge infill":
                layer_type = 7
            elif line.strip() == ";TYPE:Skirt/Brim":
                layer_type = 8
            elif line.strip() == ";TYPE:Custom":
                layer_type = 9
            
    # Gcode parsing for plane coordinates
    X_external_perimeter = []
    Y_external_perimeter = []


    shape_list_X = []
    shape_list_Y = []
    z_val = 0

    for i in range(len(layer_number_list)):
        # break if layer is over
        if layer_number_list[i] > target_layer:
            break
        # if target layer and type is found
        if layer_number_list[i] == target_layer and layer_type_list[i] == target_type:
            z_val = z_val_dict.get(layer_number_list[i])
            line = layer_code_list[i]
            if line.split(" ")[-1][0] == 'E':
                # print(line)
                for ele in line.split(" "):
                    if ele[0] == "X":
                        X_external_perimeter.append(float(ele[1:]))
                    elif ele[0] == "Y":
                        Y_external_perimeter.append(float(ele[1:]))
            elif line.startswith("M"):
                pass
            elif line.split(" ")[1][0] == 'F':
                pass
            else:
                # print("here")
                if len(X_external_perimeter) != 0:
                    X_external_perimeter.append(X_external_perimeter[0])
                    Y_external_perimeter.append(Y_external_perimeter[0])
                shape_list_X.append(X_external_perimeter)
                shape_list_Y.append(Y_external_perimeter)
                X_external_perimeter = []
                Y_external_perimeter = []
    shape_list_X.append(X_external_perimeter)
    shape_list_Y.append(Y_external_perimeter)

    def remove_empty_lists(input_list):
        output_list = [sublist for sublist in input_list if sublist]
        return output_list

    shape_list_X = remove_empty_lists(shape_list_X)
    shape_list_Y = remove_empty_lists(shape_list_Y)

    # print(shape_list_X)
    # print(shape_list_Y)
    # print(z_val)

    # fig = plt.figure()
    # plt.subplot(111)
    # plt.axis("equal")

    # colors = {0: "red",
    #           1: "blue",
    #           2: "green",
    #           3: "purple",
    #           4: "black",
    #           5: "orange",
    #           6: "pink",
    #           7: "yellow"}

    # for i in range(len(shape_list_X)):
    #     cur_shape_X = shape_list_X[i]
    #     cur_shape_Y = shape_list_Y[i]
    #     for j in range(len(cur_shape_X)):
    #         plt.plot([cur_shape_X[j],cur_shape_X[j-1]],\
    #         [cur_shape_Y[j],cur_shape_Y[j-1]],color=colors[i%7],linewidth=2,alpha=0.3)
    #         plt.scatter(cur_shape_X[j],cur_shape_Y[j],marker='s',c=colors[i%7],s=8,alpha=0.3)

    # plt.show()
    return shape_list_X, shape_list_Y, z_val

# visualization
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# def flatten_extend(matrix):
#      flat_list = []
#      for row in matrix:
#          flat_list.extend(row)
    #  return flat_list

# !!!fix layer 43-46
# x, y, z = get_layer_coordinates('printer_communication/gcode/SmallBellow_woutTri.gcode', 43, 2)
# x = flatten_extend(x)
# y = flatten_extend(y)
# x = np.array(x)
# y = np.array(y)
# print(x.shape)
# print(y)

# fig = plt.figure()
# plt.xlim(90, 160)
# plt.ylim(90, 140)
# graph, = plt.plot([], [], '.', )

# Animate the coordinates in one layer one by one according to the sequence they are being printed
# def animate(i):
#     graph.set_data(x[:i+1], y[:i+1])
#     return graph

# ani = FuncAnimation(fig, animate, frames=190, interval=500)
# plt.show()


    
