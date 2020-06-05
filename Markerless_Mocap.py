import win32gui
import os
import sys
import socket
import json
import time
import ctypes
import datetime
from cv2 import *
import numpy as np
import ctypes.util
import pyqtgraph as pg
import pypylon.pylon as py
import pyqtgraph.opengl as gl
from PyQt5.QtCore import QSize
from threading import Thread, Lock
from ctypes import Structure, byref
from ctypes.util import find_library
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
from distutils.core import setup, Extension
from pygrabber.dshow_graph import FilterGraph
from PyQt5.QtGui import QImage, QPixmap, QIcon
from ctypes import c_int, c_void_p, c_char_p, c_float, c_uint16, c_uint32, c_uint8
from PyQt5.QtWidgets import QToolBar, QAction, QMainWindow, QComboBox, QListWidget, QPlainTextEdit,QFileDialog, QProgressBar, QLabel, QRadioButton, QLineEdit,QWidget,QSizePolicy






#--------------------------------------------------------------------------#
                        #Main GUI#
#--------------------------------------------------------------------------# 
class Ui_Dialog(QMainWindow):
    def setupUi(self, Dialog):
        global Bas_cap
        global Bas_cap2
        global Bas_cap3
        global Bas_cap4
        global Bas_cap5
        global Bas_cap6
        global Bas_cap7
        global Bas_cap8
        global cal_window

        Bas_cap=[]
        Bas_cap2=[]
        Bas_cap3=[]
        Bas_cap4=[]
        Bas_cap5=[]
        Bas_cap6=[]
        Bas_cap7=[]
        Bas_cap8=[]
        
        self.camcal1=0
        self.camcal2=0
        self.camcal3=0
        self.camcal4=0
        self.camcal5=0
        self.camcal6=0
        self.camcal7=0
        self.camcal8=0

        cap="none"
        cal_window=0
        self.cameras_open=0
        self.scale_percent=100
        self.basler_cameras_amount=0
        Dialog.setObjectName("Dialog")
        self.master_camera_List=[]
        self.propwindow=0

        width = Dialog.frameGeometry().width()
        height = Dialog.frameGeometry().height()
        Dialog.setStyleSheet("background-color: rgb(36, 36, 36);")

        widget_width= width-200
        widget_width2=width+200
        widget_height= height-190
        widget_height2=height+155

        self.BGR="BayerRG8"
        
        self.TriggerMode_On="On"
        self.TriggerSelector_AcquisitionStart="AcquisitionStart"
        self.TriggerSelector_FrameStart="FrameStart"
        self.Trigger_ON="On"
        self.Trigger_OFF="Off"
        self.TriggerSource_Line1="Line1"
        self.AcquisitionMode_Continuous="Continuous"
        self.AcquisitionMode_SingleFrame="SingleFrame"
        self.TriggerActivation_RisingEdge= "RisingEdge"
        self.ExposureMode_TriggerWidth="TriggerWidth"
        self.new_w=2046
        self.new_w=int(self.new_w)
        self.new_h=1080
        self.new_h=int(self.new_h)
        self.ChunkSelector_Timestamp="Timestamp"
        
        self.video_box =  QtWidgets.QLabel(Dialog)
        self.video_box.setGeometry(QtCore.QRect(55, 55, widget_width, widget_height))
        boxwidth=self.video_box.frameGeometry().width()
        boxheight=self.video_box.frameGeometry().height()
        self.video_box.setStyleSheet("background-color: rgb(0, 0, 0);border: 1px solid black;")
        self.video_box.setObjectName("vid_box_1")

        self.video_box2 =  QtWidgets.QLabel(Dialog)
        self.video_box2.setGeometry(QtCore.QRect(55, 400, widget_width, widget_height))
        boxwidth2=self.video_box2.frameGeometry().width()
        boxheight2=self.video_box2.frameGeometry().height()
        self.video_box2.setStyleSheet("background-color: rgb(0, 0, 0);border: 1px solid black;")
        self.video_box2.setObjectName("vid_box_2")

        self.Camera_Dropdown= QComboBox(Dialog)
        self.Camera_Dropdown.setGeometry(QtCore.QRect(width-280, height-455, 130, 21))
        self.Camera_Dropdown.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.Camera_Dropdown.addItem("Camera 1")
        self.Camera_Dropdown.addItem("Camera 2")
        self.Camera_Dropdown.addItem("Camera 3")
        self.Camera_Dropdown.addItem("Camera 4")
        self.Camera_Dropdown.addItem("Camera 5")
        self.Camera_Dropdown.addItem("Camera 6")
        self.Camera_Dropdown.addItem("Camera 7")
        self.Camera_Dropdown.addItem("Camera 8")
        self.Camera_Dropdown.addItem("3D Perspective")
        self.Camera_Dropdown.setCurrentIndex(0)

        self.Camera_Dropdown2= QComboBox(Dialog)
        self.Camera_Dropdown2.setGeometry(QtCore.QRect(width-280, height-110, 130, 21))
        self.Camera_Dropdown2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.Camera_Dropdown2.addItem("Camera 1")
        self.Camera_Dropdown2.addItem("Camera 2")
        self.Camera_Dropdown2.addItem("Camera 3")
        self.Camera_Dropdown2.addItem("Camera 4")
        self.Camera_Dropdown2.addItem("Camera 5")
        self.Camera_Dropdown2.addItem("Camera 6")
        self.Camera_Dropdown2.addItem("Camera 7")
        self.Camera_Dropdown2.addItem("Camera 8")
        self.Camera_Dropdown2.addItem("3D Perspective")
        self.Camera_Dropdown2.setCurrentIndex(1)

        self.Camera_Dropdown3= QComboBox(Dialog)
        self.Camera_Dropdown3.setGeometry(QtCore.QRect(width+565, height-455, 130, 21))
        self.Camera_Dropdown3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.Camera_Dropdown3.addItem("3D Perspective")
        self.Camera_Dropdown3.addItem("Ortho X+")
        self.Camera_Dropdown3.addItem("Ortho X-")
        self.Camera_Dropdown3.addItem("Ortho Y+")
        self.Camera_Dropdown3.addItem("Ortho Y-")
        self.Camera_Dropdown3.addItem("Ortho Z+")
        self.Camera_Dropdown3.addItem("Ortho Z-")
        self.Camera_Dropdown3.setCurrentIndex(0)

        self.toolbarHor = QToolBar(Dialog)
        self.toolbarHor.setIconSize(QSize(40, 40))
        self.toolbarHor.setOrientation(QtCore.Qt.Horizontal)
        self.toolbarHor.setStyleSheet("QToolBar{spacing:200px;}")
        self.toolbarHor.setStyleSheet("QToolButton{padding-top:4px;}")
        self.toolbarHor.addSeparator()
        self.toolbarHor.addSeparator()
        self.toolbarHor.addSeparator()
        self.toolbarHor.addSeparator()
        self.toolbarHor.addSeparator()
        self.toolbarHor.addSeparator()
        self.toolbarHor.addSeparator()
        self.toolbarHor.addSeparator()
        self.toolbarHor.addSeparator()
        self.toolbarHor.addSeparator()

        
        Stream_action = QAction(QIcon('images/open.png'),'Open Stream', self)
        Stream_action.triggered.connect(self.Video_stream)
        self.toolbarHor.addAction(Stream_action)

        closecameras_action = QAction(QIcon('images/closecameras.png'),'close Stream', self)
        closecameras_action.triggered.connect(self.close_Cameras)
        self.toolbarHor.addAction(closecameras_action)

        

        self.toolbar = QToolBar(Dialog)
        self.toolbar.setIconSize(QSize(40, 40))
        self.toolbar.setOrientation(QtCore.Qt.Vertical)

        connect_action = QAction(QIcon('images/CameraConnect.png'),'Connect Cameras', self)
        connect_action.triggered.connect(self.Connect_Cameras)
        self.toolbar.addAction(connect_action)

        
        tool_action = QAction(QIcon('images/tools.png'),'Camera Tools', self)
        self.toolbar.addAction(tool_action)
        tool_action.triggered.connect(self.properties_window_A)

        calibrate_action = QAction(QIcon('images/calibrate.png'),'Calibration', self)
        self.toolbar.addAction(calibrate_action)
        calibrate_action.triggered.connect(self.calibrate_cameras)

        open_actioncalib = QAction(QIcon('images/opencalib.png'),'Open Calibration', self)
        self.toolbar.addAction(open_actioncalib)
        open_actioncalib.triggered.connect(self.Open_calibration_files)
        
        exit_action = QAction(QIcon('images/exit.png'),'Exit', self)
        self.toolbar.addAction(exit_action)
        exit_action.triggered.connect(self.window_close)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        self.threeD_view()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate  
        Dialog.setWindowTitle(_translate("Dialog", "Markerless Mocap"))

    def threeD_view(self):#-----------------------------------------------------# 3D gui graphic
        self.width = Dialog.frameGeometry().width()
        self.height = Dialog.frameGeometry().height()
        
        self.widget_width2=self.width+200
        self.widget_height2=self.height+155
        
        self.w = gl.GLViewWidget(Dialog)
        self.w.opts['distance'] = 40
        self.w.setGeometry(500, 55, self.widget_width2, self.widget_height2)
        self.w.setBackgroundColor('k')
        
        gz = gl.GLGridItem()
        gz.translate(0, 0, 0)
        self.w.addItem(gz)

        self.ax = gl.GLAxisItem()
        self.ax.translate(0,0,0.5)
        self.ax.rotate(180,0,1,0)
        self.ax.setSize(1,1,1)
        self.ax.show()
        self.w.addItem(self.ax)
        
          
    def Connect_Cameras(self):#-----------------------------------------------------# Connect cameras button
                               
    #-----------------------------------------------------# Get Basler camera usb list
        self.deviceName=None
        self.deviceName = self.deviceName
        self.tlfactory = py.TlFactory.GetInstance()
        self.deviceInfoList = self.tlfactory.EnumerateDevices()

        for i in range(len(self.deviceInfoList)):
            self.deviceName = self.deviceInfoList[i].GetUserDefinedName()
            self.deviceIndex = i
            self.camera = py.InstantCamera(self.tlfactory.CreateDevice(self.deviceInfoList[self.deviceIndex]))
            self.CameraSerialNumber = self.camera.GetDeviceInfo().GetPropertyValue('SerialNumber')


            if self.deviceIndex==0: ## camera 1
                self.basler_1=self.camera
                self.basler_cameras_amount=self.basler_cameras_amount+1
                self.master_camera_List.append("Basler:"+str(self.CameraSerialNumber[1]))
            elif self.deviceIndex ==1: ##camera 2
                self.basler_2=self.camera
                self.basler_cameras_amount=self.basler_cameras_amount+1
                self.master_camera_List.append("Basler:"+str(self.CameraSerialNumber[1]))
            elif self.deviceIndex ==2: ##camera 3
                self.basler_3=self.camera
                self.basler_cameras_amount=self.basler_cameras_amount+1
                self.master_camera_List.append("Basler:"+str(self.CameraSerialNumber[1]))
            elif self.deviceIndex ==3: ##camera 4
                self.basler_4=self.camera
                self.basler_cameras_amount=self.basler_cameras_amount+1
                self.master_camera_List.append("Basler:"+str(self.CameraSerialNumber[1]))
            elif self.deviceIndex ==4: ##camera 5
                self.basler_5=self.camera
                self.basler_cameras_amount=self.basler_cameras_amount+1
                self.master_camera_List.append("Basler:"+str(self.CameraSerialNumber[1]))
            elif self.deviceIndex ==5: ##camera 6
                self.basler_6=self.camera
                self.basler_cameras_amount=self.basler_cameras_amount+1
                self.master_camera_List.append("Basler:"+str(self.CameraSerialNumber[1]))
            elif self.deviceIndex ==6: ##camera 7
                self.basler_7=self.camera
                self.basler_cameras_amount=self.basler_cameras_amount+1
                self.master_camera_List.append("Basler:"+str(self.CameraSerialNumber[1]))
            elif self.deviceIndex ==7: ##camera 8
                self.basler_8=self.camera
                self.basler_cameras_amount=self.basler_cameras_amount+1
                self.master_camera_List.append("Basler:"+str(self.CameraSerialNumber[1]))

        
        self.error_dialog = QtWidgets.QErrorMessage()
        self.error_dialog.showMessage(str(len(self.master_camera_List))+ " Cameras connected")
        self.error_dialog.setWindowTitle("Cameras connected")
            
    def close_Cameras(self):#-----------------------------------------------------# Close cameras button

#---------------------------------------------------#
        try:
            if Bas_cap.IsOpen()==True:
                Bas_cap.StopGrabbing()
                Bas_cap.Close()
        except:
            pass
        try:
            if Bas_cap2.IsOpen()==True:
                Bas_cap2.StopGrabbing()
                Bas_cap2.Close()
        except:
            pass
        try:
            if Bas_cap3.IsOpen()==True:
                Bas_cap3.StopGrabbing()
                Bas_cap3.Close()
        except:
            pass
        try:
            if Bas_cap4.IsOpen()==True:
                Bas_cap4.StopGrabbing()
                Bas_cap4.Close()
        except:
            pass
        try:
            if Bas_cap5.IsOpen()==True:
                Bas_cap5.StopGrabbing()
                Bas_cap5.Close()
        except:
            pass
        try:
            if Bas_cap6.IsOpen()==True:
                Bas_cap6.StopGrabbing()
                Bas_cap6.Close()
        except:
            pass
        try:
            if Bas_cap7.IsOpen()==True:
                Bas_cap7.StopGrabbing()
                Bas_cap7.Close()
        except:
            pass

        try:
            if Bas_cap8.IsOpen()==True:
                Bas_cap8.StopGrabbing()
                Bas_cap8.Close()
        except:
            pass
    cv2.destroyAllWindows()
        
    def Video_stream(self):#-----------------------------------------------------# initialize video stream
        global Bas_cap
        global Bas_cap2
        global Bas_cap3
        global Bas_cap4
        global Bas_cap5
        global Bas_cap6
        global Bas_cap7
        global Bas_cap8

        self.color1=[]
        self.color2=[]
        self.color3=[]
        self.color4=[]
        self.color5=[]
        self.color6=[]
        self.color7=[]
        self.color8=[]
        
        fps=30
        
        print(self.master_camera_List)
        for i in range(len(self.master_camera_List)):
            if 'Basler' in self.master_camera_List[i]:
                if i==0:
                    Bas_cap = self.basler_1
                    Bas_cap.Open()
                    if Bas_cap.IsOpen()==True:
                        Bas_cap.PixelFormat.SetValue(self.BGR)
                        Bas_cap.AcquisitionFrameRate.SetValue(fps)
                        if '22036926' in self.master_camera_List[i]:
                            Bas_cap.DeviceLinkThroughputLimit.SetValue(70000000)
                            Bas_cap.AcquisitionFrameRateEnable.SetValue(True)
                        if '22036927' in self.master_camera_List[i]:
                            Bas_cap.DeviceLinkThroughputLimit.SetValue(70000000)
                            Bas_cap.AcquisitionFrameRateEnable.SetValue(True)
                        if '22414460' in self.master_camera_List[i]:
                            Bas_cap.DeviceLinkThroughputLimit.SetValue(60000000)
                        if '22414462' in self.master_camera_List[i]:
                            Bas_cap.DeviceLinkThroughputLimit.SetValue(60000000)

                        
                        Bas_cap.GainAuto.SetValue("Off")
                        Bas_cap.BalanceWhiteAuto.SetValue("Off")
                        Bas_cap.ExposureAuto.SetValue("Off")
                        self.new_w=Bas_cap.Width.GetValue()
                        self.new_h=Bas_cap.Height.GetValue()
                        Bas_cap.Width.SetValue(self.new_w)
                        Bas_cap.Height.SetValue(self.new_h)
                        Bas_cap.MaxNumBuffer = 2
                        
                        Bas_cap.StartGrabbing()
                        self.bas1=Thread(target=self.cameraBasler1_stream)
                        self.bas1.setDaemon(True)
                        self.bas1.start()
                        
                        
                if i==1:
                    Bas_cap2 = self.basler_2
                    Bas_cap2.Open()
                    if Bas_cap2.IsOpen()==True:
                        Bas_cap2.PixelFormat.SetValue(self.BGR)
                        Bas_cap2.AcquisitionFrameRate.SetValue(fps)
                        if '22036926' in self.master_camera_List[i]:
                            Bas_cap2.DeviceLinkThroughputLimit.SetValue(70000000)
                            Bas_cap2.AcquisitionFrameRateEnable.SetValue(True)
                        if '22036927' in self.master_camera_List[i]:
                            Bas_cap2.DeviceLinkThroughputLimit.SetValue(70000000)
                            Bas_cap2.AcquisitionFrameRateEnable.SetValue(True)
                        if '22414460' in self.master_camera_List[i]:
                            Bas_cap2.DeviceLinkThroughputLimit.SetValue(60000000)
                        if '22414462' in self.master_camera_List[i]:
                            Bas_Cap2.DeviceLinkThroughputLimit.SetValue(60000000)


                        Bas_cap2.GainAuto.SetValue("Off")
                        Bas_cap2.BalanceWhiteAuto.SetValue("Off")
                        Bas_cap2.ExposureAuto.SetValue("Off")
                        self.new_w=Bas_cap2.Width.GetValue()
                        self.new_h=Bas_cap2.Height.GetValue()
                        Bas_cap2.Width.SetValue(self.new_w)
                        Bas_cap2.Height.SetValue(self.new_h)
                        Bas_cap2.MaxNumBuffer = 2
                        
                        Bas_cap2.StartGrabbing()
                        self.bas2=Thread(target=self.cameraBasler2_stream)
                        self.bas2.setDaemon(True)
                        self.bas2.start()
                        
                if i==2:
                    Bas_cap3 = self.basler_3
                    Bas_cap3.Open()
                    if Bas_cap3.IsOpen()==True:
                        Bas_cap3.PixelFormat.SetValue(self.BGR)
                        Bas_cap3.AcquisitionFrameRate.SetValue(fps)
                        if '22036926' in self.master_camera_List[i]:
                            Bas_cap3.DeviceLinkThroughputLimit.SetValue(70000000)
                            Bas_cap3.AcquisitionFrameRateEnable.SetValue(True)
                        if '22036927' in self.master_camera_List[i]:
                            Bas_cap3.DeviceLinkThroughputLimit.SetValue(70000000)
                            Bas_cap3.AcquisitionFrameRateEnable.SetValue(True)
                        if '22414460' in self.master_camera_List[i]:
                            Bas_cap3.DeviceLinkThroughputLimit.SetValue(60000000)
                        if '22414462' in self.master_camera_List[i]:
                            Bas_cap3.DeviceLinkThroughputLimit.SetValue(60000000)

                        Bas_cap3.GainAuto.SetValue("Off")
                        Bas_cap3.BalanceWhiteAuto.SetValue("Off")
                        Bas_cap3.ExposureAuto.SetValue("Off")
                        self.new_w=Bas_cap3.Width.GetValue()
                        self.new_h=Bas_cap3.Height.GetValue()
                        Bas_cap3.Width.SetValue(self.new_w)
                        Bas_cap3.Height.SetValue(self.new_h)
                        Bas_cap3.MaxNumBuffer = 2
                        
                        Bas_cap3.StartGrabbing()
                        self.bas3=Thread(target=self.cameraBasler3_stream)
                        self.bas3.setDaemon(True)
                        self.bas3.start()
                        
                        
                if i==3:
                    Bas_cap4 = self.basler_4
                    Bas_cap4.Open()
                    if Bas_cap4.IsOpen()==True:
                        Bas_cap4.PixelFormat.SetValue(self.BGR)  
                        Bas_cap4.AcquisitionFrameRate.SetValue(fps)
                        if '22036926' in self.master_camera_List[i]:
                            Bas_cap4.DeviceLinkThroughputLimit.SetValue(70000000)
                            Bas_cap4.AcquisitionFrameRateEnable.SetValue(True)
                        if '22036927' in self.master_camera_List[i]:
                            Bas_cap4.DeviceLinkThroughputLimit.SetValue(70000000)
                            Bas_cap4.AcquisitionFrameRateEnable.SetValue(True)
                        if '22414460' in self.master_camera_List[i]:
                            Bas_cap4.DeviceLinkThroughputLimit.SetValue(60000000)
                        if '22414462' in self.master_camera_List[i]:
                            Bas_cap4.DeviceLinkThroughputLimit.SetValue(60000000)

                        Bas_cap4.GainAuto.SetValue("Off")
                        Bas_cap4.BalanceWhiteAuto.SetValue("Off")
                        Bas_cap4.ExposureAuto.SetValue("Off")
                        self.new_w=Bas_cap4.Width.GetValue()
                        self.new_h=Bas_cap4.Height.GetValue()
                        Bas_cap4.Width.SetValue(self.new_w)
                        Bas_cap4.Height.SetValue(self.new_h)
                        Bas_cap4.MaxNumBuffer = 2
                        
                        Bas_cap4.StartGrabbing()
                        self.bas4=Thread(target=self.cameraBasler4_stream)
                        self.bas4.setDaemon(True)
                        self.bas4.start()
##                        
##                if i==4:
##                    Bas_cap5 = self.basler_5
##                    Bas_cap5.Open()
##                    if Bas_cap5.IsOpen()==True:
##                        Bas_cap5.PixelFormat.SetValue(self.RGB)
##                        self.new_w=Bas_cap5.Width.GetValue()
##                        self.new_h=Bas_cap5.Height.GetValue()
##                        Bas_cap5.Width.SetValue(self.new_w)
##                        Bas_cap5.Height.SetValue(self.new_h)
##                        Bas_cap5.MaxNumBuffer = 2
##                        
##                        Bas_cap5.StartGrabbing()
##                        self.bas5=Thread(target=self.cameraBasler5_stream)
##                        self.bas5.setDaemon(True)
##                        self.bas5.start()
##                        
##                if i==5:
##                    Bas_cap6 = self.basler_6
##                    Bas_cap6.Open()
##                    if Bas_cap6.IsOpen()==True:
##                        Bas_cap6.PixelFormat.SetValue(self.RGB)
##                        self.new_w=Bas_cap6.Width.GetValue()
##                        self.new_h=Bas_cap6.Height.GetValue()
##                        Bas_cap6.Width.SetValue(self.new_w)
##                        Bas_cap6.Height.SetValue(self.new_h)
##                        Bas_cap6.MaxNumBuffer = 2
##
##                        Bas_cap6.StartGrabbing()
##                        self.bas6=Thread(target=self.cameraBasler6_stream)
##                        self.bas6.setDaemon(True)
##                        self.bas6.start()
##                        
##                if i==6:
##                    Bas_cap7 = self.basler_7
##                    Bas_cap7.Open()
##                    if Bas_cap7.IsOpen()==True:
##                        Bas_cap7.PixelFormat.SetValue(self.RGB)
##                        self.new_w=Bas_cap7.Width.GetValue()
##                        self.new_h=Bas_cap7.Height.GetValue()
##                        Bas_cap7.Width.SetValue(self.new_w)
##                        Bas_cap7.Height.SetValue(self.new_h)
##                        Bas_cap7.MaxNumBuffer = 2
##
##                        Bas_cap7.StartGrabbing()
##                        self.bas7=Thread(target=self.cameraBasler7_stream)
##                        self.bas7.setDaemon(True)
##                        self.bas7.start()
##                        
##                if i==7:
##                    Bas_cap8 = self.basler_8
##                    Bas_cap8.Open()
##                    if Bas_cap8.IsOpen()==True:
##                        Bas_cap8.PixelFormat.SetValue(self.RGB)
##                        self.new_w=Bas_cap8.Width.GetValue()
##                        self.new_h=Bas_cap8.Height.GetValue()
##                        Bas_cap8.Width.SetValue(self.new_w)
##                        Bas_cap8.Height.SetValue(self.new_h)
##                        Bas_cap8.MaxNumBuffer = 2
##                        
##                        Bas_cap8.StartGrabbing()
##                        self.bas8=Thread(target=self.cameraBasler8_stream)
##                        self.bas8.setDaemon(True)
##                        self.bas8.start()

###-----------------------------------------------------# stream with camera calibrations       
##        if self.camcal1==1:
##            self.cam1width=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
##            self.cam1height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
##            size=(int(self.cam1width),int(self.cam1height))
##            crop=1
##            self.cam1_newmat, self.cam1_ROI=cv2.getOptimalNewCameraMatrix(self.camera1_matrix,self.camera1_coeffs,size, 0,size,centerPrincipalPoint=1)
##            self.cam1_mapx,self.cam1_mapy = cv2.initUndistortRectifyMap(self.camera1_matrix,self.camera1_coeffs, None,self.cam1_newmat, size, 5)
##            
##        if self.camcal2==1:
##            self.cam2width=cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)
##            self.cam2height=cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)
##            size2=(int(self.cam2width),int(self.cam2height))
##            crop2=1
##            self.cam2_newmat, self.cam2_ROI=cv2.getOptimalNewCameraMatrix(self.camera2_matrix,self.camera2_coeffs, size2, 0, size2,centerPrincipalPoint=1)
##            self.cam2_mapx,self.cam2_mapy = cv2.initUndistortRectifyMap(self.camera2_matrix,self.camera2_coeffs, None,self.cam2_newmat, size2,5)
##
##        self.camcal3=0
##        self.camcal4=0
##        self.camcal5=0
##        self.camcal6=0
##        self.camcal7=0
##        self.camcal8=0
##              
##            
##        
#--------------------------------------------------------------------------#
                        #Camera streams#
#--------------------------------------------------------------------------#
    def cameraBasler1_stream(self):#-----------------------------------------------------# Stream basler 1 operations
        global Bas_cap
        while Bas_cap.IsGrabbing():
            img_old_1= Bas_cap.RetrieveResult(5000,py.TimeoutHandling_ThrowException)
          #  if self.propwindow==1:
          #      img_old_1.Release()
          #      break
            if img_old_1.GrabSucceeded():
                width=int(img_old_1.Array.shape[1]*self.scale_percent/100)
                height=int(img_old_1.Array.shape[0]*self.scale_percent/100)
                dim=(width,height)
                img=cv2.resize(img_old_1.Array, dim, interpolation = cv2.INTER_AREA)
                
                self.index = self.Camera_Dropdown.currentIndex()
                self.index_2=self.Camera_Dropdown2.currentIndex()
                if self.index==0:
                    if cal_window==0:
                        self.displayImageb1(img,1)
                        time.sleep(0.005)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                        
                if self.index_2==0:
                    if cal_window==0:
                        self.displayImageb1(img,1)
                        time.sleep(0.005)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                        
                if cal_window==1:
                    self.uicalibration.displayImagecalibb1(self.calibwin, img, 1)
                    time.sleep(0.005)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                pass
        img_old_1.Release()
        cv2.destroyAllWindows()
        
    def cameraBasler2_stream(self):#-----------------------------------------------------# Stream basler 2 operations
        global Bas_cap2
        while Bas_cap2.IsGrabbing():
            img_old_1= Bas_cap2.RetrieveResult(5000,py.TimeoutHandling_ThrowException)
         #   if self.propwindow==1:
         #       img_old_1.Release()
         #       break
            if img_old_1.GrabSucceeded():  
                width=int(img_old_1.Array.shape[1]*self.scale_percent/100)
                height=int(img_old_1.Array.shape[0]*self.scale_percent/100)
                dim=(width,height)
                img2=cv2.resize(img_old_1.Array, dim, interpolation = cv2.INTER_AREA) 

                self.index = self.Camera_Dropdown.currentIndex()
                self.index_2=self.Camera_Dropdown2.currentIndex()
                if self.index==1:
                    if cal_window==0:
                        self.displayImageb2(img2,1)
                        time.sleep(0.005)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                if self.index_2==1:
                    if cal_window==0:
                        self.displayImageb2(img2,1)
                        time.sleep(0.005)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                if cal_window==1:
                    self.uicalibration.displayImagecalibb2(self.calibwin, img2, 1)
                    time.sleep(0.005)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                pass
        img_old_1.Release()
        cv2.destroyAllWindows()

    def cameraBasler3_stream(self):#-----------------------------------------------------# Stream basler 3 operations
        global Bas_cap3
        while Bas_cap3.IsGrabbing():
            img_old_1= Bas_cap3.RetrieveResult(5000,py.TimeoutHandling_ThrowException)
        #    if self.propwindow==1:
        #        img_old_1.Release()
       #         break
            if img_old_1.GrabSucceeded():
                    
                width=int(img_old_1.Array.shape[1]*self.scale_percent/100)
                height=int(img_old_1.Array.shape[0]*self.scale_percent/100)
                dim=(width,height)
                img3=cv2.resize(img_old_1.Array, dim, interpolation = cv2.INTER_AREA)

                self.index = self.Camera_Dropdown.currentIndex()
                
                self.index_2=self.Camera_Dropdown2.currentIndex()
                if self.index==2:
                    if cal_window==0:
                        self.displayImageb3(img3,1)
                        time.sleep(0.005)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                if self.index_2==2:
                    if cal_window==0:
                        self.displayImageb3(img3,1)
                        time.sleep(0.005)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                if cal_window==1:
                    self.uicalibration.displayImagecalibb3(self.calibwin, img3, 1)
                    time.sleep(0.005)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                pass
                #print("Error: ", img_old_1.ErrorCode, img_old_1.ErrorDescription)
        img_old_1.Release()
        cv2.destroyAllWindows()

    def cameraBasler4_stream(self):#-----------------------------------------------------# Stream basler 4 operations
        global Bas_cap4
        while Bas_cap4.IsGrabbing():
            img_old_1= Bas_cap4.RetrieveResult(5000,py.TimeoutHandling_ThrowException)
         #   if self.propwindow==1:
         #       img_old_1.Release()
         #       break
            if img_old_1.GrabSucceeded():                
                width=int(img_old_1.Array.shape[1]*self.scale_percent/100)
                height=int(img_old_1.Array.shape[0]*self.scale_percent/100)
                dim=(width,height)
                img4=cv2.resize(img_old_1.Array, dim, interpolation = cv2.INTER_AREA)

                self.index = self.Camera_Dropdown.currentIndex()
                self.index_2=self.Camera_Dropdown2.currentIndex()
                if self.index==3:
                    if cal_window==0:
                        self.displayImageb4(img4,1)
                        time.sleep(0.005)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                if self.index_2==3:
                    if cal_window==0:
                        self.displayImageb4(img4,1)
                        time.sleep(0.005)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                if cal_window==1:
                    self.uicalibration.displayImagecalibb4(self.calibwin, img4, 1)
                    time.sleep(0.005)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                pass
        img_old_1.Release()
        cv2.destroyAllWindows()
        

#--------------------------------------------------------------------------#
                        #Camera image manipulation#
#--------------------------------------------------------------------------#

    def displayImageb1(self,img,window=1):#-----------------------------------------------------# Stream basler 1 manipulation
        global cal_window
        qformat=QImage.Format_Indexed8
        if (len(img.shape))==3: #[0]=rows,[1]=cols,[2]=channels
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        Out_img=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)  
       # Out_Img=Out_img.rgbSwapped() #BGR>>RGB

        if window==1:
            if self.index==0:
                self.video_box.setPixmap(QPixmap.fromImage(Out_img))
                self.video_box.setScaledContents(True)
            if self.index_2==0:
                self.video_box2.setPixmap(QPixmap.fromImage(Out_img))
                self.video_box2.setScaledContents(True)

    def displayImageb2(self,img2,window=1):#-----------------------------------------------------# Stream basler 2 manipulation
        global cal_window
        # conversion of cam 3 into pyqt widget
     #   print("3=ok")
        qformat=QImage.Format_Indexed8
        if (len(img2.shape))==3: #[0]=rows,[1]=cols,[2]=channels
            if img2.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        Out_img2=QImage(img2,img2.shape[1],img2.shape[0],img2.strides[0],qformat)  
      #  Out_Img2=Out_img2.rgbSwapped() #BGR>>RGB
        
        if window==1:
            if self.index==1:
                 self.video_box.setPixmap(QPixmap.fromImage(Out_img2))
                 self.video_box.setScaledContents(True)
            if self.index_2==1:
                self.video_box2.setPixmap(QPixmap.fromImage(Out_img2))
                self.video_box2.setScaledContents(True)
                
    def displayImageb3(self,img3,window=1):#-----------------------------------------------------# Stream basler 3 manipulation
        global cal_window
        qformat=QImage.Format_Indexed8
        if (len(img3.shape))==3: #[0]=rows,[1]=cols,[2]=channels
            if img3.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        Out_img3=QImage(img3,img3.shape[1],img3.shape[0],img3.strides[0],qformat)  
      #  Out_Img3=Out_img3.rgbSwapped() #BGR>>RGB
        
        if window==1:
            if self.index==2:
                 self.video_box.setPixmap(QPixmap.fromImage(Out_img3))
                 self.video_box.setScaledContents(True)
            if self.index_2==2:
                self.video_box2.setPixmap(QPixmap.fromImage(Out_img3))
                self.video_box2.setScaledContents(True)

    def displayImageb4(self,img4,window=1):#-----------------------------------------------------# Stream basler 4 manipulation
        global cal_window
        qformat=QImage.Format_Indexed8
        if (len(img4.shape))==3: #[0]=rows,[1]=cols,[2]=channels
            if img4.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        Out_img4=QImage(img4,img4.shape[1],img4.shape[0],img4.strides[0],qformat)  
     #   Out_Img4=Out_img4.rgbSwapped() #BGR>>RGB
        
        if window==1:
            if self.index==3:
                 self.video_box.setPixmap(QPixmap.fromImage(Out_img4))
                 self.video_box.setScaledContents(True)
            if self.index_2==3:
                self.video_box2.setPixmap(QPixmap.fromImage(Out_img4))
                self.video_box2.setScaledContents(True)


#--------------------------------------------------------------------------#
#--------------------------------------------------------------------------# 
    
#--------------------------------------------------------------------------#
                        #Multi-class parameters#
#--------------------------------------------------------------------------#  

    def update_camera_selection (self,Dialog,camera_index):
        self.Camera_Dropdown.setCurrentIndex(camera_index)


    def cal_widow_open (self,Dialog,camera_index):
        global cal_window

    def properties_window_A(self):
        global Bas_cap
        self.propwindow=1
        self.propWin = QtWidgets.QDialog()
        self.uiProperty = propertyWindows()
        try:
            self.uiProperty.uiProp(self.propWin)       
            self.propWin.show()
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('No cameras streaming')
            self.error_dialog.setWindowTitle("Camera stream error")
            
#--------------------------------------------------------------------------# 
#--------------------------------------------------------------------------#
            
    def calibrate_cameras (self):
        self.calibwin = QtWidgets.QDialog()
        self.uicalibration = CalibrationWindows()
        try:
            self.uicalibration.uicalib(self.calibwin)
            self.calibwin.showMaximized()
        except:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('No cameras streaming')
            self.error_dialog.setWindowTitle("Camera stream error")

    def Open_calibration_files(self):#-----------------------------------------------------# open camera calibrations button
        self.camcal1=0
        self.camcal2=0
        self.camcal3=0
        self.camcal4=0
        self.camcal5=0
        self.camcal6=0
        self.camcal7=0
        self.camcal8=0
        filter="NPZ(*.npz);;"
        filename=QFileDialog()
        filename.setFileMode(QFileDialog.ExistingFiles)
        self.Saved_Calibration_files = filename.getOpenFileNames(self,'Open file','./Calibrations',filter)
        for i in range(len(self.Saved_Calibration_files[0][:])):
            if i==0:
                self.calfile1=self.Saved_Calibration_files[0][i]
                self.calfile1_loaded=np.load(self.calfile1)
                self.camera1_matrix=self.calfile1_loaded['mtx']
                self.camera1_coeffs=self.calfile1_loaded['dist']
                self.camcal1=1
            if i==1:
                self.calfile2=self.Saved_Calibration_files[0][i]
                self.calfile2_loaded=np.load(self.calfile2)
                self.camera2_matrix=self.calfile2_loaded['mtx']
                self.camera2_coeffs=self.calfile2_loaded['dist']
                self.camcal2=1
            if i==2:
                self.calfile3=self.Saved_Calibration_files[0][i]
                self.calfile3_loaded=np.load(self.calfile3)
                self.camera3_matrix=self.calfile3_loaded['mtx']
                self.camera3_coeffs=self.calfile3_loaded['dist']
                self.camcal3=1
            if i==3:
                self.calfile4=self.Saved_Calibration_files[0][i]
                self.calfile4_loaded=np.load(self.calfile4)
                self.camera4_matrix=self.calfile4_loaded['mtx']
                self.camera4_coeffs=self.calfile4_loaded['dist']
                self.camcal4=1
            if i==4:
                self.calfile5=self.Saved_Calibration_files[0][i]
                self.calfile5_loaded=np.load(self.calfile5)
                self.camera5_matrix=self.calfile5_loaded['mtx']
                self.camera5_coeffs=self.calfile5_loaded['dist']
                self.camcal5=1
            if i==5:
                self.calfile6=self.Saved_Calibration_files[0][i]
                self.calfile6_loaded=np.load(self.calfile6)
                self.camera6_matrix=self.calfile6_loaded['mtx']
                self.camera6_coeffs=self.calfile6_loaded['dist']
                self.camcal6=1
            if i==6:
                self.calfile7=self.Saved_Calibration_files[0][i]
                self.calfile7_loaded=np.load(self.calfile7)
                self.camera7_matrix=self.calfile7_loaded['mtx']
                self.camera7_coeffs=self.calfile7_loaded['dist']
                self.camcal7=1
            if i==7:
                self.calfile8=self.Saved_Calibration_files[0][i]
                self.calfile8_loaded=np.load(self.calfile8)
                self.camera8_matrix=self.calfile8_loaded['mtx']
                self.camera8_coeffs=self.calfile8_loaded['dist']
                self.camcal8=1

        
    def window_close(self):
        Dialog.close()
#--------------------------------------------------------------------------#        
#--------------------------------------------------------------------------# 

        
#--------------------------------------------------------------------------#        
                            #Calibration Window#
#--------------------------------------------------------------------------#         
class CalibrationWindows(QMainWindow):
    def uicalib(self, calibwin):
        global Bas_cap
        global Bas_cap2
        global Bas_cap3
        global Bas_cap4
        global Bas_cap5
        global Bas_cap6
        global Bas_cap7
        global Bas_cap8
        global cal_window
        self.calibwindow=calibwin
        calibwin.setObjectName("calibwin")
        self.camera_calibindex=0
        self.cameracalstart=0
        cal_window=1
        ui.cal_widow_open(Dialog, cal_window)
        self.calibwindowInit=0
        
        width = calibwin.frameGeometry().width()
        height = calibwin.frameGeometry().height()
        calibwin.setStyleSheet("background-color: rgb(36, 36, 36);")
        calibwidget_width= width-310
        calibwidget_height= height-200

        calib_widthstart=width+50
        calib_widthstop=width+150

        textbox_height=calibwidget_height-225

        
        self.toolbarcalib = QToolBar(calibwin)
        self.toolbarcalib.setIconSize(QSize(40, 40))
        self.toolbarcalib.setOrientation(QtCore.Qt.Horizontal)

        exit_actioncalib = QAction(QIcon('images/exit.png'),'Exit', self)
        self.toolbarcalib.addAction(exit_actioncalib)
        exit_actioncalib.triggered.connect(self.window_closecalib)
        
        open_actioncalib = QAction(QIcon('images/opencalib.png'),'Open Calibration', self)
        self.toolbarcalib.addAction(open_actioncalib)
        open_actioncalib.triggered.connect(self.Open_calibration)


        self.toolbarcalib.addSeparator()
        self.toolbarcalib.addSeparator()
        self.toolbarcalib.addSeparator()

        calibrate_actionssetsave = QAction(QIcon('images/savelocation.png'),'Set Save Location', self)
        self.toolbarcalib.addAction(calibrate_actionssetsave)
        calibrate_actionssetsave.triggered.connect(self.SetSaveLocation)
        
        
        calibrate_actionsplay = QAction(QIcon('images/play.png'),'Play Calibration', self)
        self.toolbarcalib.addAction(calibrate_actionsplay)
     #   calibrate_actionsave.triggered.connect(self.calibrate_cameras)
     
        calibrate_actionstart = QAction(QIcon('images/startcalib.png'),'Start Calibration', self)
        self.toolbarcalib.addAction(calibrate_actionstart)
        calibrate_actionstart.triggered.connect(self.Start_calibrate_cameras)
     
        calibrate_actionstop = QAction(QIcon('images/stopcalib.png'),'Stop Calibration', self)
        self.toolbarcalib.addAction(calibrate_actionstop)
        calibrate_actionstop.triggered.connect(self.Stop_calibrate_cameras)

        calibrate_actioncancel = QAction(QIcon('images/cancel.png'),'Cancel Calibration', self)
        self.toolbarcalib.addAction(calibrate_actioncancel)
        calibrate_actioncancel.triggered.connect(self.cancel_calibrate_cameras)
  
        calibrate_actionsave = QAction(QIcon('images/save.png'),'Save Calibration', self)
        self.toolbarcalib.addAction(calibrate_actionsave)
     #   calibrate_actionsave.triggered.connect(self.calibrate_cameras)

        self.CheckerImage_pixmap = QPixmap('images/checker1.png')
        self.checkerlabel = QLabel(calibwin)
        self.CheckerImage_pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio)
        self.checkerlabel.setPixmap(self.CheckerImage_pixmap)
        self.checkerlabel.setGeometry(QtCore.QRect(width+330, height-475, 40, 40))

        self.circleImage_pixmap = QPixmap('images/circle1.png')
        self.checkercirclelabel = QLabel(calibwin)
        self.circleImage_pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio)
        self.checkercirclelabel.setPixmap(self.circleImage_pixmap)
        self.checkercirclelabel.setGeometry(QtCore.QRect(width+535, height-475, 40, 40))

        self.video_boxcalib1 =  QtWidgets.QLabel(calibwin)
        self.video_boxcalib1.setGeometry(QtCore.QRect(10, 50, calibwidget_width, calibwidget_height))
        boxwidth=self.video_boxcalib1.frameGeometry().width()
        boxheight=self.video_boxcalib1.frameGeometry().height()
        self.video_boxcalib1.setStyleSheet("background-color: rgb(0, 0, 0);border: 1px solid black;")
        self.video_boxcalib1.setObjectName("vid_boxcalib_1")

        self.calibTextbox_1=QPlainTextEdit(calibwin)
        self.calibTextbox_1.setGeometry(QtCore.QRect(10, 329, calibwidget_width, textbox_height))
        self.calibTextbox_1.setStyleSheet("background-color: rgb(220, 220, 220); border: 1px solid black;")
        self.calibTextbox_1.setObjectName("calibTextbox_1")
        self.calibTextbox_1.setPlainText("Calibration Images: 0/200              RMS:")
        self.calibTextbox_1.appendPlainText("Cx:              Fx:")
        self.calibTextbox_1.appendPlainText("Cy:              Fy:")
        self.calibTextbox_1.setReadOnly(True)

        self.video_boxcalib2 =  QtWidgets.QLabel(calibwin)
        self.video_boxcalib2.setGeometry(QtCore.QRect(350, 50, calibwidget_width, calibwidget_height))
        boxwidth2=self.video_boxcalib2.frameGeometry().width()
        boxheight2=self.video_boxcalib2.frameGeometry().height()
        self.video_boxcalib2.setStyleSheet("background-color: rgb(0, 0, 0);border: 1px solid black;")
        self.video_boxcalib2.setObjectName("vid_boxcalib_2")

        self.calibTextbox_2=QPlainTextEdit(calibwin)
        self.calibTextbox_2.setGeometry(QtCore.QRect(350, 329, calibwidget_width, textbox_height))
        self.calibTextbox_2.setStyleSheet("background-color: rgb(220, 220, 220); border: 1px solid black;")
        self.calibTextbox_2.setObjectName("calibTextbox_2")
        self.calibTextbox_2.setPlainText("Calibration Images: 0/200              RMS:")
        self.calibTextbox_2.appendPlainText("Cx:              Fx:")
        self.calibTextbox_2.appendPlainText("Cy:              Fy:")
        self.calibTextbox_2.setReadOnly(True)

        self.video_boxcalib3 =  QtWidgets.QLabel(calibwin)
        self.video_boxcalib3.setGeometry(QtCore.QRect(690, 50, calibwidget_width, calibwidget_height))
        boxwidth3=self.video_boxcalib3.frameGeometry().width()
        boxheight3=self.video_boxcalib3.frameGeometry().height()
        self.video_boxcalib3.setStyleSheet("background-color: rgb(0, 0, 0);border: 1px solid black;")
        self.video_boxcalib3.setObjectName("vid_boxcalib_3")

        self.calibTextbox_3=QPlainTextEdit(calibwin)
        self.calibTextbox_3.setGeometry(QtCore.QRect(690, 329, calibwidget_width, textbox_height))
        self.calibTextbox_3.setStyleSheet("background-color: rgb(220, 220, 220); border: 1px solid black;")
        self.calibTextbox_3.setObjectName("calibTextbox_3")
        self.calibTextbox_3.setPlainText("Calibration Images: 0/200              RMS:")
        self.calibTextbox_3.appendPlainText("Cx:              Fx:")
        self.calibTextbox_3.appendPlainText("Cy:              Fy:")
        self.calibTextbox_3.setReadOnly(True)
        
        self.video_boxcalib4 =  QtWidgets.QLabel(calibwin)
        self.video_boxcalib4.setGeometry(QtCore.QRect(1030, 50, calibwidget_width, calibwidget_height))
        boxwidth4=self.video_boxcalib4.frameGeometry().width()
        boxheight4=self.video_boxcalib4.frameGeometry().height()
        self.video_boxcalib4.setStyleSheet("background-color: rgb(0, 0, 0);border: 1px solid black;")
        self.video_boxcalib4.setObjectName("vid_boxcalib_4")

        self.calibTextbox_4=QPlainTextEdit(calibwin)
        self.calibTextbox_4.setGeometry(QtCore.QRect(1030, 329, calibwidget_width, textbox_height))
        self.calibTextbox_4.setStyleSheet("background-color: rgb(220, 220, 220); border: 1px solid black;")
        self.calibTextbox_4.setObjectName("calibTextbox_4")
        self.calibTextbox_4.setPlainText("Calibration Images: 0/200              RMS:")
        self.calibTextbox_4.appendPlainText("Cx:              Fx:")
        self.calibTextbox_4.appendPlainText("Cy:              Fy:")
        self.calibTextbox_4.setReadOnly(True)

        self.video_boxcalib5 =  QtWidgets.QLabel(calibwin)
        self.video_boxcalib5.setGeometry(QtCore.QRect(10, 400, calibwidget_width, calibwidget_height))
        boxwidth5=self.video_boxcalib5.frameGeometry().width()
        boxheight5=self.video_boxcalib5.frameGeometry().height()
        self.video_boxcalib5.setStyleSheet("background-color: rgb(0, 0, 0);border: 1px solid black;")
        self.video_boxcalib5.setObjectName("vid_boxcalib_5")

        self.calibTextbox_5=QPlainTextEdit(calibwin)
        self.calibTextbox_5.setGeometry(QtCore.QRect(10, 679, calibwidget_width, textbox_height))
        self.calibTextbox_5.setStyleSheet("background-color: rgb(220, 220, 220); border: 1px solid black;")
        self.calibTextbox_5.setObjectName("calibTextbox_5")
        self.calibTextbox_5.setPlainText("Calibration Images: 0/200              RMS:")
        self.calibTextbox_5.appendPlainText("Cx:              Fx:")
        self.calibTextbox_5.appendPlainText("Cy:              Fy:")
        self.calibTextbox_5.setReadOnly(True)

        self.video_boxcalib6 =  QtWidgets.QLabel(calibwin)
        self.video_boxcalib6.setGeometry(QtCore.QRect(350, 400, calibwidget_width, calibwidget_height))
        boxwidth6=self.video_boxcalib6.frameGeometry().width()
        boxheight6=self.video_boxcalib6.frameGeometry().height()
        self.video_boxcalib6.setStyleSheet("background-color: rgb(0, 0, 0);border: 1px solid black;")
        self.video_boxcalib6.setObjectName("vid_boxcalib_6")

        self.calibTextbox_6=QPlainTextEdit(calibwin)
        self.calibTextbox_6.setGeometry(QtCore.QRect(350, 679, calibwidget_width, textbox_height))
        self.calibTextbox_6.setStyleSheet("background-color: rgb(220, 220, 220); border: 1px solid black;")
        self.calibTextbox_6.setObjectName("calibTextbox_6")
        self.calibTextbox_6.setPlainText("Calibration Images: 0/200              RMS:")
        self.calibTextbox_6.appendPlainText("Cx:              Fx:")
        self.calibTextbox_6.appendPlainText("Cy:              Fy:")
        self.calibTextbox_6.setReadOnly(True)

        self.video_boxcalib7 =  QtWidgets.QLabel(calibwin)
        self.video_boxcalib7.setGeometry(QtCore.QRect(690, 400, calibwidget_width, calibwidget_height))
        boxwidth7=self.video_boxcalib7.frameGeometry().width()
        boxheight7=self.video_boxcalib7.frameGeometry().height()
        self.video_boxcalib7.setStyleSheet("background-color: rgb(0, 0, 0);border: 1px solid black;")
        self.video_boxcalib7.setObjectName("vid_boxcalib_7")

        self.calibTextbox_7=QPlainTextEdit(calibwin)
        self.calibTextbox_7.setGeometry(QtCore.QRect(690, 679, calibwidget_width, textbox_height))
        self.calibTextbox_7.setStyleSheet("background-color: rgb(220, 220, 220); border: 1px solid black;")
        self.calibTextbox_7.setObjectName("calibTextbox_7")
        self.calibTextbox_7.setPlainText("Calibration Images: 0/200              RMS:")
        self.calibTextbox_7.appendPlainText("Cx:              Fx:")
        self.calibTextbox_7.appendPlainText("Cy:              Fy:")
        self.calibTextbox_7.setReadOnly(True)

        self.video_boxcalib8 =  QtWidgets.QLabel(calibwin)
        self.video_boxcalib8.setGeometry(QtCore.QRect(1030, 400, calibwidget_width, calibwidget_height))
        boxwidth8=self.video_boxcalib8.frameGeometry().width()
        boxheight8=self.video_boxcalib8.frameGeometry().height()
        self.video_boxcalib8.setStyleSheet("background-color: rgb(0, 0, 0);border: 1px solid black;")
        self.video_boxcalib8.setObjectName("vid_boxcalib_8")

        self.calibTextbox_8=QPlainTextEdit(calibwin)
        self.calibTextbox_8.setGeometry(QtCore.QRect(1030, 679, calibwidget_width, textbox_height))
        self.calibTextbox_8.setStyleSheet("background-color: rgb(220, 220, 220); border: 1px solid black;")
        self.calibTextbox_8.setObjectName("calibTextbox_8")
        self.calibTextbox_8.setPlainText("Calibration Images: 0/200              RMS:")
        self.calibTextbox_8.appendPlainText("Cx:              Fx:")
        self.calibTextbox_8.appendPlainText("Cy:              Fy:")
        self.calibTextbox_8.setReadOnly(True)

        self.Camera_Dropdowncalib= QComboBox(calibwin)
        self.Camera_Dropdowncalib.setGeometry(QtCore.QRect(width-200, height-462, 130, 21))
        self.Camera_Dropdowncalib.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.Camera_Dropdowncalib.addItem("Camera 1")
        self.Camera_Dropdowncalib.addItem("Camera 2")
        self.Camera_Dropdowncalib.addItem("Camera 3")
        self.Camera_Dropdowncalib.addItem("Camera 4")
        self.Camera_Dropdowncalib.addItem("Camera 5")
        self.Camera_Dropdowncalib.addItem("Camera 6")
        self.Camera_Dropdowncalib.addItem("Camera 7")
        self.Camera_Dropdowncalib.addItem("Camera 8")

        self.radio_checker=QRadioButton(calibwin)
        self.radio_checker.setGeometry(QtCore.QRect(width+375, height-475,102,17))
        self.radio_checker.setStyleSheet("color: rgb(252, 255, 255);")
        self.radio_checker.setObjectName("radiobutton_1")

        self.squaresize = QLineEdit(calibwin)
        self.squaresize.setGeometry(QtCore.QRect(width+465, height-475, 65, 17))
        self.squaresize.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.squaresize.setObjectName("squaresize")
        #self.squaresize.setText("square(mm)")
        self.squaresize.setText("34")

        self.checker_width= QComboBox(calibwin)
        self.checker_width.setGeometry(QtCore.QRect(width+375, height-455, 55, 21))
        self.checker_width.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.checker_width.addItem("Width") #0
        self.checker_width.addItem("4")#1
        self.checker_width.addItem("5")#2
        self.checker_width.addItem("6")#3
        self.checker_width.addItem("7")#4
        self.checker_width.addItem("8")#5
        self.checker_width.addItem("9")#6
        self.checker_width.addItem("10")#7
        self.checker_width.addItem("11")#8
        self.checker_width.addItem("12")#9
        self.checker_width.addItem("13")#10
        self.checker_width.addItem("14")#11
        self.checker_width.addItem("15")#12
        self.checker_width.addItem("16")#13
        self.checker_width.addItem("17")#14
        self.checker_width.addItem("18")#15
        self.checker_width.addItem("19")#16
        self.checker_width.addItem("20")#17
        self.checker_width.setCurrentIndex(3) #temporary

        self.checker_height= QComboBox(calibwin)
        self.checker_height.setGeometry(QtCore.QRect(width+435, height-455, 55, 21))
        self.checker_height.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.checker_height.addItem("Height") #0
        self.checker_height.addItem("3")#1
        self.checker_height.addItem("4")#2
        self.checker_height.addItem("5")#3
        self.checker_height.addItem("6")#4
        self.checker_height.addItem("7")#5
        self.checker_height.addItem("8")#6
        self.checker_height.addItem("9")#7
        self.checker_height.addItem("10")#8
        self.checker_height.addItem("11")#9
        self.checker_height.addItem("12")#10
        self.checker_height.addItem("13")#11
        self.checker_height.addItem("14")#12
        self.checker_height.addItem("15")#13
        self.checker_height.addItem("16")#14
        self.checker_height.addItem("17")#15
        self.checker_height.addItem("18")#16
        self.checker_height.addItem("19")#17
        self.checker_height.setCurrentIndex(2) #temporary

        self.radio_circles=QRadioButton(calibwin)
        self.radio_circles.setGeometry(QtCore.QRect(width+580, height-475,102,17))
        self.radio_circles.setStyleSheet("color: rgb(252, 255, 255);")
        self.radio_circles.setObjectName("radiobutton_2")

        self.circlesize = QLineEdit(calibwin)
        self.circlesize.setGeometry(QtCore.QRect(width+640, height-475, 65, 17))
        self.circlesize.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.circlesize.setObjectName("circlesize")
        self.circlesize.setText("circle(mm)")

        self.circle_width= QComboBox(calibwin)
        self.circle_width.setGeometry(QtCore.QRect(width+580, height-455, 55, 21))
        self.circle_width.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.circle_width.addItem("Width") #0
        self.circle_width.addItem("4")#1
        self.circle_width.addItem("5")#2
        self.circle_width.addItem("6")#3
        self.circle_width.addItem("7")#4
        self.circle_width.addItem("8")#5
        self.circle_width.addItem("9")#6
        self.circle_width.addItem("10")#7
        self.circle_width.addItem("11")#8
        self.circle_width.addItem("12")#9
        self.circle_width.addItem("13")#10
        self.circle_width.addItem("14")#11
        self.circle_width.addItem("15")#12
        self.circle_width.addItem("16")#13
        self.circle_width.addItem("17")#14
        self.circle_width.addItem("18")#15
        self.circle_width.addItem("19")#16
        self.circle_width.addItem("20")#17

        self.circle_height= QComboBox(calibwin)
        self.circle_height.setGeometry(QtCore.QRect(width+640, height-455, 55, 21))
        self.circle_height.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.circle_height.addItem("Height") #0
        self.circle_height.addItem("3")#1
        self.circle_height.addItem("4")#2
        self.circle_height.addItem("5")#3
        self.circle_height.addItem("6")#4
        self.circle_height.addItem("7")#5
        self.circle_height.addItem("8")#6
        self.circle_height.addItem("9")#7
        self.circle_height.addItem("10")#8
        self.circle_height.addItem("11")#9
        self.circle_height.addItem("12")#10
        self.circle_height.addItem("13")#11
        self.circle_height.addItem("14")#12
        self.circle_height.addItem("15")#13
        self.circle_height.addItem("16")#14
        self.circle_height.addItem("17")#15
        self.circle_height.addItem("18")#16
        self.circle_height.addItem("19")#17
        

        self.retranslateUicalib(calibwin)
        QtCore.QMetaObject.connectSlotsByName(calibwin)

        self.calibwindowInit=1
        
        

    def retranslateUicalib(self, calibwin):
        _translate = QtCore.QCoreApplication.translate  
        calibwin.setWindowTitle(_translate("calibwin", "Camera Calibration"))
        self.radio_checker.setText(_translate("calibwin", "Checkerboard"))
        self.radio_circles.setText(_translate("calibwin", "Circles"))
        
    def Open_calibration(self):
     self.Calibration_file= QFileDialog.getOpenFileName(self,'Open file','./',filter="All Files(*.*);;Text Files(*.txt)")
     time.sleep(0.01)
     try:
        if len(self.Calibration_file[0])==0:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('No calibration file loaded')
            self.error_dialog.setWindowTitle("Calibration file error")
        else:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('calibration file loaded')
            self.error_dialog.setWindowTitle("Calibration")
     except OSError:
         self.error_dialog = QtWidgets.QErrorMessage()
         self.error_dialog.showMessage('No calibration file loaded')
         self.error_dialog.setWindowTitle("Calibration file error")

    def SetSaveLocation(self):
        self.saveLocation = QFileDialog.getExistingDirectory(self, "Select Directory")
        time.sleep(0.01)
        try:
            if len(self.saveLocation)==0:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.showMessage('No calibration location set')
                self.error_dialog.setWindowTitle("Calibration save error")
            else:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.showMessage('calibration location Set')
                self.error_dialog.setWindowTitle("Calibration Location")
        except OSError:
             self.error_dialog = QtWidgets.QErrorMessage()
             self.error_dialog.showMessage('No calibration location set')
             self.error_dialog.setWindowTitle("Calibration save error")
             

#--------------------------------------------------------------------------#
                        #Camera image manipulation#
#--------------------------------------------------------------------------#
    def displayImagecalibb1(self,calibwin,img,window=1): #-----------------------------------------------------# Stream basler 1 manipulation
        retb1=[]
        mtx=[]
        rvecs=[]
        tvecs=[]
        h=[]
        w=[]
        roi=[]
        h=[]
        w=[]
        corners1=[]
        corners2=[]
        circles1=[]
        mapx=[]
        mapy=[]
        
        h,  w = img.shape[:2]      
        
        if self.cameracalstart==1:
            if self.camera_calibindex==2:
                # Find the chess board corners
               # imgb1=cv2.cvtColor(imgb1,cv2.COLOR_BGR2GRAY)
                if self.checkerboard==1:
                    retb1, corners1 = cv2.findChessboardCorners(img, (self.board_width,self.board_height))#,flags=CALIB_CB_FAST_CHECK)
                elif self.circleboard==1:
                    retb1, circles1 = cv2.findCirclesGrid(img, (self.board_width,self.board_height))
                        
                if retb1 == True:
                    self.calibimages=self.calibimages+1
                    self.calibimagesstr=str(self.calibimages)
                    self.objpoints.append(self.objp)
                    if self.checkerboard==1:
                        corners2 = cv2.cornerSubPix(img,corners1,(11,11),(-1,-1),self.criteria)
                        self.imgpoints.append(corners2)
                        img = cv2.drawChessboardCorners(img, (self.board_width,self.board_height),corners2,retb1)
                    elif self.circleboard==1:
                        self.imgpoints.append(circles1)
                        img = cv2.drawChessboardCorners(img, (self.board_width,self.board_height),circles1,retb1)
                    #camera matrix, distortion coefficients, rotation and translation vectors
                    rms, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints,img.shape[::-1],None,None)# img.shape[::-1],None,None)

                    self.rmsb1=str(round(rms,2))
                    self.cxb1_temp2=self.cxb1_temp2 + mtx[0][2]
                    self.cyb1_temp2=self.cyb1_temp2 + mtx[1][2]
                    self.fxb1_temp2=self.fxb1_temp2 + mtx[0][0]
                    self.fyb1_temp2=self.fyb1_temp2 + mtx[1][1]

                    self.rmsb1_temp=self.rmsb1_temp +rms
                    self.mtxb1_temp=self.mtxb1_temp + mtx
                    self.distb1_temp=self.distb1_temp + dist
                    self.rvecsb1_temp=self.rvecsb1_temp + rvecs 
                    self.tvecsb1_temp=self.tvecsb1_temp + tvecs
                    
                    self.objpoints=[]
                    self.imgpoints=[]


                    
        # conversion of cam 1 into pyqt widget 
        qformatb1=QImage.Format_Indexed8
        if (len(img.shape))==3: #[0]=rows,[1]=cols,[2]=channels
            if img.shape[2]==4:
                qformatb1=QImage.Format_RGBA8888
            else:
                qformatb1=QImage.Format_RGB888
        Out_img=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformatb1)  
       # Out_Imgb1=Out_imgb1.rgbSwapped() #BGR>>RGB
        
        if self.calibwindowInit==1:
            if cal_window==1:
                if window==1:
                         self.video_boxcalib1.setPixmap(QPixmap.fromImage(Out_img))
                         self.video_boxcalib1.setScaledContents(True)

    def displayImagecalibb2(self,calibwin,img2,window=1): #-----------------------------------------------------# Stream basler 2 manipulation
        retb2=[]
        mtx=[]
        rvecs=[]
        tvecs=[]
        h=[]
        w=[]
        roi=[]
        h=[]
        w=[]
        corners3=[]
        corners4=[]
        circles3=[]
        mapx=[]
        mapy=[]
        
        h,  w = img2.shape[:2]      
        
        if self.cameracalstart==1:
            if self.camera_calibindex==2:
                # Find the chess board corners
               # img2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
                if self.checkerboard==1:
                    retb2, corners3 = cv2.findChessboardCorners(img2, (self.board_width,self.board_height))#,flags=CALIB_CB_FAST_CHECK)
                elif self.circleboard==1:
                    retb2, circles3 = cv2.findCirclesGrid(img2, (self.board_width,self.board_height))
                        
                if retb2 == True:
                    self.calibimages=self.calibimages+1
                    self.calibimagesstr=str(self.calibimages)
                    self.objpoints.append(self.objp)
                    if self.checkerboard==1:
                        corners4 = cv2.cornerSubPix(img2,corners3,(11,11),(-1,-1),self.criteria)
                        self.imgpoints.append(corners4)
                        img2 = cv2.drawChessboardCorners(img2, (self.board_width,self.board_height),corners4,retb2)
                    elif self.circleboard==1:
                        self.imgpoints.append(circles3)
                        img2 = cv2.drawChessboardCorners(img2, (self.board_width,self.board_height),circles3,retb2)
                    #camera matrix, distortion coefficients, rotation and translation vectors
                    rms, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints,img2.shape[::-1],None,None)# img.shape[::-1],None,None)

                    self.rmsb2=str(round(rms,2))
                    self.cxb2_temp2=self.cxb2_temp2 + mtx[0][2]
                    self.cyb2_temp2=self.cyb2_temp2 + mtx[1][2]
                    self.fxb2_temp2=self.fxb2_temp2 + mtx[0][0]
                    self.fyb2_temp2=self.fyb2_temp2 + mtx[1][1]

                    self.rmsb2_temp=self.rmsb2_temp +rms
                    self.mtxb2_temp=self.mtxb2_temp + mtx
                    self.distb2_temp=self.distb2_temp + dist
                    self.rvecsb2_temp=self.rvecsb2_temp + rvecs 
                    self.tvecsb2_temp=self.tvecsb2_temp + tvecs
                    
                    self.objpoints=[]
                    self.imgpoints=[]


                    
        # conversion of cam 1 into pyqt widget 
        qformatb2=QImage.Format_Indexed8
        if (len(img2.shape))==3: #[0]=rows,[1]=cols,[2]=channels
            if img2.shape[2]==4:
                qformatb2=QImage.Format_RGBA8888
            else:
                qformatb2=QImage.Format_RGB888
        Out_img2=QImage(img2,img2.shape[1],img2.shape[0],img2.strides[0],qformatb2)  
       # Out_img2=Out_img2.rgbSwapped() #BGR>>RGB
        
        if self.calibwindowInit==1:
            if cal_window==1:
                if window==1:
                         self.video_boxcalib2.setPixmap(QPixmap.fromImage(Out_img2))
                         self.video_boxcalib2.setScaledContents(True)

    def displayImagecalibb3(self,calibwin,img3,window=1): #-----------------------------------------------------# Stream basler 3 manipulation
        retb3=[]
        mtx=[]
        rvecs=[]
        tvecs=[]
        h=[]
        w=[]
        roi=[]
        h=[]
        w=[]
        corners5=[]
        corners6=[]
        circles5=[]
        mapx=[]
        mapy=[]
        
        h,  w = img3.shape[:2]      
        
        if self.cameracalstart==1:
            if self.camera_calibindex==2:
                # Find the chess board corners
               # img2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
                if self.checkerboard==1:
                    retb3, corners5 = cv2.findChessboardCorners(img3, (self.board_width,self.board_height))#,flags=CALIB_CB_FAST_CHECK)
                elif self.circleboard==1:
                    retb3, circles5 = cv2.findCirclesGrid(img3, (self.board_width,self.board_height))
                        
                if retb3 == True:
                    self.calibimages=self.calibimages+1
                    self.calibimagesstr=str(self.calibimages)
                    self.objpoints.append(self.objp)
                    if self.checkerboard==1:
                        corners6 = cv2.cornerSubPix(img3,corners5,(11,11),(-1,-1),self.criteria)
                        self.imgpoints.append(corners6)
                        img3 = cv2.drawChessboardCorners(img3, (self.board_width,self.board_height),corners6,retb3)
                    elif self.circleboard==1:
                        self.imgpoints.append(circles5)
                        img3 = cv2.drawChessboardCorners(img3, (self.board_width,self.board_height),circles5,retb3)
                    #camera matrix, distortion coefficients, rotation and translation vectors
                    rms, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints,img3.shape[::-1],None,None)# img.shape[::-1],None,None)

                    self.rmsb2=str(round(rms,2))
                    self.cxb3_temp2=self.cxb3_temp2 + mtx[0][2]
                    self.cyb3_temp2=self.cyb3_temp2 + mtx[1][2]
                    self.fxb3_temp2=self.fxb3_temp2 + mtx[0][0]
                    self.fyb3_temp2=self.fyb3_temp2 + mtx[1][1]

                    self.rmsb3_temp=self.rmsb3_temp +rms
                    self.mtxb3_temp=self.mtxb3_temp + mtx
                    self.distb3_temp=self.distb3_temp + dist
                    self.rvecsb3_temp=self.rvecsb3_temp + rvecs 
                    self.tvecsb3_temp=self.tvecsb3_temp + tvecs
                    
                    self.objpoints=[]
                    self.imgpoints=[]


                    
        # conversion of cam 1 into pyqt widget 
        qformatb3=QImage.Format_Indexed8
        if (len(img3.shape))==3: #[0]=rows,[1]=cols,[2]=channels
            if img3.shape[2]==4:
                qformatb2=QImage.Format_RGBA8888
            else:
                qformatb2=QImage.Format_RGB888
        Out_img3=QImage(img3,img3.shape[1],img3.shape[0],img3.strides[0],qformatb3)  
       # Out_img3=Out_img3.rgbSwapped() #BGR>>RGB
        
        if self.calibwindowInit==1:
            if cal_window==1:
                if window==1:
                         self.video_boxcalib3.setPixmap(QPixmap.fromImage(Out_img3))
                         self.video_boxcalib3.setScaledContents(True)

    def displayImagecalibb4(self,calibwin,img4,window=1): #-----------------------------------------------------# Stream basler 3 manipulation
        retb4=[]
        mtx=[]
        rvecs=[]
        tvecs=[]
        h=[]
        w=[]
        roi=[]
        h=[]
        w=[]
        corners7=[]
        corners8=[]
        circles8=[]
        mapx=[]
        mapy=[]
        
        h,  w = img4.shape[:2]      
        
        if self.cameracalstart==1:
            if self.camera_calibindex==2:
                # Find the chess board corners
               # img2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
                if self.checkerboard==1:
                    retb4, corners7 = cv2.findChessboardCorners(img4, (self.board_width,self.board_height))#,flags=CALIB_CB_FAST_CHECK)
                elif self.circleboard==1:
                    retb4, circles7 = cv2.findCirclesGrid(img4, (self.board_width,self.board_height))
                        
                if retb4 == True:
                    self.calibimages=self.calibimages+1
                    self.calibimagesstr=str(self.calibimages)
                    self.objpoints.append(self.objp)
                    if self.checkerboard==1:
                        corners8 = cv2.cornerSubPix(img4,corners7,(11,11),(-1,-1),self.criteria)
                        self.imgpoints.append(corners8)
                        img4 = cv2.drawChessboardCorners(img4, (self.board_width,self.board_height),corners8,retb4)
                    elif self.circleboard==1:
                        self.imgpoints.append(circles7)
                        img4 = cv2.drawChessboardCorners(img4, (self.board_width,self.board_height),circles7,retb4)
                    #camera matrix, distortion coefficients, rotation and translation vectors
                    rms, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints,img4.shape[::-1],None,None)# img.shape[::-1],None,None)

                    self.rmsb4=str(round(rms,2))
                    self.cxb4_temp2=self.cxb4_temp2 + mtx[0][2]
                    self.cyb4_temp2=self.cyb4_temp2 + mtx[1][2]
                    self.fxb4_temp2=self.fxb4_temp2 + mtx[0][0]
                    self.fyb4_temp2=self.fyb4_temp2 + mtx[1][1]

                    self.rmsb4_temp=self.rmsb4_temp +rms
                    self.mtxb4_temp=self.mtxb4_temp + mtx
                    self.distb4_temp=self.distb4_temp + dist
                    self.rvecsb4_temp=self.rvecsb4_temp + rvecs 
                    self.tvecsb4_temp=self.tvecsb4_temp + tvecs
                    
                    self.objpoints=[]
                    self.imgpoints=[]


                    
        # conversion of cam 1 into pyqt widget 
        qformatb4=QImage.Format_Indexed8
        if (len(img4.shape))==3: #[0]=rows,[1]=cols,[2]=channels
            if img4.shape[2]==4:
                qformatb4=QImage.Format_RGBA8888
            else:
                qformatb4=QImage.Format_RGB888
        Out_img4=QImage(img4,img4.shape[1],img4.shape[0],img4.strides[0],qformatb4)  
       # Out_img3=Out_img3.rgbSwapped() #BGR>>RGB
        
        if self.calibwindowInit==1:
            if cal_window==1:
                if window==1:
                         self.video_boxcalib4.setPixmap(QPixmap.fromImage(Out_img4))
                         self.video_boxcalib4.setScaledContents(True)
                                                               
#--------------------------------------------------------------------------#
#--------------------------------------------------------------------------#
                     

                 
    def Start_calibrate_cameras(self):
#---------------------------------------------#
        self.cxb1_temp2=0
        self.cyb1_temp2=0
        self.fxb1_temp2=0
        self.fyb1_temp2=0

        self.rmsb1_temp=0
        self.mtxb1_temp=np.zeros((3,3))
        self.distb1_temp=np.zeros(5)
        self.rvecsb1_temp=np.zeros((3,1))
        self.tvecsb1_temp=np.zeros((3,1))
#---------------------------------------------#
        self.cxb2_temp2=0
        self.cyb2_temp2=0
        self.fxb2_temp2=0
        self.fyb2_temp2=0

        self.rmsb2_temp=0
        self.mtxb2_temp=np.zeros((3,3))
        self.distb2_temp=np.zeros(5)
        self.rvecsb2_temp=np.zeros((3,1))
        self.tvecsb2_temp=np.zeros((3,1))
       
#---------------------------------------------#
        self.cxb3_temp2=0
        self.cyb3_temp2=0
        self.fxb3_temp2=0
        self.fyb3_temp2=0

        self.rmsb3_temp=0
        self.mtxb3_temp=np.zeros((3,3))
        self.distb3_temp=np.zeros(5)
        self.rvecsb3_temp=np.zeros((3,1))
        self.tvecsb3_temp=np.zeros((3,1))
#---------------------------------------------#
        self.cxb4_temp2=0
        self.cyb4_temp2=0
        self.fxb4_temp2=0
        self.fyb4_temp2=0

        self.rmsb4_temp=0
        self.mtxb4_temp=np.zeros((3,3))
        self.distb4_temp=np.zeros(5)
        self.rvecsb4_temp=np.zeros((3,1))
        self.tvecsb4_temp=np.zeros((3,1))
#---------------------------------------------#

        
        self.calibimages=0
        self.board_width=0
        self.board_height=0
        self.cancel_calibration=0
        
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        if self.radio_checker.isChecked():
            self.checkerboard=1
            self.circleboard=0
            self.board_width=int(self.checker_width.currentText())
            self.board_height=int(self.checker_height.currentText())
            self.squaresize_int=int(self.squaresize.text()) # add a try and except
            self.objp = np.zeros((self.board_height*self.board_width,3), np.float32)
            self.objp[:,:2] = np.mgrid[0:self.board_width,0:self.board_height].T.reshape(-1,2)*self.squaresize_int
            self.objpoints = [] # 3d point in real world space
            self.imgpoints = [] # 2d points in image plane.
            self.camera_calibindex = self.Camera_Dropdowncalib.currentIndex()
            self.cameracalstart=1

        elif self.radio_circles.isChecked():
            self.checkerboard=0
            self.circleboard=1
            self.board_width=int(self.circle_width.currentText())
            self.board_height=int(self.circle_height.currentText())
            self.circlesize_int=int(self.circlesize.text())
            self.objp = np.zeros((self.board_height*self.board_width,3), np.float32)
            self.objp[:,:2] = np.mgrid[0:self.board_width,0:self.board_height].T.reshape(-1,2)*self.circlesize_int
            self.objpoints = [] # 3d point in real world space
            self.imgpoints = [] # 2d points in image plane.
            self.camera_calibindex = self.Camera_Dropdowncalib.currentIndex()
            self.cameracalstart=1
            
        else:
             self.error_dialog = QtWidgets.QErrorMessage()
             self.error_dialog.showMessage('Please set calibration board')
             self.error_dialog.setWindowTitle("Calibration error")
            
    def Stop_calibrate_cameras(self):
        self.cameracalstart=0
        if self.cancel_calibration==0:
            if self.camera_calibindex==0:
                try:
                    self.cxb1=str(round(self.cxb1_temp2/self.calibimages,2))
                    self.cyb1=str(round(self.cyb1_temp2/self.calibimages,2))
                    self.fxb1=str(round(self.fxb1_temp2/self.calibimages,2))
                    self.fyb1=str(round(self.fyb1_temp2/self.calibimages,2))
                    self.calibTextbox_1.setPlainText("Calibration Images:"+self.calibimagesstr+"/200              RMS:"+self.rmsb1)
                    self.calibTextbox_1.appendPlainText("Cx:"+self.cxb1+"             Fx:"+self.fxb1)
                    self.calibTextbox_1.appendPlainText("Cy:"+self.cyb1+"             Fy:"+self.fyb1)
                   
                    rms=round(self.rmsb1_temp/self.calibimages,2)
                    mtxb1_=self.mtxb1_temp/(self.calibimages)
                    mtx=np.around(mtxb1_,decimals=2)
                    
                    distb1_=self.distb1_temp/(self.calibimages)
                    dist=np.around(distb1_,decimals=2)
                    
                    rvecsb1_=self.rvecsb1_temp/(self.calibimages)
                    rvecs=np.around(rvecsb1_,decimals=2)
                    
                    tvecsb1_=self.tvecsb1_temp/(self.calibimages)
                    tvecs=np.around(tvecsb1_,decimals=2)

                    currenttime=str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
                    fname =  self.saveLocation+"/"+currenttime+"_"+"camera1_calibration" ###add in serial number
                    np.savez(fname, mtx=mtx, dist=dist)
                except:
                    pass

            if self.camera_calibindex==1:
                try:
                    self.cxb2=str(round(self.cxb2_temp2/self.calibimages,2))
                    self.cyb2=str(round(self.cyb2_temp2/self.calibimages,2))
                    self.fxb2=str(round(self.fxb2_temp2/self.calibimages,2))
                    self.fyb2=str(round(self.fyb2_temp2/self.calibimages,2))
                    self.calibTextbox_2.setPlainText("Calibration Images:"+self.calibimagesstr+"/200              RMS:"+self.rmsb2)
                    self.calibTextbox_2.appendPlainText("Cx:"+self.cxb2+"             Fx:"+self.fxb2)
                    self.calibTextbox_2.appendPlainText("Cy:"+self.cyb2+"             Fy:"+self.fyb2)

                    rms=round(self.rmsb2_temp/self.calibimages,2)
                    mtxb2_=self.mtxb2_temp/(self.calibimages)
                    mtx=np.around(mtxb2_,decimals=2)
                    
                    distb2_=self.distb2_temp/(self.calibimages)
                    dist=np.around(distb2_,decimals=2)
                    
                    rvecsb2_=self.rvecsb2_temp/(self.calibimages)
                    rvecs=np.around(rvecsb2_,decimals=2)
                    
                    tvecsb2_=self.tvecsb2_temp/(self.calibimages)
                    tvecs=np.around(tvecsb2_,decimals=2)

                    currenttime=str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
                    fname =  self.saveLocation+"/"+currenttime+"_"+"camera2_calibration"
                    np.savez(fname, mtx=mtx, dist=dist)
                    
                except:
                    pass
            if self.camera_calibindex==2:
                try:
                    self.cx3=str(round(self.cx3_temp2/self.calibimages,2))
                    self.cy3=str(round(self.cy3_temp2/self.calibimages,2))
                    self.fx3=str(round(self.fx3_temp2/self.calibimages,2))
                    self.fy3=str(round(self.fy3_temp2/self.calibimages,2))
                    self.calibTextbox_3.setPlainText("Calibration Images:"+self.calibimagesstr+"/200              RMS:"+self.rms3)
                    self.calibTextbox_3.appendPlainText("Cx:"+self.cx3+"             Fx:"+self.fx3)
                    self.calibTextbox_3.appendPlainText("Cy:"+self.cy3+"             Fy:"+self.fy3)

                    rms=round(self.rms3_temp/self.calibimages,2)
                    mtx3_=self.mtx3_temp/(self.calibimages)
                    mtx=np.around(mtx3_,decimals=2)
                    
                    dist3_=self.dist3_temp/(self.calibimages)
                    dist=np.around(dist3_,decimals=2)
                    
                    rvecs3_=self.rvecs3_temp/(self.calibimages)
                    rvecs=np.around(rvecs3_,decimals=2)
                    
                    tvecs3_=self.tvecs3_temp/(self.calibimages)
                    tvecs=np.around(tvecs3_,decimals=2)

                    currenttime=str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
                    fname =  self.saveLocation+"/"+currenttime+"_"+"camera3_calibration"
                    np.savez(fname, mtx=mtx, dist=dist)
                    
                except:
                    pass
            if self.camera_calibindex==3:
                try:
                    self.cx4=str(round(self.cx4_temp2/self.calibimages,2))
                    self.cy4=str(round(self.cy4_temp2/self.calibimages,2))
                    self.fx4=str(round(self.fx4_temp2/self.calibimages,2))
                    self.fy4=str(round(self.fy4_temp2/self.calibimages,2))
                    self.calibTextbox_4.setPlainText("Calibration Images:"+self.calibimagesstr+"/200              RMS:"+self.rms4)
                    self.calibTextbox_4.appendPlainText("Cx:"+self.cx4+"             Fx:"+self.fx4)
                    self.calibTextbox_4.appendPlainText("Cy:"+self.cy4+"             Fy:"+self.fy4)

                    rms=round(self.rms4_temp/self.calibimages,2)
                    mtx4_=self.mtx4_temp/(self.calibimages)
                    mtx=np.around(mtx4_,decimals=2)
                    
                    dist4_=self.dist4_temp/(self.calibimages)
                    dist=np.around(dist4_,decimals=2)
                    
                    rvecs4_=self.rvecs4_temp/(self.calibimages)
                    rvecs=np.around(rvecs4_,decimals=2)
                    
                    tvecs4_=self.tvecs4_temp/(self.calibimages)
                    tvecs=np.around(tvecs4_,decimals=2)

                    currenttime=str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
                    fname =  self.saveLocation+"/"+currenttime+"_"+"camera4_calibration"
                    np.savez(fname, mtx=mtx, dist=dist)
                    
                except:
                    pass
    
        self.calibimages=0

    def cancel_calibrate_cameras(self):
        self.cancel_calibration=1
        self.Stop_calibrate_cameras()
        
    def window_closecalib(self):
        global cal_window
        cal_window=0
        self.calibwindow.close()
#--------------------------------------------------------------------------#        
#--------------------------------------------------------------------------#
        
#--------------------------------------------------------------------------#        
                            #Properties Window#
#--------------------------------------------------------------------------#         

class propertyWindows(QMainWindow):
    def uiProp(self, propWin):
        global Bas_cap
        global Bas_cap2
        global Bas_cap3
        global Bas_cap4
        global Bas_cap5
        global Bas_cap6
        global Bas_cap7
        global Bas_cap8
        
        self.propWin=propWin
        propWin.setObjectName("propWin")
        propWin.resize(330, 607)
        propWin.setStyleSheet("background-color: rgb(36, 36, 36);")

        self.camera_list = QListWidget(propWin)
        self.camera_list.setGeometry(QtCore.QRect(10, 1, 260, 91))
        self.camera_list.itemClicked.connect(self.get_camera_properties)
        self.camera_list.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")

        self.Basler_cameras=[]
        self.t1factory = py.TlFactory.GetInstance()
        self.deviceInfoList = self.t1factory.EnumerateDevices()
        
        for i in range(len(self.deviceInfoList)):
            self.deviceIndex = i
            if self.deviceIndex==0: ## camera 1
                self.basler_1=Bas_cap
                self.CameraSerialNumber=self.basler_1.GetDeviceInfo().GetPropertyValue('SerialNumber')
                self.Basler_cameras.append("Basler:"+str(self.CameraSerialNumber[1]))
            if self.deviceIndex==1: ## camera 2
                self.basler_2=Bas_cap2
                self.CameraSerialNumber=self.basler_2.GetDeviceInfo().GetPropertyValue('SerialNumber')
                self.Basler_cameras.append("Basler:"+str(self.CameraSerialNumber[1]))
            if self.deviceIndex==2: ## camera 3
                self.basler_3=Bas_cap3
                self.CameraSerialNumber=self.basler_3.GetDeviceInfo().GetPropertyValue('SerialNumber')
                self.Basler_cameras.append("Basler:"+str(self.CameraSerialNumber[1]))
            if self.deviceIndex==3: ## camera 4
                self.basler_4=Bas_cap4
                self.CameraSerialNumber=self.basler_4.GetDeviceInfo().GetPropertyValue('SerialNumber')
                self.Basler_cameras.append("Basler:"+str(self.CameraSerialNumber[1]))
            if self.deviceIndex==4: ## camera 5
                self.basler_5=Bas_cap5
                self.CameraSerialNumber=self.basler_5.GetDeviceInfo().GetPropertyValue('SerialNumber')
                self.Basler_cameras.append("Basler:"+str(self.CameraSerialNumber[1]))
            if self.deviceIndex==5: ## camera 6
                self.basler_6=Bas_cap6
                self.CameraSerialNumber=self.basler_6.GetDeviceInfo().GetPropertyValue('SerialNumber')
                self.Basler_cameras.append("Basler:"+str(self.CameraSerialNumber[1]))
            if self.deviceIndex==6: ## camera 7
                self.basler_7=Bas_cap7
                self.CameraSerialNumber=self.basler_7.GetDeviceInfo().GetPropertyValue('SerialNumber')
                self.Basler_cameras.append("Basler:"+str(self.CameraSerialNumber[1]))
            if self.deviceIndex==7: ## camera 8
                self.basler_8=Bas_cap8
                self.CameraSerialNumber=self.basler_8.GetDeviceInfo().GetPropertyValue('SerialNumber')
                self.Basler_cameras.append("Basler:"+str(self.CameraSerialNumber[1]))
               
        for i in range(len(self.Basler_cameras)):
            item=self.Basler_cameras[i]
            self.camera_list.addItem(item)
            
#--------------------------------------------------------------------------------------#    
        self.labelexposure = QtWidgets.QLabel(propWin)
        self.labelexposure.setGeometry(QtCore.QRect(10, 80, 291, 71))
        self.labelexposure.setStyleSheet("color: rgb(255, 255, 255);")
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setUnderline(True)
        font.setWeight(25)
        self.labelexposure.setFont(font)
        self.labelexposure.setObjectName("labelexposure")

        self.Exposure_number_box = QtWidgets.QLineEdit(propWin)
        self.Exposure_number_box.setGeometry(QtCore.QRect(280, 135, 41, 16))
        self.Exposure_number_box.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Exposure_number_box.setClearButtonEnabled(False)
        self.Exposure_number_box.setObjectName("Exposure_number_box")
        
        self.Exposure_Slider = QtWidgets.QSlider(propWin)
        self.Exposure_Slider.setGeometry(QtCore.QRect(20, 135, 251, 16))
        self.Exposure_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Exposure_Slider.setObjectName("Exposure_Slider")
        self.Exposure_Slider.setMaximum(200000)
        self.Exposure_Slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Exposure_Slider.setTickInterval(5000)
        self.Exposure_Slider.sliderPressed.connect(self.Exposure_S)
        self.Exposure_Slider.sliderMoved.connect(self.Exposure_S)
        self.Exposure_Slider.valueChanged.connect(self.Exposure_S)

#--------------------------------------------------------------------------------------#
        self.labelcontrast = QtWidgets.QLabel(propWin)
        self.labelcontrast.setGeometry(QtCore.QRect(10, 190, 291, 71))
        self.labelcontrast.setStyleSheet("color: rgb(255, 255, 255);")
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setUnderline(True)
        font.setWeight(25)
        self.labelcontrast.setFont(font)
        self.labelcontrast.setObjectName("labelcontrast")

        self.Contrast_number_box = QtWidgets.QLineEdit(propWin)
        self.Contrast_number_box.setGeometry(QtCore.QRect(280, 240, 41, 16))
        self.Contrast_number_box.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Contrast_number_box.setClearButtonEnabled(False)
        self.Contrast_number_box.setObjectName("Contrast_number_box")
        
        self.Contrast_Slider = QtWidgets.QSlider(propWin)
        self.Contrast_Slider.setGeometry(QtCore.QRect(20, 240, 251, 16))
        self.Contrast_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Contrast_Slider.setObjectName("Contrast_Slider")
        self.Contrast_Slider.setMaximum(5000)
        self.Contrast_Slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Contrast_Slider.setTickInterval(500)
        self.Contrast_Slider.sliderPressed.connect(self.Contrast_S)
        self.Contrast_Slider.sliderMoved.connect(self.Contrast_S)
        self.Contrast_Slider.valueChanged.connect(self.Contrast_S)
#--------------------------------------------------------------------------------------#
        self.labelGain = QtWidgets.QLabel(propWin)
        self.labelGain.setGeometry(QtCore.QRect(10, 150, 291, 41))
        self.labelGain.setStyleSheet("color: rgb(255, 255, 255);")
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setUnderline(True)
        font.setWeight(25)
        self.labelGain.setFont(font)
        self.labelGain.setObjectName("labelGain")

        self.Gain_number_box = QtWidgets.QLineEdit(propWin)
        self.Gain_number_box.setGeometry(QtCore.QRect(280, 190, 41, 16))
        self.Gain_number_box.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Gain_number_box.setClearButtonEnabled(False)
        self.Gain_number_box.setObjectName("Gain_number_box")

        self.Gain_Slider = QtWidgets.QSlider(propWin)
        self.Gain_Slider.setGeometry(QtCore.QRect(20, 190, 251, 16))
        self.Gain_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Gain_Slider.setObjectName("Gain_Slider")	
        self.Gain_Slider.setMaximum(20)
        self.Gain_Slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Gain_Slider.setTickInterval(1)
        self.Gain_Slider.sliderPressed.connect(self.Gain_S)
        self.Gain_Slider.sliderMoved.connect(self.Gain_S)
        self.Gain_Slider.valueChanged.connect(self.Gain_S)
       
#--------------------------------------------------------------------------------------#

        self.Closeprop_Button = QtWidgets.QPushButton(propWin)
        self.Closeprop_Button.setGeometry(QtCore.QRect(100, 520, 100, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Closeprop_Button.setFont(font)
        self.Closeprop_Button.setStyleSheet("background-color: rgb(220, 220, 220);")
        self.Closeprop_Button.clicked.connect(self.closeprop)
        
        self.retranslateUiprop(propWin)
        QtCore.QMetaObject.connectSlotsByName(propWin)
         

    def retranslateUiprop(self, propWin):
        _translate = QtCore.QCoreApplication.translate  
        propWin.setWindowTitle(_translate("propWin", "Camera Properties"))
        self.labelexposure.setText(_translate("propWin", "Exposure (micro-s)"))
        self.labelGain.setText(_translate("propWin", "Gain"))
        self.labelcontrast.setText(_translate("propWin", "Contrast"))
        self.Closeprop_Button.setText(_translate("propWin", "Close"))


    def Exposure_S(self):
        self.Exposure_slider=self.Exposure_Slider.value()
        self.Exposure_slider_str=str(self.Exposure_slider)
        self.Exposure_number_box.setText(self.Exposure_slider_str)
        try:
            if camera_index==0:
                Bas_cap.ExposureTime.SetValue(self.Exposure_slider)
            if camera_index==1:
                Bas_cap2.ExposureTime.SetValue(self.Exposure_slider)
            if camera_index==2:
                Bas_cap3.ExposureTime.SetValue(self.Exposure_slider)
            if camera_index==3:
                Bas_cap4.ExposureTime.SetValue(self.Exposure_slider)
##            if camera_index==4:
##            if camera_index==5:
##            if camera_index==6:
##            if camera_index==7:
        except:
            pass
     

    def Contrast_S(self):
        self.Contrast_Slider_val=self.Contrast_Slider.value()
        self.Contrast_slider_str=str(self.Contrast_Slider_val)
        self.Contrast_number_box.setText(self.Contrast_slider_str)

    def Gain_S(self):
        self.Gain_Slider_val=self.Gain_Slider.value()
        self.Gain_slider_str=str(self.Gain_Slider_val)
        self.Gain_number_box.setText(self.Gain_slider_str)
        try:
            if camera_index==0:
                Bas_cap.Gain.SetValue(self.Gain_Slider.value())
            if camera_index==1:
                Bas_cap2.Gain.SetValue(self.Gain_Slider.value())
            if camera_index==2:
                Bas_cap3.Gain.SetValue(self.Gain_Slider.value())
            if camera_index==3:
                Bas_cap4.Gain.SetValue(self.Gain_Slider.value())
##            if camera_index==4:
##            if camera_index==5:
##            if camera_index==6:
##            if camera_index==7:
        except:
            pass

    def get_camera_properties(self):
        global camera_index
        index = self.camera_list.selectedIndexes()[0]
        camera_index=index.row()
        ui.update_camera_selection(Dialog, camera_index)

        if camera_index==0:
            Exposure=int(Bas_cap.ExposureTime.GetValue())
            Gain=int(Bas_cap.Gain.GetValue())
            self.Exposure_Slider.setValue(Exposure)
            self.Gain_Slider.setValue(Gain)
        if camera_index==1:
            Exposure=int(Bas_cap2.ExposureTime.GetValue())
            Gain=int(Bas_cap2.Gain.GetValue())
            self.Exposure_Slider.setValue(Exposure)
            self.Gain_Slider.setValue(Gain)
        if camera_index==2:
            Exposure=int(Bas_cap3.ExposureTime.GetValue())
            Gain=int(Bas_cap3.Gain.GetValue())
            self.Exposure_Slider.setValue(Exposure)
            self.Gain_Slider.setValue(Gain)
        if camera_index==3:
            Exposure=int(Bas_cap4.ExposureTime.GetValue())
            Gain=int(Bas_cap4.Gain.GetValue())
            self.Exposure_Slider.setValue(Exposure)
            self.Gain_Slider.setValue(Gain)
##        if camera_index==4:
##            Exposure=Bas_cap.ExposureTime.GetValue()
##            Gain=Bas_cap.Gain.GetValue()
##        if camera_index==5:
##            Exposure=Bas_cap.ExposureTime.GetValue()
##            Gain=Bas_cap.Gain.GetValue()
##        if camera_index==6:
##            Exposure=Bas_cap.ExposureTime.GetValue()
##            Gain=Bas_cap.Gain.GetValue()
##        if camera_index==7:
##            Exposure=Bas_cap.ExposureTime.GetValue()
##            Gain=Bas_cap.Gain.GetValue()

    def closeprop(self):
        self.propWin.close()
#--------------------------------------------------------------------------#        
#--------------------------------------------------------------------------#


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    #Dialog.show()
    Dialog.showMaximized()
    sys.exit(app.exec_())
