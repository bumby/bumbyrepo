# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 13:24:12 2019

@author: USER
"""

import sys
from PyQt5.QtWidgets import *
import win32com.client
import pythoncom

from pandas import DataFrame
import time
from subject import *
from observer import *
from timeManager import *
        
      
class XAQueryEventHandlerT2301:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT2301.query_state = 1           
              
      
            
#class PyOptHogaMon:
class PyOptHogaMon(Observer):
    def __init__(self):
        print("optmon has created")
        self.count = 0
        self.tmanager = timeManager() 
        self.subject = None
      
    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_, 이론가_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        self.호가시간=호가시간_
        self.단축코드=단축코드_
        self.매도호가1=매도호가1_
        self.매수호가1=매수호가1_
        self.이론가 = 이론가_
         
        self.display()

    def register_subject(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def display(self):
        #print ('호가시간:', self.호가시간, '단축코드:', self.단축코드 , '매도호가1:', self.매도호가1,'매수호가1:', self.매수호가1, '이론가:', self.이론가)
        pass     
#       self.comm_connect()
#   self.get_code_list()


#--------------------------
# t2301  차트
#--------------------------  
    def get_opt_chart(self, Option_expiration_mon):
    
        instXAQueryT2301 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT2301)
        instXAQueryT2301.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t2301.res"
        instXAQueryT2301.SetFieldData("t2301InBlock","yyyymm",0,Option_expiration_mon) #"201908" 형테
        instXAQueryT2301.SetFieldData("t2301InBlock","gubun",0,"G")
        instXAQueryT2301.Request(0)
        
        while XAQueryEventHandlerT2301.query_state == 0:
            pythoncom.PumpWaitingMessages()
        XAQueryEventHandlerT2301.query_state = 0
        
        histimpv = instXAQueryT2301.GetFieldData("t2301OutBlock", "histimpv",0)            #역사적 변동성
        jandatecnt = instXAQueryT2301.GetFieldData("t2301OutBlock", "jandatecnt",0) # 옵션 잔존일 
        cimpv = instXAQueryT2301.GetFieldData("t2301OutBlock", "cimpv",0)           #콜옵션 대표 IV
        pimpv = instXAQueryT2301.GetFieldData("t2301OutBlock", "pimpv",0)           #풋옵션 대표 IV
        gmprice = instXAQueryT2301.GetFieldData("t2301OutBlock", "gmprice",0)       #근월물 현재가
        gmsign = instXAQueryT2301.GetFieldData("t2301OutBlock", "gmsign",0)         #근월물 전일대비 구분
        gmchange = instXAQueryT2301.GetFieldData("t2301OutBlock", "gmchange",0)     #근월물 전일대비
        gmdiff = instXAQueryT2301.GetFieldData("t2301OutBlock", "gmdiff",0)         #근월물 등락율
        gmvolume = instXAQueryT2301.GetFieldData("t2301OutBlock", "gmvolume",0)
        gmshcode = instXAQueryT2301.GetFieldData("t2301OutBlock", "gmshcode",0)
        
#        print(histimpv, jandatecnt,cimpv,  pimpv )
        
        count = instXAQueryT2301.GetBlockCount("t2301OutBlock1")
        
        #ohlcv = {'date':[], 'open':[], 'high':[], 'low':[], 'close':[]}
        ohlcv = { 'actprice':[], 'optcode':[], 'price':[], 'diff':[], 'volume':[],  'iv':[],  'offerho1':[], 'bidho1':[], 'theoryprice':[], 'impv':[], 'gmprice':[]}
        
        for i in range(count):
            actprice = instXAQueryT2301.GetFieldData("t2301OutBlock1", "actprice",i)
            optcode = instXAQueryT2301.GetFieldData("t2301OutBlock1", "optcode",i)
            price = instXAQueryT2301.GetFieldData("t2301OutBlock1", "price",i)
            sign = instXAQueryT2301.GetFieldData("t2301OutBlock1", "sign",i)
            diff = instXAQueryT2301.GetFieldData("t2301OutBlock1", "diff",i)
           
            volume = instXAQueryT2301.GetFieldData("t2301OutBlock1", "volume",i)
            iv = instXAQueryT2301.GetFieldData("t2301OutBlock1", "iv",i)
            mgjv = instXAQueryT2301.GetFieldData("t2301OutBlock1", "mgjv",i)
            mgjvupdn = instXAQueryT2301.GetFieldData("t2301OutBlock1", "mgjvupdn",i)
            offerho1 = instXAQueryT2301.GetFieldData("t2301OutBlock1", "offerho1",i)
            
            bidho1 = instXAQueryT2301.GetFieldData("t2301OutBlock1", "bidho1",i)
            cvolume = instXAQueryT2301.GetFieldData("t2301OutBlock1", "cvolume",i)
            delt = instXAQueryT2301.GetFieldData("t2301OutBlock1", "delt",i)
            gama = instXAQueryT2301.GetFieldData("t2301OutBlock1", "gama",i)
            vega = instXAQueryT2301.GetFieldData("t2301OutBlock1", "vega",i)
            
            ceta = instXAQueryT2301.GetFieldData("t2301OutBlock1", "ceta",i)
            rhox = instXAQueryT2301.GetFieldData("t2301OutBlock1", "rhox",i)
            theoryprice = instXAQueryT2301.GetFieldData("t2301OutBlock1", "theoryprice",i)
            impv = instXAQueryT2301.GetFieldData("t2301OutBlock1", "impv",i)
            timevl = instXAQueryT2301.GetFieldData("t2301OutBlock1", "timevl",i)
            
            jvolume = instXAQueryT2301.GetFieldData("t2301OutBlock1", "jvolume",i)
            parpl = instXAQueryT2301.GetFieldData("t2301OutBlock1", "parpl",i)
            jngo = instXAQueryT2301.GetFieldData("t2301OutBlock1", "jngo",i)
            offerrem1 = instXAQueryT2301.GetFieldData("t2301OutBlock1", "offerrem1",i)
            bidrem1 = instXAQueryT2301.GetFieldData("t2301OutBlock1", "bidrem1",i)
            
            open = instXAQueryT2301.GetFieldData("t2301OutBlock1", "open",i)
            high = instXAQueryT2301.GetFieldData("t2301OutBlock1", "high",i)
            low = instXAQueryT2301.GetFieldData("t2301OutBlock1", "low",i)
            atmgubun = instXAQueryT2301.GetFieldData("t2301OutBlock1", "atmgubun",i)
            jisuconv = instXAQueryT2301.GetFieldData("t2301OutBlock1", "jisuconv",i)
            
            value = instXAQueryT2301.GetFieldData("t2301OutBlock1", "value",i)
       
            
            ohlcv['actprice'].append(actprice)
            ohlcv['optcode'].append(optcode)
            ohlcv['price'].append(price)
            ohlcv['diff'].append(diff)
            ohlcv['volume'].append(volume)
            ohlcv['iv'].append(iv)
            ohlcv['offerho1'].append(offerho1)
            ohlcv['bidho1'].append(bidho1)
            ohlcv['theoryprice'].append(theoryprice)
            ohlcv['impv'].append(impv)
            ohlcv['gmprice'].append(gmprice)
            
            print(actprice, optcode, price, sign,  diff, volume, iv, mgjv, mgjvupdn, offerho1, bidho1, cvolume, delt, gama, vega, ceta, rhox, theoryprice, cimpv)
            self.subject.change_optprice(timevl,optcode,offerho1,bidho1,theoryprice)
        
        count = instXAQueryT2301.GetBlockCount("t2301OutBlock2")
        
        #ohlcv = {'date':[], 'open':[], 'high':[], 'low':[], 'close':[]}
        ohlcv2 = {'actprice':[], 'optcode':[], 'price':[], 'diff':[], 'volume':[],  'iv':[],  'offerho1':[], 'bidho1':[], 'theoryprice':[], 'impv':[], 'gmprice':[]}
        
        for i in range(count):
            actprice2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "actprice",i)
            optcode2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "optcode",i)
            price2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "price",i)
            sign2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "sign",i)
            diff2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "diff",i)
           
            volume2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "volume",i)
            iv2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "iv",i)
            mgjv2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "mgjv",i)
            mgjvupdn2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "mgjvupdn",i)
            offerho12 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "offerho1",i)
            
            bidho12 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "bidho1",i)
            cvolume2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "cvolume",i)
            delt2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "delt",i)
            gama2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "gama",i)
            vega2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "vega",i)
            
            ceta2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "ceta",i)
            rhox2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "rhox",i)
            theoryprice2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "theoryprice",i)
            impv2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "impv",i)
            timevl2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "timevl",i)
            
            jvolume2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "jvolume",i)
            parpl2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "parpl",i)
            jngo2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "jngo",i)
            offerrem12 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "offerrem1",i)
            bidrem12 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "bidrem1",i)
            
            open2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "open",i)
            high2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "high",i)
            low2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "low",i)
            atmgubun2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "atmgubun",i)
            jisuconv2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "jisuconv",i)
            
            value2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "value",i)
            
           
            ohlcv2['actprice'].append(actprice2)
            ohlcv2['optcode'].append(optcode2)
            ohlcv2['price'].append(price2)
            ohlcv2['diff'].append(diff2)
            ohlcv2['volume'].append(volume2)
            ohlcv2['iv'].append(iv2)
            ohlcv2['offerho1'].append(offerho12)
            ohlcv2['bidho1'].append(bidho12)
            ohlcv2['theoryprice'].append(theoryprice2)
            ohlcv2['impv'].append(impv2)
            ohlcv2['gmprice'].append(gmprice)
                 
            print(actprice2,optcode2, price2, sign2,  diff2, volume2, iv2, mgjv2, mgjvupdn2, offerho12, bidho12, cvolume2, delt2, gama2, vega2, ceta2, rhox2, theoryprice2, pimpv)
            self.subject.change_optprice(timevl2,optcode2,offerho12,bidho12,theoryprice2)
        
#        self.subject.print_opt()
        return ohlcv, ohlcv2    
    
#--------------------------
# XReal_OC0_  Real data Acquisition
#--------------------------  

    def OnReceiveRealData(self, tr_code): # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.count += 1
        #호가시간 = self.GetFieldData("OutBlock", "hoime")
        
        호가시간 = self.tmanager.getCurrentDash()
        매도호가1 = self.GetFieldData("OutBlock", "offerho1")
        매수호가1 = self.GetFieldData("OutBlock", "bidho1")
        매도호가2 = self.GetFieldData("OutBlock", "offerho2")
        매수호가2 = self.GetFieldData("OutBlock", "bidho2")
        단축코드 = self.GetFieldData("OutBlock", "optcode")
        
        # 변경 
        #self.subject.change_optprice(호가시간,단축코드, 매도호가1,매수호가1,"")
        try:
            self.subject.change_hogaprice(호가시간,단축코드, 매도호가1, 매수호가1, 매도호가2, 매수호가2, "" )
            print("h")
        except:
            print("호가 모니터링 에러 발생")
        #print("호가발생", self.count, tr_code, 호가시간, 단축코드, 매도호가1, 매수호가1, 매도호가2, 매수호가2)
      





    def start(self,  Option_expiration_mon):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        optresult, optresult2 = self.get_opt_chart(Option_expiration_mon)
 
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\OH0.res" # RES 파일 등록
        #self.SetFieldData("InBlock", "optcode", optcode)
        #self.AdviseRealData() # 실시간데이터 요청
 
        for i in optresult['optcode']:
            self.add_item(i)
        
        for i in optresult2['optcode']:
            self.add_item(i)
            
        

    def add_item(self, optcode):
        # 실시간데이터 요청 종목 추가
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
 


#from thread import Thread
import threading
import time
from kospi200Simulation import * 
from OptModifier import OptModifier


class PyOptHogaMonSimul(Observer):
    def __init__(self):
        print("optmon has created")
        self.count = 0
        self.virtual_time_count = 0
        self.tmanager = timeManager() 
        self.subject = None
        self.opt_modifier = OptModifier()
      
    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_, 이론가_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        self.호가시간=호가시간_
        self.단축코드=단축코드_
        self.매도호가1=매도호가1_
        self.매수호가1=매수호가1_
        self.이론가 = 이론가_
         
        self.display()

    def register_subject(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def display(self):
        #print ('호가시간:', self.호가시간, '단축코드:', self.단축코드 , '매도호가1:', self.매도호가1,'매수호가1:', self.매수호가1, '이론가:', self.이론가)
        pass     
#       self.comm_connect()
#   self.get_code_list()


#--------------------------
# t2301  차트
#--------------------------  
    def get_opt_chart(self, Option_expiration_mon):
    
        instXAQueryT2301 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT2301)
        instXAQueryT2301.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t2301.res"
        instXAQueryT2301.SetFieldData("t2301InBlock","yyyymm",0,Option_expiration_mon) #"201908" 형테
        instXAQueryT2301.SetFieldData("t2301InBlock","gubun",0,"G")
        instXAQueryT2301.Request(0)
        
        while XAQueryEventHandlerT2301.query_state == 0:
            pythoncom.PumpWaitingMessages()
        XAQueryEventHandlerT2301.query_state = 0
        
        histimpv = instXAQueryT2301.GetFieldData("t2301OutBlock", "histimpv",0)            #역사적 변동성
        jandatecnt = instXAQueryT2301.GetFieldData("t2301OutBlock", "jandatecnt",0) # 옵션 잔존일 
        cimpv = instXAQueryT2301.GetFieldData("t2301OutBlock", "cimpv",0)           #콜옵션 대표 IV
        pimpv = instXAQueryT2301.GetFieldData("t2301OutBlock", "pimpv",0)           #풋옵션 대표 IV
        gmprice = instXAQueryT2301.GetFieldData("t2301OutBlock", "gmprice",0)       #근월물 현재가
        gmsign = instXAQueryT2301.GetFieldData("t2301OutBlock", "gmsign",0)         #근월물 전일대비 구분
        gmchange = instXAQueryT2301.GetFieldData("t2301OutBlock", "gmchange",0)     #근월물 전일대비
        gmdiff = instXAQueryT2301.GetFieldData("t2301OutBlock", "gmdiff",0)         #근월물 등락율
        gmvolume = instXAQueryT2301.GetFieldData("t2301OutBlock", "gmvolume",0)
        gmshcode = instXAQueryT2301.GetFieldData("t2301OutBlock", "gmshcode",0)
        
#        print(histimpv, jandatecnt,cimpv,  pimpv )
        
        count = instXAQueryT2301.GetBlockCount("t2301OutBlock1")
        
        #ohlcv = {'date':[], 'open':[], 'high':[], 'low':[], 'close':[]}
        ohlcv = { 'actprice':[], 'optcode':[], 'price':[], 'diff':[], 'volume':[],  'iv':[],  'offerho1':[], 'bidho1':[], 'theoryprice':[], 'impv':[], 'gmprice':[]}
        
        for i in range(count):
            actprice = instXAQueryT2301.GetFieldData("t2301OutBlock1", "actprice",i)
            optcode = instXAQueryT2301.GetFieldData("t2301OutBlock1", "optcode",i)
            price = instXAQueryT2301.GetFieldData("t2301OutBlock1", "price",i)
            sign = instXAQueryT2301.GetFieldData("t2301OutBlock1", "sign",i)
            diff = instXAQueryT2301.GetFieldData("t2301OutBlock1", "diff",i)
           
            volume = instXAQueryT2301.GetFieldData("t2301OutBlock1", "volume",i)
            iv = instXAQueryT2301.GetFieldData("t2301OutBlock1", "iv",i)
            mgjv = instXAQueryT2301.GetFieldData("t2301OutBlock1", "mgjv",i)
            mgjvupdn = instXAQueryT2301.GetFieldData("t2301OutBlock1", "mgjvupdn",i)
            offerho1 = instXAQueryT2301.GetFieldData("t2301OutBlock1", "offerho1",i)
            
            bidho1 = instXAQueryT2301.GetFieldData("t2301OutBlock1", "bidho1",i)
            cvolume = instXAQueryT2301.GetFieldData("t2301OutBlock1", "cvolume",i)
            delt = instXAQueryT2301.GetFieldData("t2301OutBlock1", "delt",i)
            gama = instXAQueryT2301.GetFieldData("t2301OutBlock1", "gama",i)
            vega = instXAQueryT2301.GetFieldData("t2301OutBlock1", "vega",i)
            
            ceta = instXAQueryT2301.GetFieldData("t2301OutBlock1", "ceta",i)
            rhox = instXAQueryT2301.GetFieldData("t2301OutBlock1", "rhox",i)
            theoryprice = instXAQueryT2301.GetFieldData("t2301OutBlock1", "theoryprice",i)
            impv = instXAQueryT2301.GetFieldData("t2301OutBlock1", "impv",i)
            timevl = instXAQueryT2301.GetFieldData("t2301OutBlock1", "timevl",i)
            
            jvolume = instXAQueryT2301.GetFieldData("t2301OutBlock1", "jvolume",i)
            parpl = instXAQueryT2301.GetFieldData("t2301OutBlock1", "parpl",i)
            jngo = instXAQueryT2301.GetFieldData("t2301OutBlock1", "jngo",i)
            offerrem1 = instXAQueryT2301.GetFieldData("t2301OutBlock1", "offerrem1",i)
            bidrem1 = instXAQueryT2301.GetFieldData("t2301OutBlock1", "bidrem1",i)
            
            open = instXAQueryT2301.GetFieldData("t2301OutBlock1", "open",i)
            high = instXAQueryT2301.GetFieldData("t2301OutBlock1", "high",i)
            low = instXAQueryT2301.GetFieldData("t2301OutBlock1", "low",i)
            atmgubun = instXAQueryT2301.GetFieldData("t2301OutBlock1", "atmgubun",i)
            jisuconv = instXAQueryT2301.GetFieldData("t2301OutBlock1", "jisuconv",i)
            
            value = instXAQueryT2301.GetFieldData("t2301OutBlock1", "value",i)
       
            
            ohlcv['actprice'].append(actprice)
            ohlcv['optcode'].append(optcode)
            ohlcv['price'].append(price)
            ohlcv['diff'].append(diff)
            ohlcv['volume'].append(volume)
            ohlcv['iv'].append(iv)
            ohlcv['offerho1'].append(offerho1)
            ohlcv['bidho1'].append(bidho1)
            ohlcv['theoryprice'].append(theoryprice)
            ohlcv['impv'].append(impv)
            ohlcv['gmprice'].append(gmprice)
            
            print(actprice, optcode, price, sign,  diff, volume, iv, mgjv, mgjvupdn, offerho1, bidho1, cvolume, delt, gama, vega, ceta, rhox, theoryprice, cimpv)
            self.subject.change_optprice(timevl,optcode,offerho1,bidho1,theoryprice)
        
        count = instXAQueryT2301.GetBlockCount("t2301OutBlock2")
        
        #ohlcv = {'date':[], 'open':[], 'high':[], 'low':[], 'close':[]}
        ohlcv2 = {'actprice':[], 'optcode':[], 'price':[], 'diff':[], 'volume':[],  'iv':[],  'offerho1':[], 'bidho1':[], 'theoryprice':[], 'impv':[], 'gmprice':[]}
        
        for i in range(count):
            actprice2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "actprice",i)
            optcode2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "optcode",i)
            price2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "price",i)
            sign2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "sign",i)
            diff2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "diff",i)
           
            volume2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "volume",i)
            iv2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "iv",i)
            mgjv2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "mgjv",i)
            mgjvupdn2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "mgjvupdn",i)
            offerho12 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "offerho1",i)
            
            bidho12 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "bidho1",i)
            cvolume2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "cvolume",i)
            delt2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "delt",i)
            gama2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "gama",i)
            vega2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "vega",i)
            
            ceta2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "ceta",i)
            rhox2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "rhox",i)
            theoryprice2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "theoryprice",i)
            impv2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "impv",i)
            timevl2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "timevl",i)
            
            jvolume2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "jvolume",i)
            parpl2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "parpl",i)
            jngo2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "jngo",i)
            offerrem12 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "offerrem1",i)
            bidrem12 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "bidrem1",i)
            
            open2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "open",i)
            high2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "high",i)
            low2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "low",i)
            atmgubun2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "atmgubun",i)
            jisuconv2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "jisuconv",i)
            
            value2 = instXAQueryT2301.GetFieldData("t2301OutBlock2", "value",i)
            
           
            ohlcv2['actprice'].append(actprice2)
            ohlcv2['optcode'].append(optcode2)
            ohlcv2['price'].append(price2)
            ohlcv2['diff'].append(diff2)
            ohlcv2['volume'].append(volume2)
            ohlcv2['iv'].append(iv2)
            ohlcv2['offerho1'].append(offerho12)
            ohlcv2['bidho1'].append(bidho12)
            ohlcv2['theoryprice'].append(theoryprice2)
            ohlcv2['impv'].append(impv2)
            ohlcv2['gmprice'].append(gmprice)
                 
            print(actprice2,optcode2, price2, sign2,  diff2, volume2, iv2, mgjv2, mgjvupdn2, offerho12, bidho12, cvolume2, delt2, gama2, vega2, ceta2, rhox2, theoryprice2, pimpv)
            self.subject.change_optprice(timevl2,optcode2,offerho12,bidho12,theoryprice2)
        
#        self.subject.print_opt()
        return ohlcv, ohlcv2    
    
#--------------------------
# XReal_OC0_  Real data Acquisition
#--------------------------  

    def OnReceiveRealData(self, tr_code): # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.count += 1
        #호가시간 = self.GetFieldData("OutBlock", "hoime")
        
        호가시간 = self.tmanager.getCurrentDash()
        매도호가1 = self.GetFieldData("OutBlock", "offerho1")
        매수호가1 = self.GetFieldData("OutBlock", "bidho1")
        매도호가2 = self.GetFieldData("OutBlock", "offerho2")
        매수호가2 = self.GetFieldData("OutBlock", "bidho2")
        단축코드 = self.GetFieldData("OutBlock", "optcode")
        
        # 변경 
        #self.subject.change_optprice(호가시간,단축코드, 매도호가1,매수호가1,"")
        try:
            self.subject.change_hogaprice(호가시간,단축코드, 매도호가1, 매수호가1, 매도호가2, 매수호가2, "" )
            print("h")
        except:
            print("호가 모니터링 에러 발생")
        #print("호가발생", self.count, tr_code, 호가시간, 단축코드, 매도호가1, 매수호가1, 매도호가2, 매수호가2)
      

    def OnReceiveVirtualData(self, tr_code):
        
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.virtual_time_count += 1
        print(" virtual 호가 event 발생") 
        호가시간 = self.tmanager.getCurrentDash()
        
        temp = self.subject.get_optChart()
        print("time ", self.virtual_time_count)
        
        호가시간, 단축코드, 매도호가1, 매수호가1, 매도호가2, 매수호가2, 이론값 = self.opt_modifier.random_modify_opt(temp, 호가시간)  # OptModifier의 random_modify_opt 메서드 호출하여 optChart 수정
        #opt_data.change_price(hogaTime, random_optCode, offerho1, bidho1, theoryprice)
    
        #try:
        #    self.subject.change_hogaprice(호가시간,단축코드, 매도호가1, 매수호가1, 매도호가2, 매수호가2, "" )
       
        #except:
        #    print("호가 모니터링 에러 발생")
        print("호가발생", self.count, tr_code, 호가시간, 단축코드, 매도호가1, 매수호가1,  매도호가2, 매수호가2)
       
        threading.Timer(0.1,self.OnReceiveVirtualData, args = ("dd",)).start()  
        
        return True


    def start(self,  Option_expiration_mon):
        """
        이베스트 서버에 실시간 data 요청함.
        
        """
     
                
        optresult, optresult2 = self.get_opt_chart(Option_expiration_mon)
 
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\OH0.res" # RES 파일 등록
        #self.SetFieldData("InBlock", "optcode", optcode)
        #self.AdviseRealData() # 실시간데이터 요청
 
        for i in optresult['optcode']:
            self.add_item(i)
        
        for i in optresult2['optcode']:
            self.add_item(i)
            
        self.OnReceiveVirtualData("DD")
        

    def add_item(self, optcode):
        # 실시간데이터 요청 종목 추가
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
    
    
    
 
try:
    from bestConnect import *
except:
    print("no window communication")    
#unit test code    
if __name__ == "__main__":
   
#    
    secinfo = secInfo()                        #계좌 정보 holder
    best = BestAccess()                        #Login class 생성
    accounts_list = best.comm_connect(secinfo) #Login 
#
    optdata = OptData() #ㅐ

    opt_mon_simul = PyOptHogaMonSimul()

    # 시뮬레이션 시작
    option_expiration_mon = "202310"  # 만기 월 정보는 예제로 설정, 필요에 따라 변경 가능
    opt_mon_simul.start(option_expiration_mon)

    # 시뮬레이션을 10초 동안 실행
    time.sleep(10)

    # 시뮬레이션 종료 (필요한 경우)
    opt_mon_simul.end()
    print("Simulation ended.")