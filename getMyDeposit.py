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

class XAQueryEventHandlerCFOBQ10500:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerCFOBQ10500.query_state = 1   
        print("Balance Query has been arrived")

class XAQueryEventHandlert0441:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlert0441.query_state = 1   
        print("My Option Query has been completed")

    
class getMyDeposit:
    def __init__(self):
        #super().__init__()
        print("Deposit Scanner initialization")
        self.secinfo = secInfo()

    #--------------------------
# CFOAT00100  주식 주문
#--------------------------
    def scanDeposit(self):
       
        #계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량
        instXAQueryCFOBQ10500 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerCFOBQ10500)
        instXAQueryCFOBQ10500.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CFOBQ10500.res"
        instXAQueryCFOBQ10500.SetFieldData("CFOBQ10500InBlock1","RecCnt",0,10)
        instXAQueryCFOBQ10500.SetFieldData("CFOBQ10500InBlock1","AcntNo",0,self.secinfo.getOptAccount()) #계좌번호
        instXAQueryCFOBQ10500.SetFieldData("CFOBQ10500InBlock1","Pwd",0,self.secinfo.getOrderPasswd())   #계좌번호 암호
        instXAQueryCFOBQ10500.Request(0)
        
        
      
        print("Asking HTS query for deposit")
        
        while XAQueryEventHandlerCFOBQ10500.query_state == 0:
            pythoncom.PumpWaitingMessages()
        XAQueryEventHandlerCFOBQ10500.query_state = 0
        print("deposit query arrived")
        
        RecCnt = instXAQueryCFOBQ10500.GetFieldData("CFOBQ10500OutBlock1", "RecCnt",0)             
        AcntNo = instXAQueryCFOBQ10500.GetFieldData("CFOBQ10500OutBlock1", "AcntNo",0)         
        InptPwd = instXAQueryCFOBQ10500.GetFieldData("CFOBQ10500OutBlock1", "Pwd",0)                   

        #print(RecCnt,AcntNo,InptPwd)
        
        DpsamtTotamt = instXAQueryCFOBQ10500.GetFieldData("CFOBQ10500OutBlock2", "DpsamtTotamt",0)             #예탁금총액
        OrdAbleAmt = instXAQueryCFOBQ10500.GetFieldData("CFOBQ10500OutBlock2", "OrdAbleAmt",0)     #주문가능금액
        
        
        #print("예탁금 총액",  DpsamtTotamt, "주문가능금액", OrdAbleAmt)
        
        """       count = instXAQueryCCEAQ50600.GetBlockCount("CCEAQ50600OutBlock3")
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
        """        
        return DpsamtTotamt
    
    
    def scanMyOpt(self):
         #계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량
        instXAQueryt0441 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlert0441)
        instXAQueryt0441.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t0441.res"
        instXAQueryt0441.SetFieldData("t0441InBlock","accno",0,self.secinfo.getOptAccount()) #계좌번호
        instXAQueryt0441.SetFieldData("t0441InBlock","passwd",0,self.secinfo.getOrderPasswd())   #계좌번호 암호
        instXAQueryt0441.SetFieldData("t0441InBlock","cts_expcode",0,"")
        instXAQueryt0441.SetFieldData("t0441InBlock","cts_medocd",0,"")
        instXAQueryt0441.Request(0)
        
           
        while XAQueryEventHandlert0441.query_state == 0:
            pythoncom.PumpWaitingMessages()
        XAQueryEventHandlert0441.query_state = 0
        
        tdtsunik = instXAQueryt0441.GetFieldData("t0441OutBlock", "tdtsunik",0)             
        tappamt = instXAQueryt0441.GetFieldData("t0441OutBlock", "tappamt",0)         
        tsunik = instXAQueryt0441.GetFieldData("t0441OutBlock", "tsunik",0)                   

        #print(tdtsunik,tappamt,tsunik)
        
        count = instXAQueryt0441.GetBlockCount("t0441OutBlock1")
       # print("option count ",count)
        deposit_stack = np.array([[0,0,0,0,0,0,0]])
        for i in range(count):
            expcode = instXAQueryt0441.GetFieldData("t0441OutBlock1", "expcode",i) #종목번호
            #종목명 = instXAQueryt0441.GetFieldData("t0441OutBlock1", "IsuNm",i)  #종목명
            medosu = instXAQueryt0441.GetFieldData("t0441OutBlock1", "medosu",i) #매매구분 매수 0 매도 1
            if medosu == "매도":
                medosu_no = 1
            elif medosu == "매수":
                medosu_no = 0
            
            jqty = instXAQueryt0441.GetFieldData("t0441OutBlock1", "jqty",i) #미결재수량
            pamt = instXAQueryt0441.GetFieldData("t0441OutBlock1", "pamt",i) #평균가
            price = instXAQueryt0441.GetFieldData("t0441OutBlock1", "price",i) #현재가
            appamt = instXAQueryt0441.GetFieldData("t0441OutBlock1", "appamt",i) #평가금액
            #print( expcode, expcode, medosu, medosu_no, jqty, pamt, price, appamt)
            optinfo = [expcode, expcode, medosu_no, jqty, pamt, price, appamt]
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
    print("예탁금총액", mydeposit.scanDeposit())
    print("보유옵션",mydeposit.scanMyOpt())
    
    
    #xreal.start("201P7270")
    #while xreal.count < 100:
     #   pythoncom.PumpWaitingMessages()