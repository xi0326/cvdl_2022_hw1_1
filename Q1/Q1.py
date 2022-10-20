import cv2
import numpy as np
import glob

class Question1:

    ret = []
    dist = []
    rvecs = []
    tvecs = []
    mtx = []

    def __init__(self):
        # pattern_size = 11, 8
        self.w = 11
        self.h = 8

    def findCorner(self, dirName):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)  # termination criteria

        filePaths = sorted(glob.glob(dirName + '\\*.bmp'), key=len)  # get all file paths
        # print(filePaths)
        for filePath in filePaths:
            img = cv2.imread(filePath)

            retval, corners = cv2.findChessboardCorners(img, (self.w, self.h))

            if retval:
                corners = cv2.cornerSubPix(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), corners, (self.w, self.w), (-1, -1), criteria)
                img = cv2.drawChessboardCorners(img, (self.w, self.h), corners, retval)
                img = cv2.resize(img ,(1024, 1024)) # resize to 1024 * 1024 to show smaller
                cv2.imshow('1.1 Find corners', img)
                cv2.waitKey(500)

        cv2.destroyWindow('1.1 Find corners')


    def findIntrinsic(self, dirName):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)  # termination criteria
        global dist, mtx
        
        objPoint = np.zeros((self.w * self.h, 3), np.float32)   # initialise the matrix
        objPoint[:,:2] = np.mgrid[0:self.w, 0:self.h].T.reshape(-1, 2)

        filePaths = sorted(glob.glob(dirName + '\\*.bmp'), key=len)  # get all file paths
        # print(filePaths)
        for filePath in filePaths:
            imgGray = cv2.imread(filePath, 0)    # read image in grayscale

            retval, corners = cv2.findChessboardCorners(imgGray, (self.w, self.h))

            # arrays to store object points and image points from all the images
            objPoints = []  # 3d point in real world space
            imgPoints = []  # 2d points in image plane

            if retval:
                corners = cv2.cornerSubPix(imgGray, corners, (self.w, self.w), (-1, -1), criteria)
                objPoints.append(objPoint)
                imgPoints.append(corners)

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, imgGray.shape[::-1], None, None)

        print('Intrinsic:')
        print(mtx)

    def findExtrinsic(self, dirName, n):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)  # termination criteria

        objPoint = np.zeros((self.w * self.h, 3), np.float32)
        objPoint[:,:2] = np.mgrid[0:self.w, 0:self.h].T.reshape(-1, 2)

        imgGray = cv2.imread(dirName + '\\' + n + '.bmp', 0) # read image in grayscale

        retval, corners = cv2.findChessboardCorners(imgGray, (self.w, self.h))
        
        if retval:
            corners = cv2.cornerSubPix(imgGray, corners, (self.w, self.w), (-1, -1), criteria)
        
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([objPoint], [corners], imgGray.shape[::-1], None, None)  # only one point, so need put in a list

        rmtx, _ = cv2.Rodrigues(rvecs[0])
        extrinsic_matrix = np.zeros((3, 4)) # initialise the matrix
        
        # on ppt
        for x in range(3):
            for y in range(3):
                extrinsic_matrix[x, y] = rmtx[x, y]
                if y == 2:
                    extrinsic_matrix[x, y + 1] = tvecs[0][x]
        
        print('Extrinsic:')
        print(extrinsic_matrix)
        
    def findDistortion(self):
        global dist

        try: 
            dist    # obtained simultaneously with intrinsic parameters
        except NameError:   # intrinsic matrix is not found
            print('Please find intrinsic matrix first')
        else:
            print('Distortion:')
            print(dist)

    def showUndistortion(self, dirName):

        filePaths = sorted(glob.glob(dirName + '\\*.bmp'), key=len)  # get all file paths
        # print(filePaths)
        for filePath in filePaths:
            global mtx, dist

            imgGray = cv2.imread(filePath, 0)    # read image in grayscale
            imageHeight,  imageWidth = imgGray.shape[:2]   # image size

            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (imageWidth, imageHeight), 1, (imageWidth, imageHeight))
            undistort = cv2.resize(cv2.undistort(imgGray, mtx, dist, None, newcameramtx), (512, 512))   # find undistorted and resize to 512 * 512
            imgGray = cv2.resize(imgGray, (512, 512))   # resize to 512 * 512 to show smaller
            result = np.concatenate((imgGray, undistort), axis=1)  # show two pictures together
            
            cv2.imshow('1.5 Undistorted result', result)
            cv2.waitKey(1000)

        cv2.destroyWindow('1.5 Undistorted result')