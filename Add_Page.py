"""
In this example, we demonstrate how to create simple face detection using Opencv3 and PyQt5

Author: Berrouba.A
Last edited: 23 Feb 2018
"""
import os
# import system module
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

# import Opencv module
import cv2

from ui_main import *

class MainWindow(QtWidgets.QMainWindow):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.name =""
        self._min_size = (30, 30)
        self.img = []
        self.i = 0
        self.imageinadex=0

        # load face cascade classifier
        self.face_cascade = cv2.CascadeClassifier('HAARFace.xml')
        if self.face_cascade.empty():
            QMessageBox.information(self, "Error Loading cascade classifier" , "Unable to load the face	cascade classifier xml file")
            sys.exit()

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.detectFaces)

        # set control_bt callback clicked  function
        self.ui.start_bt.clicked.connect(self.controlTimer)
        self.ui.capture_bt.clicked.connect(self.captureFaces)
        self.ui.nextImage_bt.clicked.connect(self.nextImage)
        self.ui.previousImage_bt.clicked.connect(self.prevoiusImage)

    def captureFaces(self):
        directory= "Face/" + str(self.name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        k= str(directory)+"/" + str(self.i) + ".jpg"
        self.i+=1
        cv2.imwrite(k,self.img)
        frame = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # show frame in img_label
        self.ui.image_lable.setPixmap(QPixmap.fromImage(qImg))
        self.ui.image_lable.setAlignment(QtCore.Qt.AlignCenter)

    def nextImage(self):
        directory= "Face/" + str(self.name)
        k= str(directory)+"/" + str(self.imageinadex) + ".jpg"
        img = cv2.imread(k)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # show frame in img_label
        k1 = str(directory)+"/" + str(self.imageinadex+1) + ".jpg"
        if os.path.isfile(k1):
            self.imageinadex += 1
        self.ui.image_lable.setPixmap(QPixmap.fromImage(qImg))
        self.ui.image_lable.setAlignment(QtCore.Qt.AlignCenter)

    def prevoiusImage(self):
        directory= "Face/" + str(self.name)
        k= str(directory)+"/" + str(self.imageinadex) + ".jpg"
        img = cv2.imread(k)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # show frame in img_label
        k1 = str(directory)+"/" + str(self.imageinadex-1) + ".jpg"
        if os.path.isfile(k1):
            self.imageinadex -= 1
        self.ui.image_lable.setPixmap(QPixmap.fromImage(qImg))
        self.ui.image_lable.setAlignment(QtCore.Qt.AlignCenter)

    # detect face
    def detectFaces(self):
        self.name = self.ui.name_text.toPlainText()
        # read frame from video capture
        ret, frame = self.cap.read()

        # resize frame image
        scaling_factor = 0.8
        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

        # convert frame to GRAY format
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect rect faces
        face_rects = self.face_cascade.detectMultiScale(gray, 1.3, 4,cv2.CASCADE_SCALE_IMAGE,self._min_size)

        # for all detected faces
        for (x, y, w, h) in face_rects:
            # draw green rect on face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_image = frame[y:y + h, x:x + w]
            self.img = face_image

        # convert frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # get frame infos
        height, width, channel = frame.shape
        step = channel * width
        # create QImage from RGB frame
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # show frame in img_label
        self.ui.camera_lable.setPixmap(QPixmap.fromImage(qImg))
        self.ui.camera_lable.setAlignment(QtCore.Qt.AlignCenter)



    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.start_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.start_bt.setText("Start")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())