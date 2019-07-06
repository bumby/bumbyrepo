# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 23:00:46 2019

@author: USER
"""
import win32com.client
import pythoncom

class XASessionEventHandler:
    login_state = 0
    
    def OnLogin(self, code, msg):
        if code == "0000":
            print("로그인성공")
            XASessionEventHandler.login_state = 1
        else:
            print("로그인실패")
       

class XReal_NWS_:
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
        print("tr_code = ", tr_code)
        self.count += 1
        date = self.GetFieldData("OutBlock", "date")
        time = self.GetFieldData("OutBlock", "time")
        id = self.GetFieldData("OutBlock", "id")
        realkey = self.GetFieldData("OutBlock", "realkey")
        title = self.GetFieldData("OutBlock", "title")
        code = self.GetFieldData("OutBlock", "code")
        bodysize = self.GetFieldData("OutBlock", "bodysize")
        print(self.count, date, time, id, realkey)
        print(title)

    def start(self):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\NWS.res" # RES 파일 등록
        self.SetFieldData("InBlock", "nwcode", "NWS001")
        self.AdviseRealData() # 실시간데이터 요청


    def end(self):
        self.UnadviseRealData() # 실시간데이터 요청 모두 취소

    @classmethod
    def get_instance(cls):
        xreal = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", cls)
        return xreal
       
 



if __name__ == "__main__":


    xreal = XReal_NWS_.get_instance()
    xreal.start()
    while xreal.count < 100:
        pythoncom.PumpWaitingMessages()