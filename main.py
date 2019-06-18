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
import cv2
from ui_main import *
from FaceFeatureExtractor import *

class MainWindow(QtWidgets.QMainWindow):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.name = ""
        self._min_size = (180, 180)
        self.img = []
        self.rimg = []
        self.rname = ""
        self.i = 0
        self.imageinadex = 0

        # load face cascade classifier
        self.face_cascade = cv2.CascadeClassifier('HAARFace.xml')
        if self.face_cascade.empty():
            QMessageBox.information(self , "Error Loading cascade classifier", "Unable to load face cascade file")
            sys.exit()

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.detectFaces)
        self.rtimer = QTimer()
        # set timer timeout callback function
        self.rtimer.timeout.connect(self.rdetectFaces)

        # set control_bt callback clicked  function
        self.ui.start_bt.clicked.connect(self.controlTimer)
        self.ui.capture_bt.clicked.connect(self.captureFaces)
        self.ui.nextImage_bt.clicked.connect(self.nextImage)
        self.ui.previousImage_bt.clicked.connect(self.prevoiusImage)

        self.ui.name_text.returnPressed.connect(self.nameChnagetevent)

        self.ui.actionAdd_Data.triggered.connect(self.changeWindowAdd)
        self.ui.actionRecognise.triggered.connect(self.changeWindowRecognise)

        self.ui.process_bt.clicked.connect(self.processImages)
        self.ui.reset_bt.clicked.connect(self.resetAddPage)
        self.ui.next_dataset_bt.clicked.connect(self.nextDatabase_Bt_Pressed)

    def nextDatabase_Bt_Pressed(self):
        self.resetAddPage()
        self.ui.reset_bt.setEnabled(True)

    def resetAddPage(self):
        self.name = ""
        self._min_size = (180, 180)
        self.img = []
        self.i = 0
        self.imageinadex = 0
        self.ui.name_text.setText("")
        self.ui.name_text.setEnabled(True)
        self.ui.start_bt.setEnabled(False)
        self.ui.capture_bt.setEnabled(False)
        self.ui.process_bt.setEnabled(False)
        self.ui.next_dataset_bt.setEnabled(False)
        self.ui.lcdNumber.display(self.i)
        self.ui.currentimage_Label.setText("0")
        self.ui.image_label.setText("")
        self.ui.camera_label.setText("")
        self.timer.stop()
        self.cap.release()
        self.ui.start_bt.setText("Start")
        self.ui.image_label.clear()
        self.ui.camera_label.clear()

    def processImages(self):
        self.ui.reset_bt.setEnabled(False)

        for j in range(self.i):
            directory = "Face/" + str(self.name)
            if not os.path.exists(directory):
                os.makedirs(directory)
            k= str(directory)+"/" + str(j) + ".jpg"
            FindFace(cv2.imread(k), self.name.replace(" ", "_"))
        self.ui.next_dataset_bt.setEnabled(True)
        self.ui.process_bt.setEnabled(False)

    def nameChnagetevent(self):
        self.ui.start_bt.setEnabled(True)
        self.ui.name_text.setEnabled(False)

    def changeWindowAdd(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def changeWindowRecognise(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def captureFaces(self):
        if self.i < 20 and self.i >= 0:
            directory= "Face/" + str(self.name)
            if not os.path.exists(directory):
                os.makedirs(directory)
            k= str(directory)+"/" + str(self.i) + ".jpg"
            self.imageinadex=self.i
            self.i+=1
            cv2.imwrite(k,self.img)
            frame = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            # show frame in img_label
            self.ui.lcdNumber.display(self.i)
            self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
            self.ui.image_label.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.currentimage_Label.setText(str(self.imageinadex+1))
            self.ui.process_bt.setEnabled(True)
        else:
            self.ui.capture_bt.setEnabled(False)

    def nextImage(self):
        directory = "Face/" + str(self.name)
        k1 = str(directory)+"/" + str(self.imageinadex+1) + ".jpg"
        if os.path.isfile(k1):
            self.imageinadex += 1
            img = cv2.imread(k1)
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            # show frame in img_label
            self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
            self.ui.image_label.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.currentimage_Label.setText(str(self.imageinadex+1))

    def prevoiusImage(self):
        directory = "Face/" + str(self.name)
        k1 = str(directory)+"/" + str(self.imageinadex-1) + ".jpg"
        if os.path.isfile(k1):
            self.imageinadex = self.imageinadex - 1
            img = cv2.imread(k1)
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            # show frame in img_label
            self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
            self.ui.image_label.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.currentimage_Label.setText(str(self.imageinadex+1))

    # detect face
    def detectFaces(self):
        self.name = self.ui.name_text.text()
        # read frame from video capture
        ret, frame = self.cap.read()

        # resize frame image
        scaling_factor = 0.8
        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

        # convert frame to GRAY format
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect rect faces
        face_rects = self.face_cascade.detectMultiScale(gray, 1.3, 4, cv2.CASCADE_SCALE_IMAGE, self._min_size)

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
        self.ui.camera_label.setPixmap(QPixmap.fromImage(qImg))
        self.ui.camera_label.setAlignment(QtCore.Qt.AlignCenter)

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.capture_bt.setEnabled(True)
            self.ui.start_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.start_bt.setText("Start")

    def rdetectFaces(self):
        self.rname = self.ui.name_text.text()
        # read frame from video capture
        ret, frame = self.cap.read()

        # resize frame image
        scaling_factor = 0.8
        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

        # convert frame to GRAY format
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect rect faces
        face_rects = self.face_cascade.detectMultiScale(gray, 1.3, 4, cv2.CASCADE_SCALE_IMAGE, self._min_size)

        # for all detected faces
        for (x, y, w, h) in face_rects:
            # draw green rect on face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_image = frame[y:y + h, x:x + w]
            self.rimg = face_image

        # convert frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # get frame infos
        height, width, channel = frame.shape
        step = channel * width
        # create QImage from RGB frame
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # show frame in img_label
        self.ui.rcamera_label.setPixmap(QPixmap.fromImage(qImg))
        self.ui.rcamera_label.setAlignment(QtCore.Qt.AlignCenter)

    def rcontrolTimer(self):
        # if timer is stopped
        if not self.rtimer.isActive():
            # create video capture
            self.rcap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.rrecognise_bt.setEnabled(True)
            self.ui.rstart_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.rtimer.stop()
            # release video capture
            self.rcap.release()
            # update control_bt text
            self.ui.rstart_bt.setText("Start")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())