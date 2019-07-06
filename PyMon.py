# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 12:30:32 2018

@author: USER
"""

import sys
from PyQt5.QtWidgets import *
#import Kiwoom
import win32com.client
import pythoncom
import datetime
import time
from pandas import DataFrame

class XASessionEventHandler:
    login_state = 0
    
    def OnLogin(self, code, msg):
        if code == "0000":
            print("로그인성공")
            XASessionEventHandler.login_state = 1
        else:
            print("로그인실패")
            
class XAQueryEventHandlerT8413:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT8413.query_state = 1    

class XAQueryEventHandlerT8436:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT8436.query_state = 1    
  
    
class PyMon:
    def __init__(self):
        self.comm_connect()
     #   self.get_code_list()

            
    def comm_connect(self):
        instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession" , XASessionEventHandler)

        id = "wangsisi"
        passwd = "siyoon77"
        cert_passwd = "siyoon77!!"

#실투자
        instXASession.ConnectServer("hts.ebestsec.co.kr",20001)
#모의투자
        ##instXASession.ConnectServer("demo.ebestsec.co.kr",20001)
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
    
    def get_list_code(self):
        instXAQueryT8436 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT8436)
        instXAQueryT8436.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t8436.res"
        instXAQueryT8436.SetFieldData("t8436InBlock","gubun",0,0)  #전체 회사 검색
        instXAQueryT8436.Request(0)
        
        while XAQueryEventHandlerT8436.query_state == 0:
            pythoncom.PumpWaitingMessages()
        XAQueryEventHandlerT8436.query_state = 0
    
        count = instXAQueryT8436.GetBlockCount("t8436OutBlock")
        
        codelist = {'hname':[], 'shcode':[]}
        
        for i in range(count):
            hname = instXAQueryT8436.GetFieldData("t8436OutBlock", "hname",i)
            shcode = instXAQueryT8436.GetFieldData("t8436OutBlock", "shcode",i)
            
            codelist['hname'].append(hname)
            codelist['shcode'].append(shcode)
            print(hname, shcode)
        return codelist
    
    def get_ohlcv(self, shcode, start, today):
            
        instXAQueryT8413 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT8413)
        instXAQueryT8413.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t8413.res"
        instXAQueryT8413.SetFieldData("t8413InBlock","shcode",0,shcode)
        instXAQueryT8413.SetFieldData("t8413InBlock","gubun",0,"2")
        instXAQueryT8413.SetFieldData("t8413InBlock","sdate",0,start)
        instXAQueryT8413.SetFieldData("t8413InBlock","edate",0,today)
        instXAQueryT8413.SetFieldData("t8413InBlock","comp_yn",0,"N")
        instXAQueryT8413.Request(0)
        
        while XAQueryEventHandlerT8413.query_state == 0:
            pythoncom.PumpWaitingMessages()
        XAQueryEventHandlerT8413.query_state = 0
        
        count = instXAQueryT8413.GetBlockCount("t8413OutBlock1")
        print("count",count)
                
        ohlcv = {'date':[], 'open':[], 'high':[], 'low':[], 'close':[], 'volumn':[]}
        
        for i in range(count):
            date      = instXAQueryT8413.GetFieldData("t8413OutBlock1", "date",i)
            open      = instXAQueryT8413.GetFieldData("t8413OutBlock1", "open",i)
            high      = instXAQueryT8413.GetFieldData("t8413OutBlock1", "high",i)
            low       = instXAQueryT8413.GetFieldData("t8413OutBlock1", "low",i)
            close     = instXAQueryT8413.GetFieldData("t8413OutBlock1", "close",i)
            jdiff_vol = instXAQueryT8413.GetFieldData("t8413OutBlock1", "jdiff_vol",i)
            
            ohlcv['date'].append(date)
            ohlcv['open'].append(int(open))
            ohlcv['high'].append(int(high))
            ohlcv['low'].append(int(low))
            ohlcv['close'].append(int(close))
            ohlcv['volumn'].append(int(jdiff_vol))
           # print(date, open, high, low, close, jdiff_vol)
        df = DataFrame(ohlcv, columns = ['open','high', 'low', 'close', 'volumn'], index=ohlcv['date'])   
        df = df.sort_index(axis=0 , ascending =False)
       
        
        return df
        
        
    def check_speedy_rising_volumn(self,code,start,today):
       # today = datetime.datetime.today().strftime("%Y%m%d")
        print(code+","+today)
        df = self.get_ohlcv( code, start,today)
     

        volumes = df['volumn']
       # print(volumes)   
        if len(volumes)<21:
            return False
        sum_vol20 = 0
        today_vol = 0

        for i, vol in enumerate(volumes):
            
            if i==0:
                today_vol = vol
            elif 1 <= i <= 20:
                sum_vol20 += vol
            else:
                break
            
        avg_vol20 = sum_vol20 / 20
        print(avg_vol20, today_vol)
        if today_vol > avg_vol20*10:
            return True
        
    
        
     #   con = sqlite3.connect("D:\work\Y2018\option\kospi.db")
     #   df.to_sql('078020', con, if_exists='replace')
        
    def update_buy_list(self, buy_list):
        f = open("buy_list.txt", "wt")
        for code in buy_list:
            a = "매수;"+code+";시장가;10;0;매수전\n"
            f.writelines(a)
        f.close()
        
    
        
    def run(self):
        today = datetime.datetime.today().strftime("%Y%m%d")
        codelist = self.get_list_code()['shcode']
        #print(codelist)
        
        buy_list = []
        for i in codelist:
            time.sleep(3) # 너무 잦은 스캔 불가
            if self.check_speedy_rising_volumn(i,"20180820", today ):
                print("급등주")
                buy_list.append(i)
        self.update_buy_list(buy_list)
  
        print("run")
         
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pymon = PyMon()
    #pymon.get_list_code()
    pymon.run()
    