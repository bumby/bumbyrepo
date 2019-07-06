# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 21:23:04 2019

@author: USER
"""
import numpy as np

import pandas as pd
#import pandas_datareader.data as web
#from pandas import Series, DataFrame

import datetime
import sqlite3
from matplotlib import pyplot as plt
#start = datetime.datetime(2010,1 ,1)
#end = datetime.datetime(2016,6, 12)
#df = web.DataReader("078930.KS", "yahoo", start, end)

class DBalalysis:
    def __init__(self):
        timer = 0;
        
    def extract_call_gap(self, df, trigger_price, atms_storage):
    
        offerho1 = df['offerho1']
        bidho1 = df['bidho1']
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
                store = "call190705"+hh+mm+ss
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
    
    
                
    bins = np.arange(0,30,1)          
    plt.hist(ATMS,bins)           
    hist, bins = np.histogram(ATMS, bins)   
    
    
