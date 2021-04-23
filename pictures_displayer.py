# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pictures_displayer.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import sys
import numpy as np
import pandas as pd
from matplotlib import cm
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtCore, QtGui, QtWidgets




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(756, 577)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelForPixmap = QtWidgets.QLabel(self.centralwidget)
        self.labelForPixmap.setGeometry(QtCore.QRect(10, 10, 571, 511))
        self.labelForPixmap.setObjectName("labelForPixmap")
        self.labelForWarning = QtWidgets.QLabel(self.centralwidget)
        self.labelForWarning.setGeometry(QtCore.QRect(600, 10, 151, 31))
        self.labelForWarning.setObjectName("labelForWarning")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(600, 50, 101, 32))
        self.comboBox.setObjectName("comboBox")
        self.buttonComboBox = QtWidgets.QPushButton(self.centralwidget)
        self.buttonComboBox.setGeometry(QtCore.QRect(600, 90, 112, 32))
        self.buttonComboBox.setObjectName("buttonComboBox")
        self.labelGrains = QtWidgets.QLabel(self.centralwidget)
        self.labelGrains.setGeometry(QtCore.QRect(600, 150, 171, 16))
        self.labelGrains.setObjectName("labelGrains")
        self.buttonGrains = QtWidgets.QPushButton(self.centralwidget)
        self.buttonGrains.setGeometry(QtCore.QRect(600, 210, 112, 32))
        self.buttonGrains.setObjectName("buttonGrains")
        self.buttonCancel = QtWidgets.QPushButton(self.centralwidget)
        self.buttonCancel.setGeometry(QtCore.QRect(640, 440, 112, 32))
        self.buttonCancel.setObjectName("buttonCancel")
        self.grainLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.grainLineEdit.setGeometry(QtCore.QRect(600, 180, 113, 21))
        self.grainLineEdit.setObjectName("grainLineEdit")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(640, 290, 112, 32))
        self.loadButton.setObjectName("loadButton")
        self.allGrainsButton = QtWidgets.QPushButton(self.centralwidget)
        self.allGrainsButton.setGeometry(QtCore.QRect(601, 251, 111, 31))
        self.allGrainsButton.setObjectName("allGrainsButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 756, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.buttonComboBox.clicked.connect(lambda:self.comboBoxFun())
        self.buttonGrains.clicked.connect(lambda:self.oneGrainFun())
        self.allGrainsButton.clicked.connect(lambda:self.allGrainFun())
        self.loadButton.clicked.connect(lambda:self.loadFun())
        self.buttonCancel.clicked.connect(lambda:self.closeFun())
        
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelForPixmap.setText(_translate("MainWindow", ""))
        self.labelForWarning.setText(_translate("MainWindow", ""))
        self.buttonComboBox.setText(_translate("MainWindow", "Display"))
        self.labelGrains.setText(_translate("MainWindow", ""))
        self.buttonGrains.setText(_translate("MainWindow", "Display"))
        self.buttonCancel.setText(_translate("MainWindow", "Cancel"))
        self.loadButton.setText(_translate("MainWindow", "Load"))
        self.allGrainsButton.setText(_translate("MainWindow", "Show all"))
        self.selected_data = pd.DataFrame(data=[], columns=['X', 'Y', 'Phase', 'grainId_5deg'])
    
    
    
    def loadFun(self):
        try:
            imagePath, _ = QtWidgets.QFileDialog.getOpenFileName()
            df = pd.DataFrame(data=[], columns=['X', 'Y', 'Phase', 'grainId_5deg'])
            df = pd.read_csv(imagePath,sep='\t')
        except OSError as err:
            self.labelForWarning.setText("OS error: {0}".format(err))
        except ValueError as err:
            self.labelForWarning.setText("ValueError: {0}".format(err))
        except:
            self.labelForWarning.setText("Unexpected error: {0}".format(sys.exc_info()[0]))
        
        self.comboBox.clear()
        self.comboBox.addItems(map(str, np.sort(df['Phase'].unique())))
        self.labelGrains.setText("Grains range: {0}, {1}.".format(df['grainId_5deg'].min(), df['grainId_5deg'].max()))
        
        self.selected_data = df[['X', 'Y', 'Phase', 'grainId_5deg']]
        
        image_matrix = self.make_image(int(df['Y'].max() *10), int(df['X'].max() *10), df['Phase'].to_numpy())
        
        image  = Image.fromarray(np.uint8(cm.hsv(image_matrix) *255))
        pixmap = QtGui.QPixmap.fromImage(ImageQt(image))
        self.labelForPixmap.setPixmap(pixmap.scaled(self.labelForPixmap.size(), QtCore.Qt.KeepAspectRatio))
    
    
    def comboBoxFun(self):
        phase = int(self.comboBox.currentText())
        
        image_matrix = self.image_binarization_by_phase(int(self.selected_data['Y'].max() *10), \
                                                            int(self.selected_data['X'].max() *10), \
                                                            self.selected_data['Phase'].to_numpy(), phase)
        
        image  = Image.fromarray(np.uint8(cm.gist_ncar(image_matrix) *255))
        pixmap = QtGui.QPixmap.fromImage(ImageQt(image))
        self.labelForPixmap.setPixmap(pixmap.scaled(self.labelForPixmap.size(), QtCore.Qt.KeepAspectRatio))
    
    
    def oneGrainFun(self):
        try:
            grain = int(self.grainLineEdit.text())
        except ValueError as err:
            self.labelForWarning.setText("ValueError: {0}".format(err))
        
        if grain < self.selected_data['grainId_5deg'].min() or grain > self.selected_data['grainId_5deg'].max():
            self.labelForWarning.setText("Wrong value- out of range.")
            return
        
        image_matrix = self.make_image(int(self.selected_data['Y'].max() *10), \
                                        int(self.selected_data['X'].max() *10), \
                                        self.selected_data['Phase'].to_numpy())
        image_matrix = self.display_grain_on_image(image_matrix, self.selected_data['grainId_5deg'].to_numpy(), grain)
        
        image  = Image.fromarray(np.uint8(cm.gist_ncar(image_matrix) *255))
        pixmap = QtGui.QPixmap.fromImage(ImageQt(image))
        self.labelForPixmap.setPixmap(pixmap.scaled(self.labelForPixmap.size(), QtCore.Qt.KeepAspectRatio))
    
    
    def allGrainFun(self):
        image_matrix = self.make_image(int(self.selected_data['Y'].max() *10), \
                                        int(self.selected_data['X'].max() *10), \
                                        self.selected_data['Phase'].to_numpy())
        image_matrix = self.image_color_segmentation(image_matrix, self.selected_data['grainId_5deg'].to_numpy())
        
        image  = Image.fromarray(np.uint8(cm.gist_rainbow(image_matrix) *255))
        pixmap = QtGui.QPixmap.fromImage(ImageQt(image))
        self.labelForPixmap.setPixmap(pixmap.scaled(self.labelForPixmap.size(), QtCore.Qt.KeepAspectRatio))
    
    
    
    def closeFun(self):
        exit()
    
    
    def make_image(self, row_range, col_range, values):
        image_tab = np.zeros((row_range+1, col_range+1))
    
        for i in range((row_range+1) * (col_range+1) - values.shape[0]):
            values = np.concatenate((values, [values[-1]]))
    
    
        for i in range(row_range+1):
            for j in range(col_range+1):
                image_tab[i][j] = values[i * (col_range+1) + j]
    
        return image_tab / values.max() # normalization 0:1
    
    
    def display_grain_on_image(self, input_tab, grains, grain_number):
        output_tab = np.copy(input_tab)

        for i in range((input_tab.shape[0]) * (input_tab.shape[1]) - grains.shape[0]):
            grains = np.concatenate((grains, [grains[-1]]))

        for i in range(input_tab.shape[0]):
            for j in range(input_tab.shape[1]):
        
                if(grains[i * input_tab.shape[1] + j] == grain_number):
                    output_tab[i][j] = 0

        return output_tab
    
    
    def image_binarization_by_phase(self, row_range, col_range, values, phase):
        image_tab = np.zeros((row_range+1, col_range+1))
    
        for i in range((row_range+1) * (col_range+1) - values.shape[0]):
            values = np.concatenate((values, [values[-1]]))
    
    
        for i in range(row_range+1):
            for j in range(col_range+1):
            
                if(values[i * (col_range+1) + j] == phase):
                    image_tab[i][j] = 1
                else:
                    image_tab[i][j] = 0
    
        return image_tab
    
    
    def image_color_segmentation(self, input_tab, grains):
        output_tab = np.copy(input_tab)
    
        for i in range((input_tab.shape[0]+1) * (input_tab.shape[1]+1) - grains.shape[0]):
            grains = np.concatenate((grains, [grains[-1]]))
    
    
        for i in range(input_tab.shape[0]):
            for j in range(input_tab.shape[1]):
                output_tab[i][j] = np.remainder(grains[i * input_tab.shape[1] + j], 255)
    
        return output_tab / 255.









def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    sys.exit(main())

