# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 00:01:47 2019

@author: USER
"""
try:
    import win32com.client
    import pythoncom
except:
    print("no window communication")


from sec_info import *
    
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
        print("Order query has been completed")
    


class XAQueryEventHandlert0434:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlert0434.query_state = 1   
        print("check chegyol query has been completed")
    

class XAQueryEventHandlerCFOAT00300:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerCFOAT00300.query_state = 1   
        print("Cancel query has been completed")
    
  


class OptOrder:
    def __init__(self):
        super().__init__()
        self.secinfo = secInfo() 

#--------------------------
# CFOAT00100  선물옵션 주문
#--------------------------

    def order_option(self, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량):
       
        #계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량
        instXAQueryCFOAT00100 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerCFOAT00100)
        instXAQueryCFOAT00100.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CFOAT00100.res"
        #instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","AcntNo",0,계좌번호)
        #instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","Pwd",0,비밀번호)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","AcntNo",0,self.secinfo.getOptAccount())
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","Pwd",0,self.secinfo.getOrderPasswd())
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","FnoIsuNo",0,선물옵션종목번호)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","BnsTpCode",0,매매구분)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","FnoOrdprcPtnCode",0,선물옵션호가유형코드)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","OrdPrc",0,주문가격)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","OrdQty",0,주문수량)
        instXAQueryCFOAT00100.Request(0)
         
        print("주문내용 ",self.secinfo.getOptAccount(), self.secinfo.getOrderPasswd(), 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량)
        
        while XAQueryEventHandlerCFOAT00100.query_state == 0:
            pythoncom.PumpWaitingMessages()
        #print("매수매도 쿼리 ", XAQueryEventHandlerCFOAT00100.query_state )
        XAQueryEventHandlerCFOAT00100.query_state = 0
        
        OrdNo = instXAQueryCFOAT00100.GetFieldData("CFOAT00100OutBlock2", "OrdNo",0)            #주문번호
        return OrdNo
   
        
    def check_chegyol(self, 종목번호, 주문번호):
        instXAQueryt0434 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlert0434)
        instXAQueryt0434.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t0434.res"
        instXAQueryt0434.SetFieldData("t0434InBlock","accno",0,self.secinfo.getOptAccount())
        instXAQueryt0434.SetFieldData("t0434InBlock","passwd",0,self.secinfo.getOrderPasswd())
        instXAQueryt0434.SetFieldData("t0434InBlock","expcode",0,종목번호)
        instXAQueryt0434.SetFieldData("t0434InBlock","chegb",0,0)
        instXAQueryt0434.SetFieldData("t0434InBlock","sortgb",0,1)
        instXAQueryt0434.SetFieldData("t0434InBlock","cts_ordno",0,주문번호)
        instXAQueryt0434.Request(0)
        
        #print("체결 확인중")
        while XAQueryEventHandlert0434.query_state == 0:
            pythoncom.PumpWaitingMessages()
        #print("체결확인 쿼리 ", XAQueryEventHandlert0434.query_state )
        XAQueryEventHandlert0434.query_state = 0
        
        qty    = instXAQueryt0434.GetFieldData("t0434OutBlock1", "qty",0)            #체결수량
        cheqty = instXAQueryt0434.GetFieldData("t0434OutBlock1", "cheqty",0)            #체결수량
        ordrem = instXAQueryt0434.GetFieldData("t0434OutBlock1", "ordrem",0)            #미체결 잔량
        return qty, cheqty, ordrem


    def cancel_option(self, 선물옵션종목번호, 원주문번호, 취소수량):
        #계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량
        instXAQueryCFOAT00300 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerCFOAT00300)
        instXAQueryCFOAT00300.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CFOAT00300.res"
        
        instXAQueryCFOAT00300.SetFieldData("CFOAT00300InBlock1","AcntNo",0,self.secinfo.getOptAccount())
        instXAQueryCFOAT00300.SetFieldData("CFOAT00300InBlock1","Pwd",0,self.secinfo.getOrderPasswd())
        instXAQueryCFOAT00300.SetFieldData("CFOAT00300InBlock1","FnoIsuNo",0,선물옵션종목번호)
        instXAQueryCFOAT00300.SetFieldData("CFOAT00300InBlock1","OrgOrdNo",0,원주문번호)
        instXAQueryCFOAT00300.SetFieldData("CFOAT00300InBlock1","CancQty",0,취소수량)
        instXAQueryCFOAT00300.Request(0)
         
        print("취소내용 ",self.secinfo.getOptAccount(), self.secinfo.getOrderPasswd(), 선물옵션종목번호, 원주문번호, 취소수량)
        
        while XAQueryEventHandlerCFOAT00300.query_state == 0:
            pythoncom.PumpWaitingMessages()
        #print("취소 쿼리 ", XAQueryEventHandlerCFOAT00300.query_state )
        XAQueryEventHandlerCFOAT00300.query_state = 0
        
        #OrdNo = instXAQueryCFOAT00300.GetFieldData("CFOAT00300OutBlock2", "OrdNo",0)            #주문번호
        #return OrdNo       

        
        
        
        

class OptOrderSimul:
    def __init__(self):
        super().__init__()
        
        #self.comm_connect()
        
         
#--------------------------
# CFOAT00100  주식 주문
#--------------------------
    def order_option(self, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량):
       
        #계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량
         
        print("주문내용 ", 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량)



try:
    from bestConnect import *
except:
    print("no window communication")


import time
if __name__ == "__main__":
 #   app = QApplication(sys.argv)
    
    secinfo = secInfo()                        #계좌 정보 holder
    best = BestAccess()                        #Login class 생성
    accounts_list = best.comm_connect(secinfo) #Login 

    optorder = OptOrder()
    orderno = optorder.order_option("301Q3270" , "2", "00", "7.30", "1")
    print("orderno",orderno)
    cheq = 0
    allowabletime = 0
    while cheq != 1 :
        cheq, ordrem = optorder.check_chegyol("301Q3270",orderno)
        print("주문번호",orderno, "체결량",cheq, "미체결잔량",  ordrem)
        time.sleep(1)
        allowabletime = allowabletime + 1
        if allowabletime == 10:
            optorder.cancel_option( "301Q3270", orderno, "1")
            break
    print("done")
    