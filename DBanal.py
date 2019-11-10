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


class DBalalysis(Observer):
    def __init__(self):
        print("Option Analysis has been started")
        
      #------------------------------observer implementaion ---------------        
    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        self.호가시간=호가시간_
        self.단축코드=단축코드_
        self.매도호가1=매도호가1_
        self.매수호가1=매수호가1_
         
        self.scanTargeOpt()
        self.extract_call_gap()
        self.display()

    def register_subject(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def display(self):
        print ("")
#----------------------------------------------------------     
          
    def scanTargetOpt(self):
        kospi200price = pd.to_numeric(self.subject.envStatus['kospi200Index'])
        jandatecnt = pd.to_numeric(self.subject.envStatus['옵션잔존일'])
        HV =  pd.to_numeric(self.subject.envStatus['HV'])
        sigma = HV/100.0*math.sqrt(jandatecnt/365.0)
        self.upperTarget = math.exp(math.log(kospi200price)+sigma*1.3) #1.3은 normal distribution 90% 범위
        self.lowerTarget = math.exp(math.log(kospi200price)-sigma*1.3) #1.3은 normal distribution 90% 범위

    def optcode_gen(self, optstrike, expirationdate, putncall):

        # target price  



        #put and sell code and kospi200
        if putncall == "call" :
            opt_putncall_code = "201"
            price_divide = int(math.floor(optstrike/2.5))
            opt_index = int((price_divide+1)*2.5)
            opt_index_str = str(opt_index)
            print(opt_index_str)
        elif putncall == "put" :
            opt_putncall_code = "301"
            price_divide = int(math.floor(optstrike/2.5))
            opt_index = int((price_divide)*2.5)
            opt_index_str = str(opt_index)
            print(opt_index_str)
        else :
            print("no such code")
            raise Exception('no such code')  


        #target expiration year
        expiration_year = expirationdate[0:4]
        if  expiration_year=="2019" :
            expiration_year_code = "P"
        elif expiration_year=="2020" :
            expiration_year_code = "Q"
        elif expiration_year=="2021" :
            expiration_year_code = "R"
        elif expiration_year=="2022" :
            expiration_year_code = "S"
        elif expiration_year=="2023" :
            expiration_year_code = "T"
        elif expiration_year=="2024" :
            expiration_year_code = "V"
        elif expiration_year=="2025" :
            expiration_year_code = "W"    
        else :
            print("option code is available only for 2025")
            raise Exception("option code is available only for 2025")

        #target expiration month
        expiration_month  = expirationdate[4:6]
        if  expiration_month=="01" :
            expiration_month_code = "1"
        elif expiration_month=="02" :
            expiration_month_code = "2"
        elif expiration_month=="03" :
            expiration_month_code = "3"
        elif expiration_month=="04" :
            expiration_month_code = "4"
        elif expiration_month=="05" :
            expiration_month_code = "5"
        elif expiration_month=="06" :
            expiration_month_code = "6"
        elif expiration_month=="07" :
            expiration_month_code = "7"    
        elif expiration_month=="08" :
            expiration_month_code = "8"
        elif expiration_month=="09" :
            expiration_month_code = "9"
        elif expiration_month=="10" :
            expiration_month_code = "A"
        elif expiration_month=="11" :
            expiration_month_code = "B" 
        elif expiration_month=="12" :
            expiration_month_code = "C"
        else :
            print("choose only for 1~12")
            raise Exception("choose only for 1~12")

        optcode = opt_putncall_code + expiration_year_code+ expiration_month_code + opt_index_str
        print(optcode)
        return optcode
        
   
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

    dbanal = DBalalysis();       
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
    
    
