import cv2

def take_pic(img_dir_path, layerID):
    cap = cv2.VideoCapture(1)
    while(cap.isOpened()): # check camera status
        ret_flag,Vshow = cap.read() # get img
        cv2.imwrite(img_dir_path + "layer_{}.jpg".format(layerID),Vshow) #route
        print("success to save layer_{}.jpg".format(layerID))
        break

    cap.release() # release storage
    # cv2.destroyAllWindows()

take_pic('printer_communication/elp_test/', 'test')
