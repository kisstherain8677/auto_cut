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
    QVBoxLayout, QApplication,QLabel,QPushButton,QFileDialog)

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
        self.btnLoad.setText("导入图片")
        self.btnLoad.clicked.connect(self.loadPic)

        self.picLabel.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:25px;font-weight;font-family:宋体;}"
                                 )

        vbox=QVBoxLayout()
        vbox.addWidget(self.picLabel)
        vbox.addWidget(self.btnLoad)
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


    def grab_cut(self,r):#r是rect
        src=formatcvt.qtpixmap_to_cvimg(self.picLabel.pixmap())
        roi = src[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        # 原图mask，与原图等大小
        mask = np.zeros(src.shape[:2], dtype=np.uint8)

        # 矩形roi
        rect = (int(r[0]), int(r[1]), int(r[2]), int(r[3]))  # 包括前景的矩形，格式为(x,y,w,h)

        # bg模型的临时数组
        bgdmodel = np.zeros((1, 65), np.float64)
        # fg模型的临时数组
        fgdmodel = np.zeros((1, 65), np.float64)

        cv2.grabCut(src, mask, rect, bgdmodel, fgdmodel, 11, mode=cv2.GC_INIT_WITH_RECT)

        print(np.unique(mask))
        # 提取前景和可能的前景区域
        mask2 = np.where((mask == 1) | (mask == 3), 255, 0).astype('uint8')

        print(mask2.shape)

        # 按位与 src & src == 0，得到的是二进制
        result = cv2.bitwise_and(src, src, mask=mask2)
        # cv2.imwrite('result.jpg', result)
        # cv2.imwrite('roi.jpg', roi)
        # result转为四通道
        b_channel, g_channel, r_channel = cv2.split(result)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
        result_BGAR = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
        # result[np.all(result==[0,0,0,255],axis=2)]=[0,0,0,0]
        result_BGAR[np.all(result_BGAR == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]
        #cv2.imshow(result)
        cv2.imwrite('result/test4_re.png', result_BGAR)
        print("保存成功")

    def keyPressEvent(self, event):
        label=self.picLabel
        if(~label.flag):
            self.grab_cut((label.x0, label.y0, abs(label.x1 - label.x0), abs(label.y1 - label.y0)))
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


#工具类，opencv和QImage的互换
class formatcvt():
    #静态方法
    def qtpixmap_to_cvimg(qtpixmap):
        qimg = qtpixmap.toImage()
        temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
        temp_shape += (4,)
        ptr = qimg.bits()
        ptr.setsize(qimg.byteCount())
        result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
        result = result[..., :3]

        return result

    def cvimg_to_qtimg(cvimg):
        height, width, depth = cvimg.shape
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        cvimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)

        return cvimg



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex=mainWidget()

    sys.exit(app.exec_())
