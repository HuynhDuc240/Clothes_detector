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
from Person import *
import pandas as pd
import os, random
import requests
import time
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.Clothes = Clothes()
        self.Upper = Upper()
        self.Person = Person()
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
        # self.property_1 = QtWidgets.QLabel(self.centralwidget)
        # self.property_1.setGeometry(QtCore.QRect(480, 21, 160, 160))
        # self.property_1.setText("")
        # image_not_found = QtGui.QPixmap('images/iamge_not_found_1.png')
        # image_not_found = image_not_found.scaled(160,160)
        # self.property_1.setPixmap(image_not_found)
        # self.property_1.setObjectName("property_1")
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
        self.result.setGeometry(QtCore.QRect(480, 480, 160, 100))
        self.result.setFont(font)
        self.result.setObjectName("result")
        self.List_image_processing = QtWidgets.QListWidget(self.centralwidget)
        self.List_image_processing.setGeometry(QtCore.QRect(480, 21, 280, 450)) 
        self.List_product_same = QtWidgets.QListWidget(self.centralwidget)
        self.List_product_same.setGeometry(QtCore.QRect(740, 21, 280, 450)) 
        '''
            turn off lines of code below if you don't show list image
        '''
        ########### show some clothe ###############
        # for i in range(10):
        #     path = "data_showing/"
        #     file_name = random.choice(os.listdir(path))
        #     data = pd.read_csv(path+file_name, sep="\t", index_col=0)
        #     df_element = data.sample(n=1)
        #     image_url = df_element['url'][0]
        #     r = requests.get(image_url)
        #     with open ('images/'+str(i)+'.jpg','wb') as f:
        #         f.write(r.content)
        #     ### download #########
        #     icon = QtGui.QPixmap('images/'+str(i)+'.jpg')
        #     myQCustomQWidget = QCustomQWidget()
        #     myQCustomQWidget.setIcon(icon.scaled(190, 220))
        #     List_product_sameItem = QtWidgets.QListWidgetItem(self.List_product_same)
        #     List_product_sameItem.setSizeHint(myQCustomQWidget.sizeHint())
        #     List_product_sameItem.setForeground(QtGui.QColor(255,255,255))
        #     self.List_product_same.addItem(List_product_sameItem)
        #     self.List_product_same.setItemWidget(List_product_sameItem, myQCustomQWidget)
        
        ###################################################################
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
            self.Person.clear()
            self.Upper.clear()
            self.fileName = fileName
            self.show_image()
            start_time = time.time()
            self.predict()
            end_time = time.time()
            print ('run-time perdiction: %f ms' % ((end_time - start_time) * 1000))
            # self.show_similar_clothes()

    def show_image(self):
        image_show = QtGui.QPixmap(self.fileName)
        image_show = image_show.scaled(480,579)
        self.main_image.setPixmap(image_show)


    def predict(self):
        self.List_image_processing.clear()
        self.Person.set_image_by_filename(self.fileName)
        self.Person.predict()
        person_processed = []

        for i in range(len(self.Person.object_detected)):
            icon = QtGui.QPixmap('images/person'+str(i)+'.jpg')
            person_processed.append('images/person'+str(i)+'.jpg')
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setIcon(icon.scaled(190, 220))
            myQCustomQWidget.setTextUp('person')
            myQCustomQWidget.setTextDown(str(self.Person.object_detected[i][0]*100)+"%")
            person_list = QtWidgets.QListWidgetItem(self.List_image_processing)
            person_list.setSizeHint(myQCustomQWidget.sizeHint())
            self.List_image_processing.addItem(person_list)
            self.List_image_processing.setItemWidget(person_list, myQCustomQWidget)
            
        self.properties = []
        upper_processed = []
        if len(person_processed) != 0:
            for c in person_processed:
                self.Upper.set_image_by_filename(c)
                self.Upper.predict()
                upper_processed.append(self.Upper.image_detected[0])
            
        if len(person_processed) != 0 and len(upper_processed) != 0:
            n=0
            for i in upper_processed:
                self.Clothes.set_image(i)
                self.Clothes.predict()
                cv2.imwrite('images/upper'+ str(n)+ '.jpg',i)
                if self.Clothes.type != "":
                    self.properties.append([self.Clothes.type,self.Clothes.color])
                icon = QtGui.QPixmap('images/upper'+ str(n)+ '.jpg')
                myQCustomQWidget = QCustomQWidget()
                myQCustomQWidget.setIcon(icon.scaled(190, 220))
                upper_list = QtWidgets.QListWidgetItem(self.List_image_processing)
                upper_list.setSizeHint(myQCustomQWidget.sizeHint())
                self.List_image_processing.addItem(upper_list)
                self.List_image_processing.setItemWidget(upper_list, myQCustomQWidget)
                n+=1
        if len(person_processed) != 0 and len(upper_processed) == 0:
            # print("none upper\n")
            for i in person_processed:
                self.Clothes.set_image_by_filename(i)
                self.Clothes.predict()
                if self.Clothes.type != "":
                    self.properties.append([self.Clothes.type,self.Clothes.color])
        if len(person_processed) == 0:
            self.Clothes.set_image_by_filename(self.fileName)
            self.Clothes.predict()
            if self.Clothes.type != "":
                self.properties.append([self.Clothes.type,self.Clothes.color])
        if len(self.properties) != 0:
            text=""
            for item in range(len(self.properties)):
                text += self.properties[item][0][0]+ ": " + str(self.properties[item][0][1])+ "\n" + self.properties[item][1][0]+ ": " + str(self.properties[item][1][1])+ "\n"
            self.result.setText(text)
        else:
            self.result.setText("Don't have any clothes in image")
        print(self.properties)
        # self.Upper.set_image_by_filename(self.fileName)
        # self.Upper.predict()
        # image_process = self.Upper.image_detected
        # self.properties = []
        # for i in image_process:
        #     img = cv2.resize(i,(160,160))
        #     image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #     height, width, _ = image.shape
        #     bytesPerLine = 3 * width
        #     qImage = QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        #     pixmap = QtGui.QPixmap.fromImage(qImage)
        #     self.property_1.setPixmap(pixmap)
        #     self.Clothes.set_image(i)
        #     self.Clothes.predict()
        #     if self.Clothes.type != "":
        #         self.properties.append([self.Clothes.type,self.Clothes.color])

    # def show_similar_clothes(self):
    #     if len(self.properties) != 0:
    #         text=""
    #         self.List_product_same.clear()
    #         for item in range(len(self.properties)):
    #             text += self.properties[item][0][0]+ ": " + str(self.properties[item][0][1])+ "\n" + self.properties[item][1][0]+ ": " + str(self.properties[item][1][1])+ "\n"
    #             fileName = "data_showing/"+self.properties[item][0][0] +"_"+ self.properties[item][1][0]+".csv"
    #             data = pd.read_csv(fileName, sep="\t", index_col=0)
    #             items_in_class = int(5/len(self.properties))
    #             for i in range(items_in_class):
    #                 df_element = data.sample(n=1)
    #                 image_url = df_element['url'][0]
    #                 r = requests.get(image_url)
    #                 with open ('images/'+str(i)+'.jpg','wb') as f:
    #                     f.write(r.content)
    #                 ### download #########
    #                 icon = QtGui.QPixmap('images/'+str(i)+'.jpg')
    #                 myQCustomQWidget = QCustomQWidget()
    #                 myQCustomQWidget.setIcon(icon.scaled(190, 220))
    #                 List_product_sameItem = QtWidgets.QListWidgetItem(self.List_product_same)
    #                 List_product_sameItem.setSizeHint(myQCustomQWidget.sizeHint())
    #                 List_product_sameItem.setForeground(QtGui.QColor(255,255,255))
    #                 self.List_product_same.addItem(List_product_sameItem)
    #                 self.List_product_same.setItemWidget(List_product_sameItem, myQCustomQWidget)
    #         self.result.setText(text)
    #     else:
    #         self.result.setText("Don't have any clothes in image")

class QCustomQWidget (QtWidgets.QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        font = QtGui.QFont()
        font.setPointSize(5)
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
