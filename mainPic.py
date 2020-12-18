# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import sys

import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
                             QVBoxLayout, QApplication, QLabel, QPushButton, QFileDialog, QHBoxLayout)
from tools.PicProcess import PicProcess

#attr: picLabel btnLoad
class mainWidget(QWidget):
    def __init__(self):
        super(mainWidget,self).__init__()
        self.pic=QPixmap()
        self.initUI()
    def initUI(self):
        self.setMinimumSize(800,600)
        self.setWindowTitle("素材提取")

        self.picLabel=myLabel(self)
        self.picLabel.setText("显示导入图片")

        self.picLabel.setMinimumSize(775,530)

        self.btnLoad=QPushButton(self)
        self.btnLoad.setText("导入新图片")


        self.btnSave=QPushButton(self)
        self.btnSave.setText("截取另存为")

        self.picLabel.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:25px;font-weight;font-family:宋体;}"
                                 )

        #信号槽
        self.btnLoad.clicked.connect(self.loadPic)
        self.btnSave.clicked.connect(self.savePic)

        #布局
        vbox=QVBoxLayout()
        hbox=QHBoxLayout()
        hbox.addWidget(self.btnLoad)
        hbox.addWidget(self.btnSave)
        vbox.addWidget(self.picLabel)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.show()

        # 读取图片并显示

    def loadPic(self):
        # imgName, imgType = QFileDialog.getOpenFileName(self, "选择图片")
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "")
        if imgName == "":
            return 0

        originImg=cv2.imread(imgName)
        self.picLabel.setFixedSize(originImg.shape[1]/2,originImg.shape[0]/2)
        self.pic = QtGui.QPixmap(imgName).scaled(self.picLabel.width(),self.picLabel.height())

        self.picLabel.setPixmap(self.pic)

        self.picLabel.setCursor(Qt.CrossCursor)

        #保存截取图片
    def savePic(self):
        label = self.picLabel
        if (~label.flag):
            process=PicProcess(self.picLabel.pixmap())
            result=process.grab_cut((label.x0, label.y0, abs(label.x1 - label.x0), abs(label.y1 - label.y0)))
            cv2.imshow('result',result)
            cv2.waitKey(0)
            filename=QFileDialog.getSaveFileName(self,"保存文件",".","Image Files(*.png *.jpg)",)
            cv2.imwrite(filename[0], result)  # 注意保存的路径不能有中文
            print(filename[0])
            # cv2.imwrite('result/result6.png', result)
            print("保存成功")
        else:
            return 0



class myLabel(QLabel):
    x0=0
    y0=0
    x1=0
    y1=0
    flag=False

    def mousePressEvent(self,event):
        self.flag=True
        self.x0=event.x()
        self.y0=event.y()

    def mouseReleaseEvent(self, event):
        self.flag=False

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1=event.x()
            self.y1=event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect=QRect(self.x0,self.y0,abs(self.x1-self.x0),abs(self.y1-self.y0))
        painter=QPainter(self)
        painter.setPen(QPen(Qt.red,4,Qt.SolidLine))
        painter.drawRect(rect)
        print(rect.x(),rect.y(),rect.width(),rect.height())






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex=mainWidget()

    sys.exit(app.exec_())
