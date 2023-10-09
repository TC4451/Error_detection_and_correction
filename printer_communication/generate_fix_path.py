import cv2
import numpy as np
import matplotlib.pyplot as plt
from defect_detection import DefectDetection

# printing line width in pixels (camera frame)
LINE_WIDTH = 5.5
MAX = np.iinfo(np.int32).max

def transform(points, x, y, rad):
    # rad = np.deg2rad(theta)
    R = np.array([[np.cos(rad), -np.sin(rad), x],
                  [np.sin(rad), np.cos(rad), y],
                  [0,0,1]])
    trans_points = np.hstack((points, np.ones((points.shape[0],1)))).T
    trans_points = np.dot(R, trans_points)
    result = trans_points[:2, :].T
    # print(result)
    return result

def get_oriented_bounding_box(img_path, erode=3, dilate=15, plot=False):
    '''
        input result of error detection
        which is a image of black background with error show as small white area

        return a list of oriented rectangles as nx5 np.array
            [x,y,w,h,theta]
            w is always the longer edge
            theta is angle of width with horizontal
    '''

    img = cv2.imread(img_path)
    img_binary = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # erode and dilate to form pixel blob for detection
    element_dilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate, dilate))
    element_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (erode, erode))
    dst_temp = cv2.dilate(img_binary, element_erode)
    dst_temp = cv2.erode(dst_temp, element_erode)
    dst_temp = cv2.erode(dst_temp, element_erode)
    dst = cv2.dilate(dst_temp, element_dilate)
    # get contour
    ret,thresh = cv2.threshold(dst,127,255,cv2.THRESH_BINARY)
    contours,_ = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print("Number of contours detected:", len(contours))

    box_list = np.zeros((0,5))
    for cnt in contours:
        
        rect = cv2.minAreaRect(cnt)
        pos, wh, theta = rect
        x,y = pos
        w,h = wh
        # force width to be longer than height
        if h > w:
            h,w = wh
            theta += 90
        
        theta = np.deg2rad(theta)

        box_list = np.vstack((box_list, np.array((x,y,w,h,theta))))

    if plot is True:
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            # print("rotated box\t", box)
            # draw minimum area rectangle (rotated rectangle)
            img = cv2.drawContours(img,[box],0,(0,255,255),2)

        cv2.imshow("bounding box", img)
        cv2.waitKey(0)

    return box_list



def slice_boxes(box_list, line_width=LINE_WIDTH, plot_img=None):
    
    fix_box_vertex = np.zeros((0,4))
    fix_box_coverage_list = []

    for box in box_list:
        x,y,w,h,theta = box

        num = int (h // line_width) + 1

        # zig-zag coverage path
        path = [(-w/2, -h/2)]
        for ii in range(num*2+1):
            last_point = path[-1]
            if ii%4 == 0:
                next_point = (last_point[0]+w, last_point[1])
            elif ii%4 == 1:
                next_point = (last_point[0], last_point[1]+LINE_WIDTH)
            elif ii%4 == 2:
                next_point = (last_point[0]-w, last_point[1])
            elif ii%4 == 3:
                next_point = (last_point[0], last_point[1]+LINE_WIDTH)
            path.append(next_point)

        path = np.array(path)

        path_trans = transform(path, x,y,theta)
        fix_box_coverage_list.append(path_trans)

        box_ends = np.hstack((path_trans[0], path_trans[-1]))
        fix_box_vertex = np.vstack((fix_box_vertex, box_ends))

        if plot_img is not None:
            path_trans_plot = np.floor(path_trans).astype(int)
            color = (0, 0, 255)  # Red color (BGR format)
            thickness = 2  # Line thickness
            for jj in range(path_trans_plot.shape[0]-1):
                # print(path_trans[jj])
                plot_img = cv2.line(plot_img, path_trans_plot[jj], path_trans_plot[jj+1], color, thickness)
            cv2.imshow("Path", plot_img)
            cv2.waitKey(0)

    connect_mat = vertex_to_graph(fix_box_vertex)
    fix_box_path_idx = tsp_greedy(connect_mat)

    final_fix_path = np.zeros((0,2))
    # for idx in range(len(fix_box_path_idx)-1):
        # if idx != 0:
        #     last_path_end = fix_box_vertex[idx-1, 2:]
        #     this_path_start = fix_box_vertex[idx, :2]
        #     final_fix_path = np.vstack((final_fix_path, ))

    for idx in fix_box_path_idx:
        final_fix_path = np.vstack((final_fix_path, fix_box_coverage_list[idx]))

    # print(final_fix_path)

    if plot_img is not None:
        path_trans_plot = np.floor(final_fix_path).astype(int)
        color = (0, 0, 255)  # Red color (BGR format)
        thickness = 2  # Line thickness
        for jj in range(path_trans_plot.shape[0]-1):
            # print(path_trans[jj])
            plot_img = cv2.line(plot_img, path_trans_plot[jj], path_trans_plot[jj+1], color, thickness)
        cv2.imshow("Path", plot_img)
        cv2.waitKey(0)


    return final_fix_path

def vertex_to_graph(vertex):
    # from row to column
    connection_matrix = np.zeros((vertex.shape[0], vertex.shape[0]))
    for ii in range(vertex.shape[0]):
        for jj in range(vertex.shape[0]):
            dist = np.linalg.norm(vertex[ii,2:] - vertex[jj,:2])
            connection_matrix[ii, jj] = dist
    # print(connection_matrix)
    return connection_matrix

def tsp_greedy(dist):
    num_cities = len(dist)
    path = [0]  # Start at city 0
    visited = set([0])
    current_city = 0
    dist[:,0] = MAX

    while len(visited) < num_cities:
        nearest_city = np.argmin(
            [dist[current_city][i] 
                for i in range(num_cities)])
        # print([dist[current_city][i] 
        #         for i in range(num_cities)])

        path.append(nearest_city)
        visited.add(nearest_city)
        current_city = nearest_city
        dist[:,nearest_city] = MAX
        # print(visited)
    
    # path.append(0)  # Return to starting city
    # print(path)
    return path


if __name__ == '__main__':
    # img_path = "Laplacian.png"
    # box_list = get_oriented_bounding_box(img_path, plot=True)
    # slice_boxes(box_list, line_width=LINE_WIDTH, plot_img=cv2.imread(img_path))
    img_folder_path = "printer_communication/images/elp_test1003/"
    gcode_path = 'printer_communication/gcode/SmallBellow_newwoutTri.gcode'
    img_taken_position = [148, 150]
    layer_height = 0.1
    defect_detector = DefectDetection(gcode_path, img_folder_path, img_taken_position, layer_height)

    imgID = 8
    layerID = imgID
    print("image ID: {}".format(imgID))
    img_path = img_folder_path + "layer_{}.jpg".format(imgID)
    img = cv2.imread(img_path)
    positions = defect_detector.get_defect_positions(img, layerID)
    # print(positions)

    defect_img_path = img_folder_path + "layer_{}_defect.jpg".format(imgID)
    box_list = get_oriented_bounding_box(defect_img_path)
    # final_fix_path = slice_boxes(box_list, line_width=LINE_WIDTH)
    final_fix_path = slice_boxes(box_list, line_width=LINE_WIDTH, plot_img=cv2.imread(defect_img_path))

    final_gcode_pos = defect_detector.get_Gcode_positions(final_fix_path)
    # print(final_gcode_pos)

