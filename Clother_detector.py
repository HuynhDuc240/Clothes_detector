# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main_Window.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from Clothes import *
from Upper import *
import os, random
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.Clothes = Clothes()
        self.Upper = Upper()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 81, 21))
        self.pushButton.clicked.connect(self.openFileNameDialog)
        self.pushButton.setObjectName("pushButton")
        self.main_image = QtWidgets.QLabel(self.centralwidget)
        self.main_image.setGeometry(QtCore.QRect(0, 21, 480, 579))
        self.main_image.setText("")
        image_not_found = QtGui.QPixmap('images/image_not_found.png')
        image_not_found = image_not_found.scaled(480,579)
        self.main_image.setPixmap(image_not_found)
        self.main_image.setObjectName("main_image")
        self.property_1 = QtWidgets.QLabel(self.centralwidget)
        self.property_1.setGeometry(QtCore.QRect(480, 21, 160, 160))
        self.property_1.setText("")
        image_not_found = QtGui.QPixmap('images/iamge_not_found_1.png')
        image_not_found = image_not_found.scaled(160,160)
        self.property_1.setPixmap(image_not_found)
        self.property_1.setObjectName("property_1")
        # self.property_2 = QtWidgets.QLabel(self.centralwidget)
        # self.property_2.setGeometry(QtCore.QRect(480, 182, 160, 160))
        # self.property_2.setText("")
        # self.property_2.setPixmap(image_not_found)
        # self.property_2.setObjectName("property_2")
        # self.property_3 = QtWidgets.QLabel(self.centralwidget)
        # self.property_3.setGeometry(QtCore.QRect(480, 343, 160, 160))
        # self.property_3.setText("")
        # self.property_3.setPixmap(image_not_found)
        # self.property_3.setObjectName("property_3")
        self.result = QtWidgets.QLabel(self.centralwidget)
        self.result.setGeometry(QtCore.QRect(480, 503, 160, 100))
        self.result.setFont(font)
        self.result.setObjectName("result")
        self.myQListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.myQListWidget.setGeometry(QtCore.QRect(700, 21, 280, 570)) 
        for _ in range(100):
            path = "C:/Users/Huynh Duc/Desktop/data/"
            kind = random.choice(os.listdir(path))
            color = random.choice(os.listdir(path + kind))
            image_name = random.choice(os.listdir(path+kind+"/"+color))
            icon = QtGui.QPixmap(path+kind+"/"+color+"/"+image_name)
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setIcon(icon.scaled(190, 220))
            myQListWidgetItem = QtWidgets.QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            myQListWidgetItem.setForeground(QtGui.QColor(255,255,255))
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Select Image"))

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self.centralwidget,"File", "","All Files (*);;image (*.png,*.jpg)", options=options)
        if fileName:
            path = "C:/Users/Huynh Duc/Desktop/data/"
            self.fileName = fileName
            image_show = QtGui.QPixmap(fileName)
            image_show = image_show.scaled(480,579)
            self.main_image.setPixmap(image_show)
            self.Upper.set_image_by_filename(fileName)
            self.Upper.predict()
            image_process = self.Upper.image_detected
            self.properties = []
            for i in image_process:
                img = cv2.resize(i,(160,160))
                image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                height, width, _ = image.shape
                bytesPerLine = 3 * width
                qImage = QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImage)
                self.property_1.setPixmap(pixmap)
                self.Clothes.set_image(i)
                self.Clothes.predict()
                if self.Clothes.type != "":
                    self.properties.append([self.Clothes.type,self.Clothes.color])
            if len(self.properties) != 0:
                text = ""
                self.myQListWidget.clear()
                for item in range(len(self.properties)):
                    if len(self.properties) ==1 :
                        item_in_class = 100
                    else:
                        item_in_class = int(100 / len(self.properties))
                    text += self.properties[item][0][0]+ ": " + str(self.properties[item][0][1])+ "\n" + self.properties[item][1][0]+ ": " + str(self.properties[item][1][1])+ "\n"
                    folder = path + self.properties[item][0][0] +"/"+ self.properties[item][1][0] 
                    for i in range(item_in_class):
                        iamge_name = random.choice(os.listdir(folder))
                        icon = QtGui.QPixmap(folder +"/"+iamge_name)
                        myQCustomQWidget = QCustomQWidget()
                        myQCustomQWidget.setIcon(icon.scaled(190, 220))
                        myQListWidgetItem = QtWidgets.QListWidgetItem(self.myQListWidget)
                        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
                        myQListWidgetItem.setForeground(QtGui.QColor(255,255,255))
                        self.myQListWidget.addItem(myQListWidgetItem)
                        self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
                self.result.setText(text)
            else:
                self.result.setText("None")
            

class QCustomQWidget (QtWidgets.QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textUpQLabel    = QtWidgets.QLabel()
        self.textDownQLabel  = QtWidgets.QLabel()
        self.text_link = QtGui.QTextDocument()
        self.textUpQLabel.setFont(font)
        self.textDownQLabel.setFont(font)
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QtWidgets.QHBoxLayout()
        self.iconQLabel      = QtWidgets.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
