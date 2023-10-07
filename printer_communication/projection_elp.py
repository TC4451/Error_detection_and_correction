import cv2 as cv
import numpy as np
from gcode_layer_visualization import get_layer_coordinates
import copy
import matplotlib.pyplot as plt
np.set_printoptions(suppress=True)

def get_defect_positions(img_path, gcode_path, layerID, type = 1):
    # type 1: centroid
    # type 2: all points
    nozzle_pos = [168, 165, 0.3 * layerID - 0.1]
    T_printer_nozzle = np.array([
        [1, 0, 0, -nozzle_pos[0]],
        [0, 1, 0, -nozzle_pos[1]],
        [0, 0, 1, -nozzle_pos[2]],
        [0, 0, 0, 1]
    ])
    T_nozzle_cam = np.array([
    [  0.99992787,   0.00990087,  -0.00679966,  51.2],
    [  0.00991064,  -0.9999499,    0.00140497, -50.5],
    [ -0.00678541,  -0.00147225,  -0.9999759,  101],
    [  0.,           0.,           0.,           1.        ]
    ]) 
    camera_matrix = np.array(
        [[2213.44472103,   0.,         955.10214021], 
        [0.,         2224.30381979, 527.46399473], 
        [0., 0., 1.]])
    dist_coeffs = np.array([[-0.29758743, -0.37224022, -0.00058477, -0.00031724,  2.23050257]])

    T_printer_cam = np.matmul(T_nozzle_cam, T_printer_nozzle)
    # print("T_printer_cam: \n", T_printer_cam)
    tvec = T_printer_cam[:3, 3].reshape((3, 1))
    rvec, _ = cv.Rodrigues(T_printer_cam[:3, :3])

    x, y, z = get_layer_coordinates(gcode_path, layerID, 2)
    num_contour = len(x)
    all_contours = []
    for contour_id in range(num_contour):
        size_contour = len(x[contour_id])
        contour_points = np.zeros((size_contour, 3), np.float32)
        contour_points[:, 0] = np.array(x[contour_id])
        contour_points[:, 1] = np.array(y[contour_id])
        contour_points[:, 2] = z
        all_contours.append(contour_points)

    img = cv.imread(img_path)
    img = cv.resize(img, (1920, 1080))
    height, width = img.shape[:2]
    color = (255, 255, 255)

    contour_id = 0
    masks = []

    isClosed = True
    contour_color = (0, 0, 255)
    thickness = 2
    for contour_points in all_contours:
        img_points, _ = cv.projectPoints(contour_points, rvec, tvec, camera_matrix, dist_coeffs)
        img_points.reshape(-1, 1, 2)
        mask = np.zeros((height, width), dtype=np.uint8)

        # img = cv.polylines(img, [img_points.astype(np.int32)],isClosed, contour_color, thickness)
        cv.drawContours(mask, [img_points.astype(np.int32)], 0, color, thickness=cv.FILLED)
        masks.append(mask)

    # xor all masks
    final_mask = np.zeros((height, width), dtype=np.uint8)
    for mask in masks:
        final_mask = cv.bitwise_xor(final_mask, mask)

    # crop out valid part
    dst = cv.bitwise_and(img, img, mask=final_mask)

    # make background white
    dst[np.where(np.all(dst[..., :3] == 0, -1))] = 0
    # split channels
    r,g,b = cv.split(dst)

    # Normalize each channel independently
    norm_r = cv.normalize(r, None, 0, 255, cv.NORM_MINMAX)
    norm_g = cv.normalize(g, None, 0, 255, cv.NORM_MINMAX)
    norm_b = cv.normalize(b, None, 0, 255, cv.NORM_MINMAX)

    # merge and use mask as alpha channel
    dst_transparent = cv.merge([norm_r, norm_g, norm_b,final_mask], 4)
    # plt.imshow(dst_transparent), plt.axis('off')
    # plt.show()

    # Image pre processing
    img_RGB = cv.cvtColor(dst_transparent, cv.COLOR_BGR2RGB)
    grayImage = cv.cvtColor(dst_transparent, cv.COLOR_BGR2GRAY)

    gaussianBlur = cv.GaussianBlur(grayImage, (5, 5), 0)
    ret, binary = cv.threshold(gaussianBlur, 130, 255, cv.THRESH_BINARY)

    dst_lap = cv.Laplacian(binary, cv.CV_16S, ksize = 3)
    Laplacian = cv.convertScaleAbs(dst_lap)

    def image_pixel_to_Gcode_position(defect_coord, img_shape = (1080, 1920)):
        img_center_pos = copy.copy(nozzle_pos) # in printer frame
        img_center_pos[0] -= T_nozzle_cam[0, 3]
        img_center_pos[1] += T_nozzle_cam[1, 3]

        (h, w) = img_shape
        undistort_camera_matrix, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w,h), 1, (w,h))

        fx = undistort_camera_matrix[0, 0]
        fy = undistort_camera_matrix[1, 1]
        f = (fx + fy) / 2
        cx = undistort_camera_matrix[0, 2]
        cy = undistort_camera_matrix[1, 2]
        depth = T_nozzle_cam[2, 3]

        dx = defect_coord[0] - cx
        dy = defect_coord[1] - cy

        dX_printer = depth / f * dx
        dY_printer = -depth / f * dy
        defect_pos = copy.copy(img_center_pos) + np.array([dX_printer, dY_printer, 0])

        return defect_pos

    def get_Gcode_positions(defect_coords):
        all_positions = []
        for coord in defect_coords:
            all_positions.append(image_pixel_to_Gcode_position(coord))
        return all_positions

    def defect_mask_to_positions(defect_mask, type):
        # type 1: centroid
        # type 2: all points

        analysis = cv.connectedComponentsWithStats(defect_mask, 8, cv.CV_32S)
        (totalLabels, label_ids, values, centroid) = analysis

        if type == 1:
            return get_Gcode_positions(centroid[1:])
        elif type == 2:
            defect_positions = []
            for i in range(1, totalLabels):
                pixels = np.argwhere(label_ids == i)
                pixels = pixels[:, ::-1]
                defect_positions.append(get_Gcode_positions(pixels))
            return defect_positions

    return defect_mask_to_positions(Laplacian, 2)

# img_folder_path = "printer_communication/elp_test/"
# imgID = 1
# print("image ID: {}".format(imgID))
# img_path = img_folder_path + "layer_{}.jpeg".format(imgID)
# gcode_path = 'printer_communication/gcode/SmallBellow_woutTri.gcode'
# layerID = imgID
# # positions = get_defect_positions(img_path, gcode_path, layerID)

# # print(positions)
# coord_list = get_defect_positions('printer_communication\elp_test\layer_1.jpg', 'printer_communication/gcode/SmallBellow_newwoutTri.gcode', 1, type = 2)
# coord_list=[element for sublist in coord_list for element in sublist]
# print(len(coord_list))