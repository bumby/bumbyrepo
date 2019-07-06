# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 13:28:40 2018

@author: USER
"""

from sec_info import *

import matplotlib.pyplot as plt
#import matplotlib.finance as matfin

import win32com.client
import pandas as pd
import pythoncom
import sqlite3

class XASessionEventHandler:
    login_state=0
    
    def OnLogin(self, code, msg):
        if code == "0000":
            print("로그인성공")
            XASessionEventHandler.login_state = 1
        else:
            print("로그인실패")
 

class XAQueryEventHandlerT1102:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT1102.query_state = 1           
            
        
      
class XAQueryEventHandlerT8430:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT8430.query_state = 1           
            
class XAQueryEventHandlerT8413:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT8413.query_state = 1 
        
        
class XAQueryEventHandlerT0424:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT0424.query_state = 1 
      
#주문 TR
class XAQueryEventHandlerCSPAT00600:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerCSPAT00600.query_state = 1   
    
    
#주문 TR
class XAQueryEventHandlerCFOAT00100:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerCFOAT00100.query_state = 1   
    
    
    
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
         
#--------------------------
# t1102 주식 조회
#--------------------------

    def get_master_code_name(self, code):
        
        instXAQueryT1102 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT1102)
        instXAQueryT1102.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t1102.res"
        instXAQueryT1102.SetFieldData("t1102InBlock","shcode",0,code)
        instXAQueryT1102.Request(0)
        
        while XAQueryEventHandlerT1102.query_state == 0:
            pythoncom.PumpWaitingMessages()
        
        
        name = instXAQueryT1102.GetFieldData("t1102OutBlock","hname",0)
        price = instXAQueryT1102.GetFieldData("t1102OutBlock", "price",0)
        
        print(name)
        print(price)
        XAQueryEventHandlerT1102.query_state = 0
        return name
    
    
#    def send_order(self, account, order_type, code, num, price, hoga):
    def get_curr_stock_balance(self,accno,passwd):
        instXAQueryT0424 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT0424)
        instXAQueryT0424.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t0424.res"
        instXAQueryT0424.SetFieldData("t0424InBlock","accno",0,accno)
        instXAQueryT0424.SetFieldData("t0424InBlock","passwd",0,passwd)
        instXAQueryT0424.SetFieldData("t0424InBlock","prcgb",0,1) #단가구분 1: 평균 2: BEP
        instXAQueryT0424.SetFieldData("t0424InBlock","chegb",0,0) #체결구분 0: 결재기준  2: 체결기준 
        instXAQueryT0424.SetFieldData("t0424InBlock","dangb",0,0) #단일가구분 0:정규장 1:시간외단일가 
        instXAQueryT0424.SetFieldData("t0424InBlock","charge",0,1) #제비용 포함여부 0:제비용미포함 1:제비용포함
        instXAQueryT0424.SetFieldData("t0424InBlock","cts_expcode",0," ") #제비용 포함여부 0:제비용미포함 1:제비용포함
        instXAQueryT0424.Request(0)
        
        
        while XAQueryEventHandlerT0424.query_state == 0:
            pythoncom.PumpWaitingMessages()
            
        
        sunamt1 = instXAQueryT0424.GetFieldData("t0424OutBlock","sunamt1",0)
        mamt    = instXAQueryT0424.GetFieldData("t0424OutBlock","mamt",0)
        tappamt = instXAQueryT0424.GetFieldData("t0424OutBlock","tappamt",0)
        tdtsunik= instXAQueryT0424.GetFieldData("t0424OutBlock","tdtsunik",0)
        sunamt  = instXAQueryT0424.GetFieldData("t0424OutBlock","sunamt",0)
        
        count = instXAQueryT0424.GetBlockCount("t0424OutBlock1")
        
        balcv = {'hname':[], 'janqty':[], 'mamt':[], 'price':[], 'dtsunik':[], 'sunikrt':[]}
        for i in range(count):       
            hname = instXAQueryT0424.GetFieldData("t0424OutBlock1", "hname",i)
            janqty = instXAQueryT0424.GetFieldData("t0424OutBlock1", "janqty",i)
            mamt = instXAQueryT0424.GetFieldData("t0424OutBlock1", "mamt",i)
            price = instXAQueryT0424.GetFieldData("t0424OutBlock1", "price",i)
            dtsunik = instXAQueryT0424.GetFieldData("t0424OutBlock1", "dtsunik",i)
            sunikrt = instXAQueryT0424.GetFieldData("t0424OutBlock1", "sunikrt",i)
           
            balcv['hname'].append(hname)
            balcv['janqty'].append(janqty)
            balcv['mamt'].append(mamt)
            balcv['price'].append(price)
            balcv['dtsunik'].append(dtsunik)
            balcv['sunikrt'].append(sunikrt) 
        
        XAQueryEventHandlerT0424.query_state = 0
        return sunamt1, mamt,tappamt,tdtsunik,sunamt,count,balcv

    
#--------------------------
# t8413  차트
#--------------------------  
    def get_chart(self):
    
        instXAQueryT8413 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT8413)
        instXAQueryT8413.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t8413.res"
        instXAQueryT8413.SetFieldData("t8413InBlock","shcode",0,"078020")
        instXAQueryT8413.SetFieldData("t8413InBlock","gubun",0,"2")
        instXAQueryT8413.SetFieldData("t8413InBlock","sdate",0,"20180111")
        instXAQueryT8413.SetFieldData("t8413InBlock","edate",0,"20180622")
        instXAQueryT8413.SetFieldData("t8413InBlock","comp_yn",0,"N")
        instXAQueryT8413.Request(0)
        
        while XAQueryEventHandlerT8413.query_state == 0:
            pythoncom.PumpWaitingMessages()
        XAQueryEventHandlerT8413.query_state = 0
        
        count = instXAQueryT8413.GetBlockCount("t8413OutBlock1")
        
        ohlcv = {'date':[], 'open':[], 'high':[], 'low':[], 'close':[]}
        
        for i in range(count):
            date = instXAQueryT8413.GetFieldData("t8413OutBlock1", "date",i)
            open = instXAQueryT8413.GetFieldData("t8413OutBlock1", "open",i)
            high = instXAQueryT8413.GetFieldData("t8413OutBlock1", "high",i)
            low = instXAQueryT8413.GetFieldData("t8413OutBlock1", "low",i)
            close = instXAQueryT8413.GetFieldData("t8413OutBlock1", "close",i)
            jdiff_vol = instXAQueryT8413.GetFieldData("t8413OutBlock1", "jdiff_vol",i)
            
            ohlcv['date'].append(date)
            ohlcv['open'].append(open)
            ohlcv['high'].append(high)
            ohlcv['low'].append(low)
            ohlcv['close'].append(close)
            ohlcv['jdiff_vol'].append(jdiff_vol)
            print(date, open, high, low, close, jdiff_vol)
            
            
                
#--------------------------
# CSPAT00600  주식 주문
#--------------------------
    def order_stock(self, account, InptPwd, IsuNo, OrdQty, OrdPrc, BnsTpCode, OrdprcPtnCode, MgntrnCode, LoanDt, OrdCndiTpCode):
        
        #계좌번호, 비밀번호, 종목번호, 주문수량, 주문가, 매매구분, 호가유형코드, 신용거래코드, 대출일, 주문조건구분
        instXAQueryCSPAT00600 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerCSPAT00600)
        instXAQueryCSPAT00600.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CSPAT00600.res"
        instXAQueryCSPAT00600.SetFieldData("CSPAT00600InBlock1","AcntNo",0,account)
        instXAQueryCSPAT00600.SetFieldData("CSPAT00600InBlock1","InptPwd",0,InptPwd)
        instXAQueryCSPAT00600.SetFieldData("CSPAT00600InBlock1","IsuNo",0,IsuNo)
        instXAQueryCSPAT00600.SetFieldData("CSPAT00600InBlock1","OrdQty",0,OrdQty)
        instXAQueryCSPAT00600.SetFieldData("CSPAT00600InBlock1","OrdPrc",0,OrdPrc)
        instXAQueryCSPAT00600.SetFieldData("CSPAT00600InBlock1","BnsTpCode",0,BnsTpCode)
        instXAQueryCSPAT00600.SetFieldData("CSPAT00600InBlock1","OrdprcPtnCode",0,OrdprcPtnCode)
        instXAQueryCSPAT00600.SetFieldData("CSPAT00600InBlock1","MgntrnCode",0,MgntrnCode)
        instXAQueryCSPAT00600.SetFieldData("CSPAT00600InBlock1","LoanDt",0,LoanDt)
        instXAQueryCSPAT00600.SetFieldData("CSPAT00600InBlock1","OrdCndiTpCode",0,OrdCndiTpCode)  
        instXAQueryCSPAT00600.Request(0)
        
        while XAQueryEventHandlerCSPAT00600.query_state == 0:
            pythoncom.PumpWaitingMessages()
        XAQueryEventHandlerCSPAT00600.query_state = 0
        
        print( XAQueryEventHandlerCSPAT00600.query_state )
 


    
#--------------------------
# CFOAT00100  주식 주문
#--------------------------
    def order_option(self, 계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량):
        
        #계좌번호, 비밀번호, 선물옵션종목번호, 매매구분, 선물옵션호가유형코드, 주문가격, 주문수량
        instXAQueryCFOAT00100 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerCFOAT00100)
        instXAQueryCFOAT00100.ResFileName = "C:\\eBEST\\xingAPI\\Res\\CFOAT00100.res"
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","AcntNo",0,계좌번호)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","Pwd",0,비밀번호)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","FnolsuNo",0,선물옵션종목번호)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","BnsTpCode",0,매매구분)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","FnoOrdprcPtnCode",0,선물옵션호가유형코드)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","OrdPrc",0,주문가격)
        instXAQueryCFOAT00100.SetFieldData("CFOAT00100InBlock1","OrdQty",0,주문수량)
        instXAQueryCFOAT00100.Request(0)
        
        while XAQueryEventHandlerCFOAT00100.query_state == 0:
            pythoncom.PumpWaitingMessages()
        XAQueryEventHandlerCFOAT00100.query_state = 0
        
        print( XAQueryEventHandlerCFOAT00100.query_state )


       
#
#
#df = pd.DataFrame(ohlcv, columns = ['open','high', 'low', 'close'], index=ohlcv['date'])
#
#con = sqlite3.connect("D:\work\Y2018\option\kospi.db")
#df.to_sql('078020', con, if_exists='replace')
#
#
#if __name__== "__main__":
#    bestaccess = BestAccess()
#    bestaccess.comm_connect()
#    bestaccess.get_chart()