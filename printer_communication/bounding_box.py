import cv2
import numpy as np
import matplotlib.pyplot as plt

from tsp import *


def transform(points, x, y, theta):
    rad = np.deg2rad(theta)
    R = np.array([[np.cos(rad), -np.sin(rad), x],
                  [np.sin(rad), np.cos(rad), y],
                  [0,0,1]])
    trans_points = np.hstack((points, np.ones((points.shape[0],1)))).T
    trans_points = np.dot(R, trans_points)
    result = trans_points[:2, :].T
    # print(result)
    return result






# img = cv2.imread('bound_2.png')
img = cv2.imread('printer_communication/Laplacian.png')
img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
element_3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
dst_0 = cv2.dilate(img1, element_3)
dst_0 = cv2.erode(dst_0, element_3)
dst_0 = cv2.erode(dst_0, element_3)
dst = cv2.dilate(dst_0, element)
# cv2.imshow("before", img1)
# cv2.waitKey(0)
# cv2.imshow("erode", dst_0)
# cv2.waitKey(0)
# cv2.imshow("dilate", dst)
# cv2.waitKey(0)



ret,thresh = cv2.threshold(dst,127,255,cv2.THRESH_BINARY)
contours,_ = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


print("Number of contours detected:", len(contours))
# print(contours)
# cnt = contours[0]

fix_box_points = np.zeros((0,2))
fix_box_vertex = np.zeros((0,4))

for cnt in contours:
    # # compute straight bounding rectangle
    # x,y,w,h = cv2.boundingRect(cnt)
    # img = cv2.drawContours(img,[cnt],0,(255,255,0),2)
    # img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    # compute rotated rectangle (minimum area)
    rect = cv2.minAreaRect(cnt)
    pos, wh, theta = rect
    x,y = pos
    w,h = wh
    fix_box_points = np.vstack((fix_box_points, np.array((x,y))))

    # plot Oriented bounding box
    # print("rect", rect)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    # print("rotated box\t", box)
    # draw minimum area rectangle (rotated rectangle)
    img = cv2.drawContours(img,[box],0,(0,255,255),2)


    # make longer edge width, theta is angle from horizontal to width
    if h > w:
        h,w = wh
        theta += 90

    # printing line width in pixels (camera frame)
    LINE_WIDTH = 5.5

    num = int (h // LINE_WIDTH) + 1
    
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
    # print(path)
    # plt.plot(path[:,0], path[:,1])
    # plt.axis("equal")
    # plt.show()

    path_trans = transform(path, x,y,theta)
    # plt.plot(path_trans[:,0], path_trans[:,1])
    # plt.axis("equal")
    # plt.show()
    path_trans_plot = np.floor(path_trans).astype(int)

    color = (0, 0, 255)  # Red color (BGR format)
    thickness = 2  # Line thickness
    for jj in range(path_trans_plot.shape[0]-1):
        # print(path_trans[jj])
        img = cv2.line(img, path_trans_plot[jj], path_trans_plot[jj+1], color, thickness)

    this_vertex = np.hstack((path_trans[0], path_trans[-1]))
    fix_box_vertex = np.vstack((fix_box_vertex, this_vertex))








cv2.imshow("Original", cv2.imread('printer_communication/Laplacian.png'))
cv2.waitKey(0)
cv2.imshow("Sliced", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("fix_box_points", fix_box_points)
# connect_mat = point_to_graph(fix_box_points)
print("fix_box_vertex", fix_box_vertex)
connect_mat = vertex_to_graph(fix_box_vertex)
fix_box_path_idx = tsp_greedy(connect_mat)
# fix_box_path_idx = travellingSalesmanProblem(connect_mat)
print(fix_box_path_idx)

fix_box_points_plot = np.floor(fix_box_points).astype(int)
fix_box_vertex_plot = np.floor(fix_box_vertex).astype(int)


for ii in range(len(fix_box_path_idx)-1):
    idx = fix_box_path_idx[ii]
    next_idx = fix_box_path_idx[ii+1]
    # img = cv2.line(img, fix_box_points_plot[idx], fix_box_points_plot[next_idx], color, thickness)
    img = cv2.line(img, fix_box_vertex_plot[idx,2:], fix_box_vertex_plot[next_idx,:2], color, thickness)


cv2.imshow("Path", img)
cv2.waitKey(0)

