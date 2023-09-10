# -*- coding: utf-8 -*-

import sys
import threading
import copy
import pandas as pd
import sqlite3
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from observer import *
from ControllerInterface import *
from OptScanController import *
from OptStatusMonitor import *
from XingAPIMonitor import *  
from OptStatMonitorSimul import *

form_class = uic.loadUiType("mainwindowv03.ui")[0]

class MyWindow(QMainWindow, form_class, Observer):

    def __init__(self, ControllerInterface, optdata):
        super().__init__()
        
        self.controller = ControllerInterface
        self.setupUi(self)
        self.register_subject(optdata)  
        
        self.lineEdit.textChanged.connect(self.code_changed)
        self.pushButton.clicked.connect(self.StartButton)
        self.controller.Start(optdata) 
        self.updateGuiOptHoga()

    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_, 이론가_):
        self.단축코드=단축코드_
        self.호가시간=호가시간_
        self.매도호가1=매도호가1_
        self.매수호가1=매수호가1_
        self.이론가 = 이론가_
       
        self.display()
        #self.updateGuiOptHoga()

    def register_subject(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def display(self):
        pass

    def updateGuiOptHoga(self):
        optHogaChart = copy.deepcopy(self.subject.get_optChart())
        itemcount = len(optHogaChart)
        row_no = 0

        for j in sorted(optHogaChart):
            row_no += 1

            self.tableWidget_2.setItem(row_no, 0, self.create_table_item(j))
            self.tableWidget_2.setItem(row_no, 1, self.create_table_item(optHogaChart[j]['offerho1']))
            self.tableWidget_2.setItem(row_no, 2, self.create_table_item(optHogaChart[j]['bidho1']))
            self.tableWidget_2.setItem(row_no, 3, self.create_table_item(self.subject.envStatus["kospi200Index"]))
            self.tableWidget_2.setItem(row_no, 4, self.create_table_item(self.subject.envStatus["옵션잔존일"]))
            self.tableWidget_2.setItem(row_no, 5, self.create_table_item(self.subject.envStatus["HV"]))

        self.tableWidget_2.setRowCount(itemcount)
        threading.Timer(1, self.updateGuiOptHoga).start()

    def create_table_item(self, text):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        return item

    def code_changed(self):
        print("code changed")
        code = self.lineEdit.text()
        name = self.best.get_master_code_name(code)
        self.lineEdit_2.setText(name)

    def StartButton(self):
        self.controller.Start()
    
    def EndButton(self):
        self.controller.End()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.controller.End()
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    optdata = OptData()
    mode = "XingAPI"

    if mode == "XingAPI":
        optstatmon = XingAPIMonitor()  
        optscancon = OptScanContoller(optdata, optstatmon, "XingAPI")
    elif mode == "simulation":
        optstatmon = OptStatMonitorSimul()
    myWindow = MyWindow(optscancon, optdata)
    myWindow.show()
    app.exec_()