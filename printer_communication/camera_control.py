import cv2

# def take_pic(img_dir_path, layerID):
#     cap = cv2.VideoCapture(1)
#     # while(cap.isOpened()): # check camera status
#     ret_flag,Vshow = cap.read() # get img
#     cv2.imwrite(img_dir_path + "layer_{}.jpg".format(layerID),Vshow) #route
#     print("success to save layer_{}.jpg".format(layerID))

#     cap.release() # release storage
    # cv2.destroyAllWindows()

# take_pic('printer_communication/elp_test/', 'test')

class CameraControl:
    def __init__(self, camera_id = 0, resolution = (1920, 1080)):
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    def take_pic(self, img_dir_path, layerID):
        while(not self.cap.isOpened()): # check camera status
            pass

        ret_flag, Vshow = self.cap.read() # get img
        cv2.imwrite(img_dir_path + "layer_{}.jpg".format(layerID),Vshow) #route
        print("success to save layer_{}.jpg".format(layerID))

    def set_resolution(self, resolution):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    def turn_off_cam(self):
        self.cap.release()
