# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 21:36:07 2020

@author: USER
"""

try:
    import win32com.client
    import pythoncom
except:
    print("opt purse simulation mode")

import numpy as np
from sec_info import *

class XAQueryEventHandlerCCEAQ50600:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerCCEAQ50600.query_state = 1   
        print("Order has been completed")


  

class getMyDeposit:
    def __init__(self):
        #super().__init__()
        print("Deposit Scanner initialization")
        self.secinfo = secInfo()

    #--------------------------
# CFOAT00100  주식 주문
#--------------------------
    def scanDeposit(self,   레코드갯수, 잔고평가구분, 선물가격평가구분):
       
        #계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량
        instXAQueryCCEAQ50600 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerCCEAQ50600)
        instXAQueryCCEAQ50600.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CCEAQ50600.res"
        instXAQueryCCEAQ50600.SetFieldData("CCEAQ50600InBlock1","RecCnt",0,레코드갯수)
        #instXAQueryCCEAQ50600.SetFieldData("CCEAQ50600InBlock1","AcntNo",0,계좌번호)
        #instXAQueryCCEAQ50600.SetFieldData("CCEAQ50600InBlock1","InptPwd",0,입력비밀번호)
        instXAQueryCCEAQ50600.SetFieldData("CCEAQ50600InBlock1","AcntNo",0,self.secinfo.getOptAccount())
        instXAQueryCCEAQ50600.SetFieldData("CCEAQ50600InBlock1","InptPwd",0,self.secinfo.getOrderPasswd())
        instXAQueryCCEAQ50600.SetFieldData("CCEAQ50600InBlock1","BalEvalTp",0,잔고평가구분)
        instXAQueryCCEAQ50600.SetFieldData("CCEAQ50600InBlock1","FutsPrcEvalTp",0,선물가격평가구분)
        instXAQueryCCEAQ50600.Request(0)
        
        print("주문내용 ",레코드갯수, self.secinfo.getOptAccount(),self.secinfo.getOrderPasswd(), 잔고평가구분, 선물가격평가구분)
        
      #
      
        while XAQueryEventHandlerCCEAQ50600.query_state == 0:
            pythoncom.PumpWaitingMessages()
        XAQueryEventHandlerCCEAQ50600.query_state = 0
        
        
        RecCnt = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock1", "RecCnt",0)             
        AcntNo = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock1", "AcntNo",0)         
        InptPwd = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock1", "InptPwd",0)                   
        BalEvalTp = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock1", "BalEvalTp",0)              
        FutsPrcEvalTp = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock1", "FutsPrcEvalTp",0)               
 #       gmchange = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock1", "gmchange",0)          
 #       gmdiff = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock1", "gmdiff",0)             
 #       gmvolume = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock1", "gmvolume",0)
 #       gmshcode = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock1", "gmshcode",0)
        print(RecCnt,AcntNo,InptPwd,BalEvalTp,FutsPrcEvalTp)
        
        평가예탁 = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock2", "EvalDpsamtTotamt",0)             
        print("평가예탁", 평가예탁)
        
        count = instXAQueryCCEAQ50600.GetBlockCount("CCEAQ50600OutBlock3")
        print(count)
        deposit_stack = np.array([[0,0,0,0,0,0,0]])
        for i in range(count):
            종목번호 = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock3", "FnoIsuNo",i)
            종목명 = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock3", "IsuNm",i)
            매매구분 = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock3", "BnsTpCode",i)
            미결재수량 = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock3", "UnsttQty",i)
            평균가 = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock3", "FnoAvrPrc",i)
            현재가 = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock3", "NowPrc",i)
            평가금액 = instXAQueryCCEAQ50600.GetFieldData("CCEAQ50600OutBlock3", "EvalPnl",i)
            print( 종목번호, 종목명, 매매구분, 미결재수량, 평균가, 현재가, 평가금액)
            optinfo = [종목번호, 종목명, 매매구분, 미결재수량, 평균가, 현재가, 평가금액]
            deposit_stack = np.vstack((deposit_stack,optinfo))
        deposit_stack = deposit_stack[1:count+1,:]
        return deposit_stack
        


try:
    from bestConnect import *
except:
    print("opt purse simulation mode")

if __name__ == "__main__":
 #   app = QApplication(sys.argv)
    
    secinfo = secInfo()                        #계좌 정보 holder
    best = BestAccess()                        #Login class 생성
    accounts_list = best.comm_connect(secinfo) #Login 


    mydeposit = getMyDeposit()
    mydeposit.scanDeposit(10, "1", "1")
    
    
    #xreal.start("201P7270")
    #while xreal.count < 100:
     #   pythoncom.PumpWaitingMessages()