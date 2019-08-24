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
from PyOptHogaMon import *
from DBanal import *
from opt_order_tr import *
from sec_info import *

import pandas as pd
import sqlite3
import datetime

from subject import *
from observer import *


form_class = uic.loadUiType("mainwindowv03.ui")[0]

class accessDB:
    def __init__(self):
        self.con = sqlite3.connect("D:\work\Y2018\option\kospi.db")
        
    def saveToDB(self, calltable, puttable):
        print("data 저장")
        dt = datetime.datetime.now().strftime("%y%m%d%H%M%S")
       
        call_table_name = "call"+dt
        calltable.to_sql(call_table_name, self.con, if_exists='replace')
       
        put_table_name = "put"+dt
        puttable.to_sql(put_table_name, self.con, if_exists='replace')
        print("data 저장끝")


class MyWindow(QMainWindow, form_class, Observer):
    def __init__(self):
        super().__init__()

        #subject 생성
        self.optdata = OptData() #ㅐ
        
        
        #로그인 프로세스
        self.secinfo = secInfo()
        self.best = BestAccess()
        self.accounts_list = self.best.comm_connect(self.secinfo)
     
        self.passwd =  self.secinfo.getOrderPasswd()  
        
        self.setupUi(self)
                
        self.Option_expiration_mon = "201909"
        #self.optmon = PyOptHogaMon()
        self.optmon = PyOptHogaMon.get_instance()
        #opthogamon observer 등록
        self.optmon.register_subject(self.optdata)
      
        #자신을 observer로 등록
        self.register_subject(self.optdata)  
        
        
        
        
        self.optmon.start(self.Option_expiration_mon)        
           
        #db 분석 정의 
        self.dbanal = DBalalysis()
       
        #sell 주문
        self.order = XReal_CFOAT00100_()
        
        
        self.lineEdit.textChanged.connect(self.code_changed)
        self.pushButton.clicked.connect(self.send_order)
        self.pushButton_2.clicked.connect(self.check_balance)
        
        #timer2
        self.timer2 = QTimer(self)
        #self.timer2.start(1000*4)
        #self.timer2.timeout.connect(self.timeout2)
       
        self.remained_burget = 1
        self.access_db = accessDB()
        
          
#------------------------------observer implementaion ---------------        
    def update(self, 호가시간_, 매도호가1_, 매수호가1_, 단축코드_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        self.호가시간=호가시간_
        self.매도호가1=매도호가1_
        self.매수호가1=매수호가1_
        self.단축코드=단축코드_
        
        self.display()
        self.updateGuiOptHoga()

    def register_subject(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def display(self):
        print ("Gui updated")

    def updateGuiOptHoga(self):
        itemcount = len(self.subject.optHogaChart)
        for j in range(itemcount):
          #  item = QTableWidgetItem(balcv[j][])
            item = QTableWidgetItem(self.subject.optHogaChart[j][0])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(j,0,item)  
          
            item = QTableWidgetItem(self.subject.optHogaChart[j][1])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(j,1,item)
            
            item = QTableWidgetItem(self.subject.optHogaChart[j][2])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(j,2,item)
       
        self.tableWidget_2.setRowCount(itemcount)
        
        print("on construction print", itemcount)

#----------------------------------------------------------     
          
    
    def code_changed(self):
        print("code changed")
        code= self.lineEdit.text()
        name = self.best.get_master_code_name(code)
        self.lineEdit_2.setText(name)
        
    def send_order(self):
        order_type_lookup = {'신규매도':1, '신규매수':2}
        hoga_lookup = {'지정가':"00", '시장가':"03"}
                        
        #계좌번호, 비밀번호, 종목번호, 주문수량, 주문가, 매매구분, 호가유형코드, 신용거래코드, 대출일, 주문조건구분
        account = self.comboBox.currentText()

        code = self.lineEdit.text()
        OrdQty = self.spinBox.value()
        OrdPrc = self.spinBox_2.value()          
        BnsTpcode = self.comboBox_2.currentText()  #//매매구분
        OrdprcPtnCode = self.comboBox_3.currentText() #호가유형코드
        MgntrnCode = "000"
        LoanDt = ""
        OrdCndiTpCode = 0 # 0 없음 1 IOC 2 FOK

        ordrslt = self.best.order_stock(account, self.secinfo.getOrderPasswd(), code, OrdQty, OrdPrc, order_type_lookup[BnsTpcode], hoga_lookup[OrdprcPtnCode], MgntrnCode, LoanDt, OrdCndiTpCode)
         
        
        
    def check_balance(self):
        account = self.comboBox.currentText()
        sunamt1, mamt,tappamt,tdtsunik,sunamt,itemcount,balcv = self.best.get_curr_stock_balance(account,self.secinfo.getOrderPasswd())
        
        item = QTableWidgetItem(sunamt1)
        item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
        self.tableWidget.setItem(0,0,item)
        
        item = QTableWidgetItem(mamt)
        item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
        self.tableWidget.setItem(0,1,item)
        
        item = QTableWidgetItem(tappamt)
        item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
        self.tableWidget.setItem(0,2,item)
                
        item = QTableWidgetItem(tdtsunik)
        item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
        self.tableWidget.setItem(0,3,item)
        
        item = QTableWidgetItem(sunamt)
        item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
        self.tableWidget.setItem(0,5,item)
        
        self.tableWidget_2.setRowCount(itemcount)
        
  
    
        for j in range(itemcount):
            
            item = QTableWidgetItem(balcv['hname'][j])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(j,0,item)
                
            item = QTableWidgetItem(balcv['janqty'][j])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(j,1,item)
       
            item = QTableWidgetItem(balcv['mamt'][j])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(j,2,item)
                
            item = QTableWidgetItem(balcv['price'][j])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(j,3,item)
                
            item = QTableWidgetItem(balcv['dtsunik'][j])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(j,4,item)
                
            item = QTableWidgetItem(balcv['sunikrt'][j])
            item.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
            self.tableWidget_2.setItem(j,5,item)
        

    def timeout2(self):
        #database에 저장
        optresult, optresult2 = self.optmon.get_opt_chart(self.Option_expiration_mon)
    
        df_call = pd.DataFrame(optresult, columns = ['optcode','price','diff', 'volume', 'iv','offerho1','bidho1','theoryprice','impv','gmprice'], index=optresult['actprice'])
        df_put = pd.DataFrame(optresult2, columns = ['optcode','price','diff', 'volume', 'iv','offerho1','bidho1','theoryprice','impv','gmprice'], index=optresult['actprice'])
        

        #
        ATMS = [] #임시 
        ATMS, deal_signal, sell_code, sell_price, buy_code, buy_price = self.dbanal.extract_call_gap(df_call, 10.0, ATMS)
        print("sell ", sell_code, buy_code, deal_signal)
        
        print("주문 판단 중...")
        #def order_option(self, 계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량):
        if deal_signal == "yes" and self.remained_burget == 1:
            print(self.secinfo.getOptAccount(), self.secinfo.getOrderPasswd(), sell_code, "1", "00", "{:.2f}".format(sell_price), "1")
            self.order.order_option(self.secinfo.getOptAccount(), self.secinfo.getOrderPasswd(), sell_code, "1", "00", "{:.2f}".format(sell_price), "1") #모의 투자 비밀번호 사용
            self.order.order_option(self.secinfo.getOptAccount(), self.secinfo.getOrderPasswd(), buy_code, "2", "00", "{:.2f}".format(buy_price), "1")
            self.remained_burget = 0

        self.access_db.saveToDB(df_call, df_put) #database에 call put 데이타 테이블을 저장한다. 
  
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    
