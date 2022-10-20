import cv2
import numpy as np
import glob


class Question2:
    def __init__(self):
        # pattern_size = 11, 8
        self.w = 11
        self.h = 8

    def onBoard(self, dirName, text):
        fs = cv2.FileStorage(dirName + '\\Q2_lib\\alphabet_lib_onboard.txt', cv2.FILE_STORAGE_READ)   # read the lib
        self.word = text
        self.chessboardAR(fs, dirName)

    def verticalOnBoard(self, dirName, text):
        fs = cv2.FileStorage(dirName + '\\Q2_lib\\alphabet_lib_vertical.txt', cv2.FILE_STORAGE_READ)  # read the lib
        self.word = text
        self.chessboardAR(fs, dirName)

    def showWord(self, img, lines, rvecs, tvecs, mtx, dist):
        axes = np.array([[7, 5, 0], [4, 5, 0], [1, 5, 0], [7, 2, 0], [4, 2, 0], [1, 2, 0]])    # axes for showing words

        # shift the word to the axes
        shiftedAxis = np.ndarray.tolist(np.zeros(len(self.word))) #initialise
        for i in range(len(lines)):
            shiftedAxis[i] = np.float32(lines[i] + axes[i]).reshape(-1, 3)
        shiftedAxis = np.concatenate(tuple(shiftedAxis), axis=0)

        imgPoints, _ = cv2.projectPoints(shiftedAxis, rvecs, tvecs, mtx, dist) # project 3D points to image plane

        imgPoints = imgPoints.reshape(int(imgPoints.shape[0] / 2), 2, 2).astype(int)    # reshape 2D points
        
        # draw lines on the image
        for l in range(len(imgPoints)):
            img = cv2.line(img, tuple(imgPoints[l][0]), tuple(imgPoints[l][1]), (0, 0, 255), 5)
        
    def chessboardAR(self, fs, dirName):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)  # termination criteria

        objPoint = np.zeros((self.w * self.h, 3), np.float32)
        objPoint[:,:2] = np.mgrid[0:self.w, 0:self.h].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        objPoints = []  # 3d point in real world space
        imgPoints = []  # 2d points in image plane.

        filePaths = sorted(glob.glob(dirName + '\\*.bmp'), key=len)  # get all file paths
        # print(filePaths)
        for filePath in filePaths:
            img = cv2.imread(filePath)
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
            ret, corners = cv2.findChessboardCorners(imgGray, (self.w, self.h), None)   # Find the chess board corners

            # if found, add object points, image points (after refining them)
            if ret == True:
                objPoints.append(objPoint)
                corners = cv2.cornerSubPix(imgGray, corners, (self.w, self.w), (-1, -1), criteria)
                imgPoints.append(corners)

                ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, imgGray.shape[::-1], None, None)

                _, rvecs, tvecs, _ = cv2.solvePnPRansac(objPoint, corners, mtx, dist)    # Find the rotation and translation vectors.

                # get data from library
                alphabetAxis = np.ndarray.tolist(np.zeros(len(self.word)))

                # derive the shape of the "alphabet" by using the library
                for x in range(len(self.word)):
                    alphabetAxis[x] = fs.getNode(self.word[x]).mat()
                
                if any(x is None for x in alphabetAxis) or len(alphabetAxis) > 6:   # prevent there are characters not in lib, and length > 6
                    print("please input captial English charater and the length need less than 7")
                    break
                else:
                    self.showWord(img, alphabetAxis, rvecs, tvecs, mtx, dist)   # Show word on chessboard
                    img = cv2.resize(img, (1024, 1024)) # resize to 1024 * 1024 to show smaller
                    
                    cv2.imshow('AR', img)
                    cv2.waitKey(1000)

        cv2.destroyWindow('AR')