#-*- coding:utf-8 -*-
'''
inputDialog
'''
__author__ = 'Tony Zhu'

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QInputDialog, QGridLayout, QLabel, QPushButton, QFrame

class InputDialog(QWidget):
    def __init__(self):       
        super(InputDialog,self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("输入描述信息")
        self.setGeometry(400,400,300,260)

        example_sentence="请输入描述的句子，描述鸟的身体颜色、头冠颜色、腹部颜色、翅膀颜色、喙的长度等，可参考以下示例：\n"+\
                "this bird is red with white and has a very short beak\n"+\
            "the bird has a yellow crown and a black eyering that is round"
        label0=QLabel(example_sentence)
        label1=QLabel("身体颜色:")
        label2=QLabel("头冠颜色:")
        label3=QLabel("腹部颜色:")
        label4=QLabel("翅膀颜色:")
        label5=QLabel("喙长度:")
        label6=QLabel("编辑描述句子")

        self.bodyColorLabel = QLabel("red with white")
        self.bodyColorLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.crownColorLabel = QLabel("red")
        self.crownColorLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.bellyColorLabel = QLabel("white")
        self.bellyColorLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.wingsColorLabel = QLabel("yellow")
        self.wingsColorLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.beakSizeLabel = QLabel("short")
        self.beakSizeLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        self.introductionLabel = QLabel("this bird is red with white and has a very short beak")
        self.introductionLabel.setFrameStyle(QFrame.Panel|QFrame.Sunken)

        bodyColorButton=QPushButton("...")
        bodyColorButton.clicked.connect(self.selectName)
        crownColorButton=QPushButton("...")
        crownColorButton.clicked.connect(self.selectStyle)
        bellyColorButton=QPushButton("...")
        bellyColorButton.clicked.connect(self.selectNumber)
        wingsColorButton=QPushButton("...")
        wingsColorButton.clicked.connect(self.selectCost)
        beakSizeButton=QPushButton("...")
        beakSizeButton.clicked.connect(self.selectBeak)
        showDisButton=QPushButton("...")
        showDisButton.clicked.connect(self.selectIntroduction)

        mainLayout=QGridLayout()
        mainLayout.addWidget(label1,0,0)
        mainLayout.addWidget(self.bodyColorLabel,0,1)
        mainLayout.addWidget(bodyColorButton,0,2)
        mainLayout.addWidget(label2,1,0)
        mainLayout.addWidget(self.crownColorLabel,1,1)
        mainLayout.addWidget(crownColorButton,1,2)
        mainLayout.addWidget(label3,2,0)
        mainLayout.addWidget(self.bellyColorLabel,2,1)
        mainLayout.addWidget(bellyColorButton,2,2)
        mainLayout.addWidget(label4,3,0)
        mainLayout.addWidget(self.wingsColorLabel,3,1)
        mainLayout.addWidget(wingsColorButton,3,2)

        mainLayout.addWidget(label5, 4, 0)
        mainLayout.addWidget(self.beakSizeLabel, 4, 1)
        mainLayout.addWidget(beakSizeButton, 4, 2)
        
        mainLayout.addWidget(label6,5,0)
        mainLayout.addWidget(self.introductionLabel,5,1)
        mainLayout.addWidget(showDisButton,5,2)

        self.setLayout(mainLayout)



    def selectBodyColor(self):
        name,ok = QInputDialog.getText(self,"身体颜色","输入身体颜色:",
                                       QLineEdit.Normal,self.nameLabel.text())
        if ok and (len(name)!=0):
            self.nameLabel.setText(name)
    def selectStyle(self):
        list = ["外包","自研"]

        style,ok = QInputDialog.getItem(self,"项目性质","请选择项目性质：",list)
        if ok :
            self.crownColorLabel.setText(style)

    def selectNumber(self):
        number,ok = QInputDialog.getInt(self,"项目成员","请输入项目成员人数：",int(self.bellyColorLabel.text()),20,100,2)
        if ok :
            self.bellyColorLabel.setText(str(number))

    def selectCost(self):
        cost,ok = QInputDialog.getDouble(self,"项目成本","请输入项目成员人数：",float(self.wingsColorLabel.text()),100.00,500.00,2)
        if ok :
            self.wingsColorLabel.setText(str(cost))

    def selectIntroduction(self):
        introduction,ok = QInputDialog.getMultiLineText(self,"编辑描述","描述：","this bird is red with white and has a very short beak")
        if ok :
            self.introductionLabel.setText(introduction)

    def selectBeak(self):
        name,ok = QInputDialog.getText(self,"鸟喙大小","输入鸟喙大小:",
                                       QLineEdit.Normal,self.nameLabel.text())
        if ok and (len(name)!=0):
            self.nameLabel.setText(name)



if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)
    myshow=InputDialog()
    myshow.show()
    sys.exit(app.exec_())
