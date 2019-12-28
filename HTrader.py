# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 00:11:52 2018

@author: USER
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
#from sqlite_save_from_Ebest import *
from bestConnect import *

from DBanal import *
from opt_order_tr import *
from sec_info import *


import pandas as pd
import sqlite3
import datetime

#from subject import *
from observer import *
from ControllerInterface import *



from OptScanController import *

form_class = uic.loadUiType("mainwindowv03.ui")[0]

class MyWindow(QMainWindow, form_class, Observer):
    def __init__(self, ControllerInterface, optdata):
        super().__init__()

      

        self.controller = ControllerInterface
        
        
        #로그인 프로세스
        self.secinfo = secInfo()
        self.best = BestAccess()
        self.accounts_list = self.best.comm_connect(self.secinfo)
        self.passwd =  self.secinfo.getOrderPasswd()  

        
        self.setupUi(self)
#        #자신을 observer로 등록
        self.register_subject(optdata)  
     
        
        
        self.lineEdit.textChanged.connect(self.code_changed)
        self.pushButton.clicked.connect(self.StartButton)
        
#        self..pushButton.clicked.
#        self.remained_burget = 1
     
        
        
#        ####################test code####################
#        #timer2
#        self.timer2 = QTimer(self)
#        self.timer2.start(1000*4)
#        self.timer2.timeout.connect(self.timeout2)
#        self.test_counter = 0
#        
        self.controller.Start()  
        
        
#------------------------------observer implementaion -----------------------------------------------------------------------------       
    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_, 이론가_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        self.단축코드=단축코드_
        self.호가시간=호가시간_
        self.매도호가1=매도호가1_
        self.매수호가1=매수호가1_
        self.이론가 = 이론가_
       
        self.display()
        self.updateGuiOptHoga()

    def register_subject(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def display(self):
        #print ("Gui updated")
        pass

    def updateGuiOptHoga(self):
         
        optHogaChart = self.subject.get_optChart()
        itemcount = len(optHogaChart)
        row_no = 0

        for j in sorted(optHogaChart):
          #  item = QTableWidgetItem(balcv[j][])
            row_no += 1
            item = QTableWidgetItem(j)
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(row_no,0,item)  
          
            item = QTableWidgetItem(optHogaChart[j]['offerho1'])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(row_no,1,item)
            
            item = QTableWidgetItem(optHogaChart[j]['bidho1'])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(row_no,2,item)
            
            item = QTableWidgetItem(self.subject.envStatus["kospi200Index"])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(row_no,3,item)

            item = QTableWidgetItem(self.subject.envStatus["옵션잔존일"])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(row_no,4,item)

            item = QTableWidgetItem(self.subject.envStatus["HV"])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(row_no,5,item)

        self.tableWidget_2.setRowCount(itemcount)
        
       
#        pass
#----------------------------------------------------------------------------------------------------------------------     
       
    def code_changed(self):
        print("code changed")
        code= self.lineEdit.text()
        name = self.best.get_master_code_name(code)
        self.lineEdit_2.setText(name)
        

    def StartButton(self):
        self.controller.Start()
   
    
    def EndButton(self):
        self.controller.End()
  
    def closeEvent(self, event):
        print("event")
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.controller.End()
            event.accept()
        else:
            event.ignore()
            
            
if __name__=="__main__":
    app = QApplication(sys.argv)
    optdata =  OptData() #ㅐ
    optscancon = OptScanContoller(optdata)
    myWindow = MyWindow(optscancon, optdata)
    myWindow.show()
    app.exec_()
    
