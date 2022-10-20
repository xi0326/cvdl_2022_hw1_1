from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import MainWindow as ui
import os

from Q1.Q1 import Question1
from Q2.Q2 import Question2
from Q3.Q3 import Question3


class Main(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Load data
        self.pushButtonLoadFolder.clicked.connect(self.selectDir)
        self.pushButtonLoadImageL.clicked.connect(self.getImLPath)
        self.pushButtonLoadImageR.clicked.connect(self.getImRPath)
        
        # self.pushButtonFindCorners.clicked.connect(lambda: Q1Object.test(self.dirName))
        # Question 1
        self.pushButtonFindCorners.clicked.connect(lambda: Q1Object.findCorner(self.dirName))
        self.pushButtonFindIntrinsicMatrix.clicked.connect(lambda: Q1Object.findIntrinsic(self.dirName))
        self.pushButtonFindExtrinsicMatrix.clicked.connect(lambda: Q1Object.findExtrinsic(self.dirName, self.comboBoxFindExtrinsic.currentText()))
        self.pushButtonFindDistortionMatrix.clicked.connect(Q1Object.findDistortion)
        self.pushButtonShowUndistortedResult.clicked.connect(lambda: Q1Object.showUndistortion(self.dirName))

        # Question 2
        self.pushButtonShowWordsOnBoard.clicked.connect(lambda: Q2Object.onBoard(self.dirName, self.textEditAugmentedReality.toPlainText()))
        self.pushButtonShowWordsVertically.clicked.connect(lambda: Q2Object.verticalOnBoard(self.dirName, self.textEditAugmentedReality.toPlainText()))

        # Question 3
        self.pushButtonShowStereoDisparityMap.clicked.connect(lambda: Q3Object.stereoDisparityMap(self.ImLPath, self.ImRPath))
    

    def selectDir(self):
        self.dirName = QtCore.QDir.toNativeSeparators(QtWidgets.QFileDialog.getExistingDirectory(None, caption='Select a folder:', directory='C:\\', options=QtWidgets.QFileDialog.ShowDirsOnly))
    
    def selectFile(self):
        fileName = QtCore.QDir.toNativeSeparators(QtWidgets.QFileDialog.getOpenFileName(None, caption='Choose a File', directory='C:\\', filter='Image Files (*.png *.jpg *.bmp)')[0])  # get turple[0] which is file name
        return fileName
    
    def getImLPath(self):
        self.ImLPath = self.selectFile()
    
    def getImRPath(self):
        self.ImRPath = self.selectFile()
    
    # overide to force exit
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super().closeEvent(a0)
        os._exit(0)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Q1Object = Question1()
    Q2Object = Question2()
    Q3Object = Question3()
    window = Main()
    window.show()
    sys.exit(app.exec_())