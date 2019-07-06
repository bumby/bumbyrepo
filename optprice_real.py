# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 23:22:36 2019

@author: USER
"""


import win32com.client
import pythoncom


class XReal_OC0_:
    def __init__(self):
        super().__init__()
        self.count = 0
        self.comm_connect()

    def comm_connect(self):
        instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession" , XASessionEventHandler)

        id = "wangsisi"
        passwd = "siyoon77"
        cert_passwd = "siyoon77!!"
        
#실투자
        #instXASession.ConnectServer("hts.ebestsec.co.kr",20001)
#모의투자
        instXASession.ConnectServer("demo.ebestsec.co.kr",20001)
        instXASession.Login(id,passwd,cert_passwd,0,0)

        while XASessionEventHandler.login_state == 0:
            pythoncom.PumpWaitingMessages()
            
        num_account = instXASession.GetAccountListCount()
 
        account = []
        for i in range(num_account):
        #    account = instXASession.GetAccountList(i)
             account.append(instXASession.GetAccountList(i))   
        
        print(account)
            
        return account
    
    def OnReceiveRealData(self, tr_code): # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.count += 1
        체결시간 = self.GetFieldData("OutBlock", "chetime")
        전일대비구분 = self.GetFieldData("OutBlock", "sign")
        전일대비 = self.GetFieldData("OutBlock", "change")
        등락율 = self.GetFieldData("OutBlock", "drate")
        현재가 = self.GetFieldData("OutBlock", "price")
        시가 = self.GetFieldData("OutBlock", "open")
        고가 = self.GetFieldData("OutBlock", "high")
        저가 = self.GetFieldData("OutBlock", "low")
        체결구분 = self.GetFieldData("OutBlock", "cgubun")
        체결량 = self.GetFieldData("OutBlock", "cvolume")
        누적거래량 = self.GetFieldData("OutBlock", "volume")
        누적거래대금 = self.GetFieldData("OutBlock", "value")
        매도누적체결량 = self.GetFieldData("OutBlock", "mdvolume")
        매도누적체결건수 = self.GetFieldData("OutBlock", "mdchecnt")
    
        매수누적체결량 = self.GetFieldData("OutBlock", "msvolume")
        매수누적체결건수 = self.GetFieldData("OutBlock", "mschecnt")
        체결강도 = self.GetFieldData("OutBlock", "cpower")
        매도호가1 = self.GetFieldData("OutBlock", "offerho1")
        매수호가2 = self.GetFieldData("OutBlock", "bidho1")
        미결제약정수량 = self.GetFieldData("OutBlock", "openyak")
        KOSPI200지수 = self.GetFieldData("OutBlock", "k200jisu")
        KOSPI등가 = self.GetFieldData("OutBlock", "eqva")
        
        이론가 = self.GetFieldData("OutBlock", "theoryprice")
        내재변동성 = self.GetFieldData("OutBlock", "impv")
        미결제약정증감 = self.GetFieldData("OutBlock", "openyakcha")
        시간가치 = self.GetFieldData("OutBlock", "timevalue")
        
        장운영정보 = self.GetFieldData("OutBlock", "jgubun")
        전일동시간대거래량 = self.GetFieldData("OutBlock", "jnilvolume")
        단축코드 = self.GetFieldData("OutBlock", "optcode")
        
        
        print(self.count, 체결시간, 현재가, 시가, 매도호가1, 매수호가1)
        print(단축코드)

    def start(self, optcode):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\OC0.res" # RES 파일 등록
        self.SetFieldData("InBlock", "optcode", optcode)
        self.AdviseRealData() # 실시간데이터 요청

    def add_item(self, optcode):

        # 실시간데이터 요청 종목 추가
        #self.SetFieldData("InBlock", "shcode", stockcode)
        self.SetFieldData("InBlock", "optcode", optcode)
        self.AdviseRealData()

    def remove_item(self, optcode):
        # stockcode 종목만 실시간데이터 요청 취소
        self.UnadviseRealDataWithKey(optcode)

    def end(self):
        self.UnadviseRealData() # 실시간데이터 요청 모두 취소

    @classmethod
    def get_instance(cls):
        xreal = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", cls)
        return xreal
       
        



class XASessionEventHandler:
    login_state = 0
    
    def OnLogin(self, code, msg):
        if code == "0000":
            print("로그인성공")
            XASessionEventHandler.login_state = 1
        else:
            print("로그인실패")



    
if __name__ == "__main__":
 #   app = QApplication(sys.argv)
    

    xreal = XReal_OC0_.get_instance()
    xreal.start("201P7270")
    while xreal.count < 100:
        pythoncom.PumpWaitingMessages()