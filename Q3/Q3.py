import cv2
import numpy as np


# Z = baseline * f / (d + doffs)
baseline = 342.789 # mm //from ppt
focalLength = 4019.284 # pixel //from ppt
doffs = 279.184 # pixel //from ppt

class Question3:
    def __init__(self):
        pass

    def stereoDisparityMap(self, ImLPath, ImRPath):
        self.ImLPath = ImLPath
        self.ImRPath = ImRPath


        imgGrayL = cv2.imread(self.ImLPath, 0)  # read image in grayscale
        imgGrayR = cv2.imread(self.ImRPath, 0)  # read image in grayscale

        stereo = cv2.StereoBM_create(numDisparities=256, blockSize=25)  # from ppt
        self.imgDisparity = cv2.normalize(stereo.compute(imgGrayL, imgGrayR), None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)  #Disparity

        imgL = cv2.imread(self.ImLPath)

        cv2.namedWindow('imgL', cv2.WINDOW_NORMAL)
        cv2.resizeWindow("imgL", int(imgL.shape[1] / 4), int(imgL.shape[0] / 4))    # resize window to 1/16
        cv2.setMouseCallback('imgL', self.drawDot)
        cv2.imshow('imgL', imgL)
        
        cv2.namedWindow('disparity', cv2.WINDOW_NORMAL)
        cv2.resizeWindow("disparity", int(self.imgDisparity.shape[1] / 4), int(self.imgDisparity.shape[0] / 4))   # # resize window to 1/16
        cv2.imshow('disparity', self.imgDisparity)
        cv2.waitKey(0)

        cv2.destroyAllWindows()


    def drawDot(self, event, mouseX, mouseY, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
        
            img = cv2.cvtColor(np.copy(self.imgDisparity), cv2.COLOR_GRAY2BGR) # change to RGB for x - z
            # imgDot = cv2.cvtColor(np.copy(self.imgDisparity), cv2.COLOR_GRAY2BGR)  # change to RGB
            # cv2.circle(imgDot, (mouseX, mouseY), radius=25, color=(255, 255, 255), thickness=-1)  # draw a black dot for test

            # depth = baseline * focalLength / (img[mouseY][mouseX][0] + doffs)
            # print(mouseX, mouseY)

            imgRDot = cv2.imread(self.ImRPath)
            disparity = img[mouseY][mouseX][0]
            
            # ignore the position with 0 disparity (don't draw a dot)
            if disparity != 0:
                cv2.circle(imgRDot, (mouseX - disparity, mouseY), radius=25, color=(0, 255, 0), thickness=-1) # draw a green dot on the right image at accurate position
            
            cv2.namedWindow('imgR_dot', cv2.WINDOW_NORMAL)
            cv2.resizeWindow("imgR_dot", int(imgRDot.shape[1] / 4), int(imgRDot.shape[0] / 4))    # resize window to 1/16
            cv2.imshow('imgR_dot', imgRDot)
            cv2.waitKey(0)