# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 13:28:40 2018

@author: USER
"""


from sec_info import *
import win32com.client
import pythoncom


class XASessionEventHandler:
    login_state=0
    
    def OnLogin(self, code, msg):
        if code == "0000":
            print("로그인성공")
            XASessionEventHandler.login_state = 1
        else:
            print("로그인실패")
 

    
    
class BestAccess:
    
    #def __init__(self):
     
        
        
    def comm_connect(self, sec_info):
        instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession" , XASessionEventHandler)

        id = sec_info.getLoginID()
        passwd = sec_info.getLoginPasswd()
        cert_passwd = sec_info.getCertPasswd()

#실투자
       # instXASession.ConnectServer("hts.ebestsec.co.kr",20001)
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
         


if __name__== "__main__":
    secinfo = secInfo() #계좌 정보 holder
    
    bestaccess = BestAccess()
    bestaccess.comm_connect(secinfo)
