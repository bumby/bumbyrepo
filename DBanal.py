# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 21:23:04 2019

@author: USER
"""
import numpy as np
import pandas as pd
#import pandas_datareader.data as web
#from pandas import Series, DataFrame

import sqlite3
import math
from matplotlib import pyplot as plt

from observer import *
from opt_order_tr import *
from targetOptHistory import *
from datetime import datetime
from optPurse import *
from timeManager import *
from OptVisualizeTool import *
from kospi_history import *
from OptCodeTool import *



class DBalalysis(Observer):
    def __init__(self, expireMonth_,monitor_mode_):
        print("Option Analysis has been started")
        
        self.optcodetool = OptCodeTool()
        self.expiremonth = expireMonth_
        self.opthistory  = TargetOptHistory()
        
        
        if monitor_mode_ == "XingAPI":
            self.optpurse = optPurse()
            
        elif  monitor_mode_ == "simulation":
            self.optpurse = optPurseSimul()
            
        else:
            print("%s error no such mode in DBanal",monitor_mode_)
            
        self.tmanager = timeManager()    
        #parameter
        self.HV = 13.46
        self.threshold = 1.8
        self.remained_TO = 1
        
        
        self.strategylock = False # 현재 lock 중인가
        
        self.optvis = OptVisualizeTool()
        self.kospi_info = KOSPIHISTORYINFO()
        
      #------------------------------observer implementaion ---------------        
    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_, 이론가_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        if self.strategylock == False:
            self.strategylock = True
            
            self.호가시간=호가시간_
            self.단축코드=단축코드_
            self.매도호가1=매도호가1_
            self.매수호가1=매수호가1_
            self.이론가=이론가_
             
            self.scanStrategy_I()
            
            self.strategylock = False
            
        
        #self.extract_call_gap()
        

    def register_subject(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def display(self):
        #print ("호가시간",self.호가시간)
        pass
    
    def closeDBanal(self):
        now = datetime.now()
        datestr  = str(now.year)+str(now.month)+str(now.day)+".json"
        self.opthistory.saveTargetOptHistory(datestr)
#----------------------------------------------------------     
          
    def scanTargetOpt(self):
        kospi200price = pd.to_numeric(self.subject.envStatus['kospi200Index'])
        jandatecnt = pd.to_numeric(self.subject.envStatus['옵션잔존일'])
        self.HV =  pd.to_numeric(self.subject.envStatus['HV'])*1.2 
        #self.HV = 13.46 #전광판엑서 제공한함 다른 방법 필요

        
      ##  kospi200price=238
      #  jandatecnt = 35
      #  HV = 13.53
        if kospi200price != 0:  #초기화가 되면 초기화가 제대로 안된 점이 있음 
            
            #print("kospi", kospi200price, " jandatecnt", jandatecnt, " HV ", HV)
            sigma = self.HV/100.0*math.sqrt(jandatecnt/365.0)
            self.upperTarget = math.exp(math.log(kospi200price)+sigma*0.8) #1.3은 normal distribution 90% 범위 #0.8은 78% 범위
            self.lowerTarget = math.exp(math.log(kospi200price)-sigma*0.8) #1.3은 normal distribution 90% 범위
            self.upperTargetOpt = self.optcodetool.optcode_gen(self.upperTarget, self.expiremonth , "call")
            self.lowerTargetOpt = self.optcodetool.optcode_gen(self.lowerTarget, self.expiremonth , "put")
            
            #new safe target
            self.safeupperTargetOpt = self.optcodetool.optcode_gen(self.upperTarget+10.0, self.expiremonth , "call")
            self.safelowerTargetOpt = self.optcodetool.optcode_gen(self.lowerTarget-10.0, self.expiremonth , "put")
             
        
            if self.단축코드 == self.upperTargetOpt:
                #print("correct target upper", self.upperTargetOpt, "lower ", self.lowerTargetOpt )
                
                self.threshold = 1.8
                bid_theory_ratio = pd.to_numeric(self.매수호가1)/pd.to_numeric(self.이론가)
                print("target", self.단축코드, " 매수호가", pd.to_numeric(self.매수호가1), "이론가", pd.to_numeric(self.이론가))
                print("ratio", bid_theory_ratio)
                self.opthistory.setOptData(self.호가시간, self.단축코드, self.매도호가1, self.매수호가1, self.이론가) #저장 툴
                if bid_theory_ratio > 1.1 and  bid_theory_ratio > self.threshold  :
                    print("!!!! sell sell sell !!!")
                    print("!!!! sell sell sell !!!")
                    print("!!!! sell sell sell !!!")
                    if  self.remained_TO == 1:
                        self.optpurse.SellOption(self.단축코드, "00",pd.to_numeric(self.매수호가1),1)
                        
                        #safe option 도 현재 매도 가격                         
                        self.optpurse.BuyOption(self.safeupperTargetOpt,"03", 0.00, 1)
                        self.remained_TO = 0
                    
            if self.단축코드 == self.lowerTargetOpt:
                #print("correct target upper", self.upperTargetOpt, "lower ", self.lowerTargetOpt )
                
                self.threshold = 1.8
                bid_theory_ratio = pd.to_numeric(self.매수호가1)/pd.to_numeric(self.이론가)
                print("target", self.단축코드, " 매수호가", pd.to_numeric(self.매수호가1), "이론가", pd.to_numeric(self.이론가))
                print("ratio", bid_theory_ratio)
                self.opthistory.setOptData(self.호가시간, self.단축코드, self.매도호가1, self.매수호가1, self.이론가) #저장 툴 
                
                if bid_theory_ratio > 1.1 and  bid_theory_ratio > self.threshold  :
                    print("!!!! sell sell sell !!!")
                    print("!!!! sell sell sell !!!")
                    print("!!!! sell sell sell !!!")
                    if self.remained_TO == 1:
                        
                        self.optpurse.SellOption(self.단축코드,"00", pd.to_numeric(self.매수호가1),1)
                    
                        #safe option 도 현재 매도 가격                         
                        self.optpurse.BuyOption(self.safelowerTargetOpt,"03", 0.00, 1)
                        self.remained_TO = 0
     
                   
    def scanStrategy_I(self):
        kospi200price = pd.to_numeric(self.subject.envStatus['kospi200Index'])
        jandatecnt = pd.to_numeric(self.subject.envStatus['옵션잔존일'])
        self.HV =  pd.to_numeric(self.subject.envStatus['HV']) 
        #self.HV = 13.46 #전광판엑서 제공한함 다른 방법 필요
       
        if kospi200price != 0:
            k = self.호가시간 #업데이트에서 호가시간이 기재되지 않거나 잘못기재되는 경우가 많다. 
            curr_year = k[0:4]
            curr_month = k[5:7]
            curr_day = k[8:10]
            currday_dash = curr_year+'/'+curr_month+'/'+curr_day
            expire_month = self.tmanager.getNextYearMonth(pd.to_numeric(curr_year),pd.to_numeric(curr_month))
          
            #print("k",k)
            #print("kospi200price",kospi200price,"jandatecnt",jandatecnt,"HV", self.HV)
           # print("curr_day",currday_dash,"expire_month",expire_month)
            sigma = self.HV/100.0*math.sqrt(jandatecnt/365.0)
            self.upperTarget = math.exp(math.log(kospi200price)+sigma*0.8) #1.3은 normal distribution 90% 범위 #0.8은 78% 범위
            self.lowerTarget = math.exp(math.log(kospi200price)-sigma*0.8) #1.3은 normal distribution 90% 범위
            
            #print("uppertarget",self.upperTarget)
            self.upperTargetOpt = self.optcodetool.optcode_gen(self.upperTarget, expire_month , "call")
            self.lowerTargetOpt = self.optcodetool.optcode_gen(self.lowerTarget, expire_month , "put")
                
            #new safe target
            safe_bound = 10.0
            self.safeupperTargetOpt = self.optcodetool.optcode_gen(self.upperTarget+safe_bound, expire_month , "call")
            self.safelowerTargetOpt = self.optcodetool.optcode_gen(self.lowerTarget-safe_bound, expire_month , "put")
                 
              
     
            
            minvalue = self.optpurse.MinEstForCurrentPortfolio(kospi200price,expire_month)
            
            #1달 허용투자
        
            self.allowable_divide = 2.5
            allowable_expense = self.optpurse.GetDepositInfo()/self.allowable_divide*-1
            unit  = int(self.optpurse.GetDepositInfo()/100000000)+1
           # print("allowable min value",minvalue ,"allowable expense", allowable_expense)
            if minvalue > allowable_expense :
                
                
                
                if self.단축코드 == self.upperTargetOpt  and (self.safeupperTargetOpt in self.subject.optChart.keys()):  #이미 한 번 읽혀진 옵션에 대해서만 조사 
                    success = self.optpurse.SellOption(self.upperTargetOpt,"00",pd.to_numeric(self.매수호가1),unit)
                    if success == True: #지정가로 매도 성공하면 시장가로 
                    # safe option 도 현재 매도 가격                         
                        #self.optpurse.BuyOption(self.safeupperTargetOpt,"03",pd.to_numeric(self.subject.optChart[self.safeupperTargetOpt]["offerho1"]),unit)
                        while self.optpurse.BuyOption(self.safeupperTargetOpt,"03",0.0,unit) == False:
                            print("upper safe guard call option 매입 중")
                        print("upper 구입완료",self.optpurse.GetDepositInfo())
                    
                if self.단축코드 == self.lowerTargetOpt and (self.safelowerTargetOpt in self.subject.optChart.keys()):
                         
                    success = self.optpurse.SellOption(self.lowerTargetOpt,"00",pd.to_numeric(self.매수호가1),unit)
                    if success ==  True:
                    # safe option 도 현재 매도 가격                         
                        #self.optpurse.BuyOption(self.safelowerTargetOpt,"03",pd.to_numeric(self.subject.optChart[self.safelowerTargetOpt]["offerho1"]),unit)                                     
                        while self.optpurse.BuyOption(self.safelowerTargetOpt,"03",0.0,unit) == False:
                            print("lower safe guard put option 매입 중" )
                        print("lower 구입완료",self.optpurse.GetDepositInfo())
           
                    
            
            """
            #시뮬레이션의 경우 만기일 청산 작업 진행
            current_year_month = curr_year+curr_month
            if self.kospi_info.get_expiration_date(current_year_month) == currday_dash:
               #code = self.optpurse.ExpirationOptionScan(current_year_month)
                                     
               #for i in code:
               #    self.optpurse.ClearingOption(kospi200price,i)
               self.optpurse.ExpirationProcess()
                
             #option deposit history를 모두 도시
            self.optvis.stackDate(currday_dash)
            
            self.optvis.stackDeposit("111",self.optpurse.GetDepositInfo())         
            self.optvis.stackKospi200("111",kospi200price)             
            self.optvis.stackUpperBound("111",self.upperTarget)   
            self.optvis.stackLowerBound("111",self.lowerTarget)  
            #print("index", index,"expirateion month", expire_month)
            expire_value = self.kospi_info.get_expiration_value(expire_month)
            self.optvis.stackExpirationValue(expire_value)
            self.optvis.stackMinValue(minvalue)
            """  
        #해당월 option을 모두 검색      
   
 
    
    def extract_call_gap(self, df, trigger_price, atms_storage):
    
        offerho1 = df['offerho1']
        bidho1 =  df['bidho1']
        gmprice = df['gmprice']
        optcode = df['optcode']
        
        offerho1_num = pd.to_numeric(offerho1[::-1])  #순서를 뒤집기 높은 strike price 부터 출력되어 오름차순으로 재정렬
        bidho1_num = pd.to_numeric(bidho1[::-1])
        gmprice_num = pd.to_numeric(gmprice[::-1])
        optcode_sel = optcode[::-1]
        
        #print(hh,mm,ss)
        
        deal_signal = "no"
        sell_code = "no"
        sell_price = 0
        buy_code = "no"
        buy_price = 0
        
        gaptot = []
        gappre = 0.0
        for i in range(0,offerho1.size-1):
            gap = bidho1_num[i]-offerho1_num[i+1]
            gaptot.append(gap)
            
            if gappre>0.25 and gap<=0.25 and bidho1_num[i]>0.005 and offerho1_num[i+1]>0.005:
               print(bidho1_num.index[i], gmprice_num[i], gappre, gap )  
               print(pd.to_numeric(bidho1_num.index[i])-gmprice_num[i])
               atms_storage.append(pd.to_numeric(bidho1_num.index[i])-gmprice_num[i]) 
               if pd.to_numeric(bidho1_num.index[i])-gmprice_num[i]>trigger_price and bidho1_num[i]>0.005 and offerho1_num[i+1]>0.005:
                  #maximum.append(store)
                  sell_code = optcode_sel[i]
                  sell_price = bidho1_num[i]
                  buy_code = optcode_sel[i+1]
                  buy_price = offerho1_num[i+1]
                  deal_signal = "yes"
        
            #print(gaptot)
            gappre = gap
            #plt.plot(gaptot[25:60])
            #plt.show()   
        
        return atms_storage, deal_signal, sell_code, sell_price, buy_code, buy_price

if __name__ == "__main__":

    dbanal = DBalalysis("202002","XingAPI")      
    con = sqlite3.connect("D:\work\Y2018\option\kospi.db")
    
    hhtot = ["09","10","11","12","13","14"]
    mmtot = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19", "20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39", "40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59"];
    sstot = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19", "20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39", "40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59"];
    

    
    ATMS = []
    maximum = []; 
    
    for hh in hhtot:
        for mm in mmtot:
            for ss in sstot:
                store = "call190712"+hh+mm+ss
                #print(store)
                #df1 = pd.read_sql("SELECT * from "+store, con, index_col = "index")
                #print(df1)
                #df1 = pd.read_sql("SELECT * from call190624090001", con, index_col = "index")
               
                try:
                    df1 = pd.read_sql("SELECT * from "+store, con, index_col = "index")
                    ATMS, deal_signal, sell_code, sell_price, buy_code, buy_price = dbanal.extract_call_gap(df1, 12.8, ATMS) 
                   # maximum.append(sell_code)
    #                offerho1 = df1['offerho1']
    #                bidho1 = df1['bidho1']
    #                gmprice = df1['gmprice']
    #                offerho1_num = pd.to_numeric(offerho1[::-1])
    #                bidho1_num = pd.to_numeric(bidho1[::-1])
    #                gmprice_num = pd.to_numeric(gmprice[::-1])
    #                # gap = offerho1_num[0:offerho1.size-1]-bidho1_num[1:offerho1.size]
    #                print(hh,mm,ss)
    #                # plt.plot(offerho1_num)
    #                # plt.plot(bidho1_num)
    #                # plt.show()
    #                
    #                
    #                
    #                gaptot = []
    #                gappre = 0.0
    #                for i in range(0,offerho1.size-1):
    #                    gap = bidho1_num[i]-offerho1_num[i+1]
    #                    #print(offerho1[index])
    #                    #-bidho1[int(index)+1] 
    #                    gaptot.append(gap)
    #                    
    #                    if gap>2.0 and bidho1_num[i]>0.005 and offerho1_num[i+1]>0.005:
    #                       overgap.append(store)
    #                        
    #                    if gappre>0.25 and gap<=0.25 and bidho1_num[i]>0.005 and offerho1_num[i+1]>0.005:
    #                       print(bidho1_num.index[i], gmprice_num[i], gappre, gap )  
    #                       print(pd.to_numeric(bidho1_num.index[i])-gmprice_num[i])
    #                       ATMS.append(pd.to_numeric(bidho1_num.index[i])-gmprice_num[i]) 
    #                       if pd.to_numeric(bidho1_num.index[i])-gmprice_num[i]>16 and bidho1_num[i]>0.005 and offerho1_num[i+1]>0.005:
    #                          maximum.append(store)
    #                
    #                        #print(gaptot)
    #                    gappre = gap
    #                plt.plot(gaptot[25:60])
    #                plt.show()
               
    
    
                except Exception:
                        # Catching this exception works fine if, for example,
                        # I enter the wrong username and password
                    print("\nNo such table")
    
    
                
    bins = np.arange(0,30,0.2)          
    plt.hist(ATMS,bins)           
    hist, bins = np.histogram(ATMS, bins)   
    
    
