# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 17:36:03 2021

@author: USER
"""
import numpy as np
import pandas as pd
import math
from datetime import datetime,timedelta

try:
    import win32com.client
    import pythoncom
except:
    print("no window communication")

class XAQueryEventHandlerT8419:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT8419.query_state = 1           
              
    
    
class HistoricalVolatilityCalc:
        
    def __init__(self):
        self.S = []
        
    def getKospi200History(self, startdate, enddate):
        instXAQueryT8419 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT8419)
        instXAQueryT8419.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t8419.res"
        instXAQueryT8419.SetFieldData("t8419InBlock","shcode",0,"101") #kospi200
        instXAQueryT8419.SetFieldData("t8419InBlock","gubun",0,"2")
        instXAQueryT8419.SetFieldData("t8419InBlock","qrycnt",0,30) 
        instXAQueryT8419.SetFieldData("t8419InBlock","sdate",0,startdate)
        instXAQueryT8419.SetFieldData("t8419InBlock","edate",0,enddate) 
        instXAQueryT8419.SetFieldData("t8419InBlock","cts_date",0,"")
        instXAQueryT8419.SetFieldData("t8419InBlock","comp_yn",0,"N") 
        instXAQueryT8419.Request(0)

       
        while XAQueryEventHandlerT8419.query_state == 0:
            pythoncom.PumpWaitingMessages()
        XAQueryEventHandlerT8419.query_state = 0
        
        
                
        shcode  = instXAQueryT8419.GetFieldData("t8419OutBlock", "shcode",0)
        jisiga  = instXAQueryT8419.GetFieldData("t8419OutBlock", "jisiga",0)        
        jihigh  = instXAQueryT8419.GetFieldData("t8419OutBlock", "jihigh",0)       
        jilow   = instXAQueryT8419.GetFieldData("t8419OutBlock", "jilow",0)        
        jiclose = instXAQueryT8419.GetFieldData("t8419OutBlock", "jiclose",0)   
        jivolume= instXAQueryT8419.GetFieldData("t8419OutBlock", "jivolume",0)      
        disiga  = instXAQueryT8419.GetFieldData("t8419OutBlock", "disiga",0)    
        dihigh  = instXAQueryT8419.GetFieldData("t8419OutBlock", "dihigh",0)       
        dilow   = instXAQueryT8419.GetFieldData("t8419OutBlock", "dilow",0)
        diclose = instXAQueryT8419.GetFieldData("t8419OutBlock", "diclose",0)
        disvalue= instXAQueryT8419.GetFieldData("t8419OutBlock", "disvalue",0)
        cts_date= instXAQueryT8419.GetFieldData("t8419OutBlock", "cts_date",0)
        s_time  = instXAQueryT8419.GetFieldData("t8419OutBlock", "s_time",0)
        e_time  = instXAQueryT8419.GetFieldData("t8419OutBlock", "e_time",0)
        dshmin  = instXAQueryT8419.GetFieldData("t8419OutBlock", "dshmin",0)
        rec_count= instXAQueryT8419.GetFieldData("t8419OutBlock", "rec_count",0)
        
        
        count = instXAQueryT8419.GetBlockCount("t8419OutBlock1")
        self.S = []


        for i in range(count):
            date  = instXAQueryT8419.GetFieldData("t8419OutBlock1", "date",i)
            open_ = instXAQueryT8419.GetFieldData("t8419OutBlock1", "open",i)
            high  = instXAQueryT8419.GetFieldData("t8419OutBlock1", "high",i)
            low   = instXAQueryT8419.GetFieldData("t8419OutBlock1", "low",i)
            close = instXAQueryT8419.GetFieldData("t8419OutBlock1", "close",i)
            jdiff_vol = instXAQueryT8419.GetFieldData("t8419OutBlock1", "jdiff_vol",i)
            value = instXAQueryT8419.GetFieldData("t8419OutBlock1", "value",i)
            
            #print(date, open_, high, low, close, jdiff_vol, value)

            self.S.append(pd.to_numeric(close))
            
        
        return self.S
         
    def getHV(self, data):
        self.S = data
        self.N = len(self.S)
        print("kospi 200 data size", self.N)
    
        R = []
        sum = 0
        for i in range(0,self.N-1):
            R.append(math.log(self.S[i+1]/self.S[i]))
            sum = sum + R[i]
            #print(i, self.S[i])
        
        #print('sum',sum, 'sumsum', math.log(self.S[10]/self.S[0]))
        R_mean = sum/(self.N-1)
       
        sum = 0
        Rt = []
        for i in range(0,self.N-1):
            Rt.append((R[i]-R_mean)**2)
            sum = sum + Rt[i]
            #print(i, Rt[i])
            
        #print(Rt)
        STD = math.sqrt(sum/(self.N-2))*100
        self.HV  = STD*math.sqrt(252)
        #self.HV  = STD*math.sqrt(365)
        print("STD",STD ,"HV", self.HV)
        
        return self.HV
    
    def get30dayHistorcalVol(self):
        raw_edate = datetime.now()
        edate = raw_edate.strftime("%Y%m%d")
        raw_sdate = raw_edate+timedelta(days=-40) #working day 기준 30일
        sdate = raw_sdate.strftime("%Y%m%d")
        print("Calculating Historical Volatility period ", sdate, edate)
        kospihistory =  self.getKospi200History(sdate, edate)
        return self.getHV(kospihistory)
        
    def get90dayHistorcalVol(self):
        raw_edate = datetime.now()
        edate = raw_edate.strftime("%Y%m%d")
        raw_sdate = raw_edate+timedelta(days=-90)
        sdate = raw_sdate.strftime("%Y%m%d")
        print(sdate, edate)
        kospihistory =  self.getKospi200History(sdate, edate)
        return self.getHV(kospihistory)
       

try:
    from bestConnect import *
except:
    print("no window communication")    
#unit test code    
if __name__ == "__main__":
   
    
    secinfo = secInfo()                        #계좌 정보 holder
    best = BestAccess()                        #Login class 생성
    accounts_list = best.comm_connect(secinfo) #Login 
 
    HVcalc = HistoricalVolatilityCalc()
    HV = HVcalc.get30dayHistorcalVol()
    print("HV", HV)
    
