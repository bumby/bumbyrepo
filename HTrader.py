# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 00:11:52 2018

@author: USER
"""

import sys
import threading
import copy

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic


import pandas as pd
import datetime

#from subject import *
from observer import *
from ControllerInterface import *

from OptScanController import *
from OptStatusMonitor import *

form_class = uic.loadUiType("mainwindowv03.ui")[0]

class MyWindow(QMainWindow, form_class, Observer):
    def __init__(self, ControllerInterface, optdata):
        super().__init__()

      

        self.controller = ControllerInterface
        
        
#        #로그인 프로세스
#        if mode == "XingAPI":
#            self.secinfo = secInfo()
#            self.best = BestAccess()
#            self.accounts_list = self.best.comm_connect(self.secinfo)
#            self.passwd =  self.secinfo.getOrderPasswd()  
#        elif mode == "simulation":
#            self.passwd = "1234"
#        else:
#            print("not adequate mode has been selected")

        
        #ui setting
        self.setupUi(self)
#        #자신을 observer로 등록
        self.register_subject(optdata)  
        self.lineEdit.textChanged.connect(self.code_changed)
        self.pushButton.clicked.connect(self.StartButton)
        
       
        self.controller.Start(optdata) 
        self.updateGuiOptHoga()
        
        
#------------------------------observer implementaion -----------------------------------------------------------------------------       
    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_, 이론가_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
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
       # print(self.단축코드, self.매도호가1, self.매수호가1)
        pass

    def updateGuiOptHoga(self):
         
        optHogaChart = copy.deepcopy(self.subject.get_optChart())
        itemcount = len(optHogaChart)
        row_no = 0

  
        for j in sorted(optHogaChart):
            #print("챠트",optHogaChart[j]['offerho1'], optHogaChart[j]['bidho1'])
            #item = QTableWidgetItem(balcv[j][])
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
        
        threading.Timer(1,self.updateGuiOptHoga).start()
        return True
       
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



from XingAPIMonitor import *   
from OptStatMonitorSimul import *
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    optdata =  OptData()
    mode = "XingAPI"
    #mode = "simulation"
    
    if mode == "XingAPI" :
         optstatmon = XingAPIMonitor()  #data 획득 방법 xing api냐 simulation 이냐 에 따라 생성자 변경
         optscancon = OptScanContoller(optdata,optstatmon, "XingAPI")
    elif mode == "simulation":
        optstatmon = OptStatMonitorSimul()
        optscancon = OptScanContoller(optdata,optstatmon, "XingAPI")
    
    myWindow = MyWindow(optscancon, optdata)
    myWindow.show()
    app.exec_()