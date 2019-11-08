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
          
#------------------------------observer implementaion -----------------------------------------------------------------------------       
    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        self.단축코드=단축코드_
        self.호가시간=호가시간_
        self.매도호가1=매도호가1_
        self.매수호가1=매수호가1_
       
        self.display()
        self.updateGuiOptHoga()

    def register_subject(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def display(self):
        print ("Gui updated")

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

        self.tableWidget_2.setRowCount(itemcount)
        
        print("on construction print", itemcount)
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

#    def send_order(self):
#        order_type_lookup = {'신규매도':1, '신규매수':2}
#        hoga_lookup = {'지정가':"00", '시장가':"03"}
#                        
#        #계좌번호, 비밀번호, 종목번호, 주문수량, 주문가, 매매구분, 호가유형코드, 신용거래코드, 대출일, 주문조건구분
#        account = self.comboBox.currentText()
#
#        code = self.lineEdit.text()
#        OrdQty = self.spinBox.value()
#        OrdPrc = self.spinBox_2.value()          
#        BnsTpcode = self.comboBox_2.currentText()  #//매매구분
#        OrdprcPtnCode = self.comboBox_3.currentText() #호가유형코드
#        MgntrnCode = "000"
#        LoanDt = ""
#        OrdCndiTpCode = 0 # 0 없음 1 IOC 2 FOK
#
#        ordrslt = self.best.order_stock(account, self.secinfo.getOrderPasswd(), code, OrdQty, OrdPrc, order_type_lookup[BnsTpcode], hoga_lookup[OrdprcPtnCode], MgntrnCode, LoanDt, OrdCndiTpCode)
#         
#        
        


#   def timeout2(self):
#        
#        self.test_counter = self.test_counter + 1 
#        self.test_counter_s = str(self.test_counter)
#        self.subject.change_optprice("1234", "201P9360", self.test_counter_s, self.test_counter_s)
#        
        
         
#        #database에 저장
#        optresult, optresult2 = self.optmon.get_opt_chart(self.Option_expiration_mon)
#    
#        df_call = pd.DataFrame(optresult, columns = ['optcode','price','diff', 'volume', 'iv','offerho1','bidho1','theoryprice','impv','gmprice'], index=optresult['actprice'])
#        df_put = pd.DataFrame(optresult2, columns = ['optcode','price','diff', 'volume', 'iv','offerho1','bidho1','theoryprice','impv','gmprice'], index=optresult['actprice'])
#        
#
#        #
#        ATMS = [] #임시 
#        ATMS, deal_signal, sell_code, sell_price, buy_code, buy_price = self.dbanal.extract_call_gap(df_call, 10.0, ATMS)
#        print("sell ", sell_code, buy_code, deal_signal)
#        
#        print("주문 판단 중...")
#        #def order_option(self, 계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량):
#        if deal_signal == "yes" and self.remained_burget == 1:
#            print(self.secinfo.getOptAccount(), self.secinfo.getOrderPasswd(), sell_code, "1", "00", "{:.2f}".format(sell_price), "1")
#            self.order.order_option(self.secinfo.getOptAccount(), self.secinfo.getOrderPasswd(), sell_code, "1", "00", "{:.2f}".format(sell_price), "1") #모의 투자 비밀번호 사용
#            self.order.order_option(self.secinfo.getOptAccount(), self.secinfo.getOrderPasswd(), buy_code, "2", "00", "{:.2f}".format(buy_price), "1")
#            self.remained_burget = 0
#
#        self.access_db.saveToDB(df_call, df_put) #database에 call put 데이타 테이블을 저장한다. 
#  
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    optdata =  OptData() #ㅐ
    optscancon = OptScanContoller(optdata)
    myWindow = MyWindow(optscancon, optdata)
    myWindow.show()
    app.exec_()
    
