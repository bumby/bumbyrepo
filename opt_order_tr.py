# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 00:01:47 2019

@author: USER
"""

import win32com.client
import pythoncom
from bestConnect import *
#
#class XASessionEventHandler:
#    login_state = 0
#    
#    def OnLogin(self, code, msg):
#        if code == "0000":
#            print("로그인성공")
#            XASessionEventHandler.login_state = 1
#        else:
#            print("로그인실패")
#

      
#주문 TR
class XAQueryEventHandlerCFOAT00100:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerCFOAT00100.query_state = 1   
        print("Order has been completed")
    
            

class OptOrder:
    def __init__(self):
        super().__init__()
        self.count = 0
        self. remained_TO = 1
        #self.comm_connect()
        
#        self.secinfo = secInfo()
#        self.optaccount = self.secinfo.getOptAccount()
#        self.passwd =  self.secinfo.getOrderPasswd()       
#            
#        self.best = BestAccess()
#        self.accounts_list = self.best.comm_connect(self.secinfo)
#        self.comboBox.addItems(self.accounts_list)

#    def comm_connect(self):
#        instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession" , XASessionEventHandler)
#
#        id =
#        passwd = 
#        cert_passwd = 
#        
##실투자
#        #instXASession.ConnectServer("hts.ebestsec.co.kr",20001)
##모의투자
#        instXASession.ConnectServer("demo.ebestsec.co.kr",20001)
#        instXASession.Login(id,passwd,cert_passwd,0,0)
#
#        while XASessionEventHandler.login_state == 0:
#            pythoncom.PumpWaitingMessages()
#            
#        num_account = instXASession.GetAccountListCount()
# 
#        account = []
#        for i in range(num_account):
#        #    account = instXASession.GetAccountList(i)
#             account.append(instXASession.GetAccountList(i))   
#        
#        print(account)
#            
#        return account
         
    #--------------------------
# CFOAT00100  주식 주문
#--------------------------
    def order_option(self, 계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량):
       
        #계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량
        instXAQueryCFOAT00100 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerCFOAT00100)
        instXAQueryCFOAT00100.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CFOAT00100.res"
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","AcntNo",0,계좌번호)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","Pwd",0,비밀번호)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","FnoIsuNo",0,선물옵션종목번호)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","BnsTpCode",0,매매구분)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","FnoOrdprcPtnCode",0,선물옵션호가유형코드)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","OrdPrc",0,주문가격)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","OrdQty",0,주문수량)
        instXAQueryCFOAT00100.Request(0)
         
        print("주문내용 ",계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량)
        
        self. remained_TO = 0
      #  while XAQueryEventHandlerCFOAT00100.query_state == 0:
      #      pythoncom.PumpWaitingMessages()
      #  XAQueryEventHandlerCFOAT00100.query_state = 0
      #  
      #  print( XAQueryEventHandlerCFOAT00100.query_state )

   
        

    
if __name__ == "__main__":
 #   app = QApplication(sys.argv)
    
    secinfo = secInfo()                        #계좌 정보 holder
    best = BestAccess()                        #Login class 생성
    accounts_list = best.comm_connect(secinfo) #Login 


    xreal = XReal_CFOAT00100_.get_instance()
    xreal.order_option("55551024561","0000","201P7270" , "1", "00", "0.37", "1")
    #xreal.start("201P7270")
    while xreal.count < 100:
        pythoncom.PumpWaitingMessages()