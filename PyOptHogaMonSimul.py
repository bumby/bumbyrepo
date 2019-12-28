# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 21:57:09 2019

@author: USER
"""
#from pandas import DataFrame
import pandas as pd
import sqlite3
from DBanal import *
from subject import *
from observer import *
import time
from time import sleep
from timeManager import *
from kospi_history import *


class PyOptHogaMonSimul(Observer):
    """
    this class generates the simulation data from Hoga Event
    Real Event cannot be used in off the market time.
    Using this class developper can develop the SW anytime 
    """
    _instance = None
    
    def __init__(self):
        if self._instance is not None:
            raise ValueError("An instance already exists")
        print("optmon has created")
        self.count = 0
        self.con = sqlite3.connect("kospisample.db")
        self.sample = {}
        self.dataload()
        self.dbanal = DBalalysis('2')
        self.tmanager = timeManager()
        self.kospi_info = KOSPIHISTORYINFO()
        
                        
    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_, 이론가_): 
        #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        """
        observer implementaion
        """
        print(호가시간_, 단축코드_, 매도호가1_, 매수호가1_, 이론가_)
   
   
    def register_subject(self, subject):
        """
        observer implementaion
        """
        self.subject = subject
        self.subject.register_observer(self)


    def start(self,  Option_expiration_mon):
        """
        db에서 data  load
        """
                
        kospi_at_target = 0  #target kospi 에 대하여 
        index = 0
        for k in self.df["일자"]:
            
            
            index = index + 1
            cur_kospi_price = pd.to_numeric(self.df["현재지수"][index])
            curr_year = k[0:4]
            curr_month = k[5:7]
            curr_day = k[8:10]
            currday_dash = curr_year+'/'+curr_month+'/'+curr_day
            expire_month = self.tmanager.getNextYearMonth(pd.to_numeric(curr_year),pd.to_numeric(curr_month))
            
            if curr_year in ["2013","2014","2015","2016","2017"]:
                
                
                
                #잔여일 계산
                remaining_days = self.kospi_info.get_remaining_days(currday_dash,expire_month)
                #HV 계산
                HV = self.kospi_info.get90dayHistorcalVol(currday_dash)
                upperTarget, lowerTarget = self.kospi_info.currentTargetOptBand(cur_kospi_price,HV,remaining_days)
    
                   
                #target_call_opt_code = self.dbanal.optcode_gen(cur_kospi_price+10.0,expire_month,'call')
                #target_put_opt_code = self.dbanal.optcode_gen(cur_kospi_price-10.0,expire_month,'put')
                target_call_opt_code = self.dbanal.optcode_gen(upperTarget,expire_month,'call')
                target_put_opt_code = self.dbanal.optcode_gen(lowerTarget,expire_month,'put')
                print(k, self.df["현재지수"][index],curr_year+curr_month, cur_kospi_price,expire_month,target_call_opt_code, target_put_opt_code )#,k[0:4])
               
                
                try:
                    calloptdata = pd.read_csv("./data/K"+target_call_opt_code+".csv",sep=",")
                    matchingdayindex = (calloptdata[calloptdata['일자'] == currday_dash])
                    print(matchingdayindex.iloc[0]['시가'])
                    #print('현재날짜',currday_dash)
    
                except:
                    print("option has not been solved" )
                
                
                try: 
                    putoptdata = pd.read_csv("./data/K"+target_put_opt_code+".csv",sep=",")
                    matchingdayindex = (putoptdata[putoptdata['일자'] == currday_dash])
                    print(matchingdayindex.iloc[0]['시가'])
                    #print('현재날짜',currday_dash)
                except:
                    print("option has not been solved")
    #           
                
                            
              
            

            
            
            
        
    
#kospi date load 초기화     
    def dataload(self):
        
    #    hhtot = ["09","10","11","12","13","14"]
    #    mmtot = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19", "20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39", "40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59"];
          
    #    hhtot = ["09"]    
    #    mmtot = ["24","25"]
    #    sstot = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19", "20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39", "40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59"];
    
#        store_index = ["option190910224214",
#                       "option190910224455",
#                       "option190910225052",
#                       "option190910230617"]    
#        
#      
#        for store in store_index:
#          
#                   
#            self.sample[store]={}
#            try:
#                df = pd.read_sql("SELECT * from "+store, self.con, index_col = "index")
#                #ATMS, deal_signal, sell_code, sell_price, buy_code, buy_price = dbanal.extract_call_gap(df1, 12.8, ATMS) 
#                self.sample[store]["time"]     = store
#                self.sample[store]["offerho1"] = df['offerho1']
#                self.sample[store]["bidho1"]   = df['bidho1']
#                self.sample[store]["optcode"]  = df['optcode']
#                
#            except Exception:
#                    # Catching this exception works fine if, for example,
#                    # I enter the wrong username and password
#                pass
#                #print("\nNo such table")

        data = pd.read_csv("kospi200data_2012_.csv",sep=",")
        data.head()
        self.df = data[["일자","현재지수"]]




    def getSampleSize(self):
        return len(self.sample)
 
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PyOptHogaMonSimul()
        return cls._instance

  
    
   #unit test code    
if __name__ == "__main__":
   # app = QApplication(sys.argv)
   
    optdata =  OptData() 
    optmon = PyOptHogaMonSimul().get_instance()
    print(optmon.getSampleSize())
        #opthogamon observer 등록
    optmon.register_subject(optdata)
    optmon.start("201810")

