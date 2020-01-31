# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 14:42:48 2019

@author: USER
"""

import sys
from PyQt5.QtWidgets import *

try:
    import win32com.client
    import pythoncom
except:
    print("no window communication")

from pandas import DataFrame
#from threading import Timer,Thread,Event
import time

from subject import *

class XAQueryEventHandlerT2301:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT2301.query_state = 1           
              

       
            
class PyOptChegyolMon:
    def __init__(self):
        print("optmon has created")
        self.count = 0


#temporary
    def register_subject(self, subject):
        self.subject = subject
        #self.subject.register_observer(self)

    
        
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
        
        print(histimpv, jandatecnt,cimpv,  pimpv )
        
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
            
            print(actprice, optcode, price, sign,  diff, volume, iv, mgjv, mgjvupdn, offerho1, bidho1, cvolume, delt, gama, vega, ceta, rhox, theoryprice)
        
        
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
                 
            print(actprice2,optcode2, price2, sign2,  diff2, volume2, iv2, mgjv2, mgjvupdn2, offerho12, bidho12, cvolume2, delt2, gama2, vega2, ceta2, rhox2, theoryprice2)
        
        #옵션 잔존일 측정
        self.subject.change_envStatus("HV",histimpv)
        self.subject.change_envStatus("kospi200Index",gmprice)
        self.subject.change_envStatus("옵션잔존일",jandatecnt)
        return ohlcv, ohlcv2    
    
#--------------------------
# XReal_OC0_  Real data Acquisition
#--------------------------  

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
        매수호가1 = self.GetFieldData("OutBlock", "bidho1")
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
        
        self.subject.change_envStatus("kospi200Index",KOSPI200지수)
        self.subject.change_optprice(체결시간,단축코드,매도호가1,매수호가1, 이론가)
        #print("체결발생", self.count, tr_code, 체결시간, 현재가, 시가, 매도호가1, 매수호가1, 단축코드, 장운영정보, KOSPI200지수)
        

    def start(self,  Option_expiration_mon):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        optresult, optresult2 = self.get_opt_chart(Option_expiration_mon)
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\OC0.res" # RES 파일 등록
        #self.SetFieldData("InBlock", "optcode", optcode)
        #self.AdviseRealData() # 실시간데이터 요청
 
        for i in optresult['optcode']:
            print(i)
            self.add_item(i)
        
        for i in optresult2['optcode']:
            self.add_item(i)
            
       

    def add_item(self, optcode):
        # 실시간데이터 요청 종목 추가
        #self.SetFieldData("InBlock", "shcode", stockcode)
        print("flag",optcode)
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
 


import threading
import time

class PyOptChegyolMonSimul:
    _instance = None
        
    def __init__(self):
        if self._instance is not None:
            raise ValueError("An instantiation already exist")
        print("optmon has created")
        self.count = 0

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PyOptChegyolMonSimul()
        return cls._instance
    

#temporary
    def register_subject(self, subject):
        self.subject = subject
        #self.subject.register_observer(self)

    
        
#--------------------------
# t2301  차트
#--------------------------  
    def get_opt_chart(self, Option_expiration_mon):
    
        pass   
    
#--------------------------
# XReal_OC0_  Real data Acquisition
#--------------------------  

    def OnReceiveRealData(self, tr_code): # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """
        self.count += 1
        KOSPI200지수 = "234"
        체결시간 =  "123"
        매도호가1 = "11.0" 
        매수호가1 = "10.0"
        단축코드 = "201CA230"
        이론가 = "11.0"
        
        self.subject.change_envStatus("kospi200Index",KOSPI200지수)
        self.subject.change_optprice(체결시간,단축코드,매도호가1,매수호가1, 이론가)
        print("체결발생", self.count, tr_code, 체결시간, KOSPI200지수, 매도호가1, 매수호가1, 단축코드)
        threading.Timer(1.0,self.OnReceiveRealData, args = ("dd",)).start()
        

    def start(self,  Option_expiration_mon):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        #while(1):
        self.OnReceiveRealData("")
        
       

    def add_item(self, optcode):
        # 실시간데이터 요청 종목 추가
        #self.SetFieldData("InBlock", "shcode", stockcode)
        print("flag",optcode)
        self.SetFieldData("InBlock", "optcode", optcode)
        self.AdviseRealData()

    def remove_item(self, optcode):
        # stockcode 종목만 실시간데이터 요청 취소
        self.UnadviseRealDataWithKey(optcode)

    def end(self):
        self.UnadviseRealData() # 실시간데이터 요청 모두 취소

try:
    from bestConnect import *
except:
    print("no window communication")

#unit test code    
if __name__ == "__main__":
   # app = QApplication(sys.argv)
    
    secinfo = secInfo()                        #계좌 정보 holder
    best = BestAccess()                        #Login class 생성
    accounts_list = best.comm_connect(secinfo) #Login 

    optdata =  OptData() #ㅐ
    pyoptchegyolmon = PyOptChegyolMon.get_instance()
    pyoptchegyolmon.register_subject(optdata)
    pyoptchegyolmon.start("202002")
    #pyoptmon.get_list_code()
    #pyoptmon.get_opt_chart()
    #pyoptmon.run()

    while pyoptchegyolmon.count < 500:
        pythoncom.PumpWaitingMessages()
