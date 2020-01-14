# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 21:57:09 2019

@author: USER
"""
#from pandas import DataFrame
import pandas as pd
import sqlite3
from OptCodeTool import *
from subject import *
from observer import *
import time
from time import sleep
from timeManager import *
from kospi_history import *
from optPurse import *
from OptVisualizeTool import *

class PyOptHogaMonSimul:
    """
    this class generates the simulation data from Hoga Event
    Real Event cannot be used in off the market time.
    Using this class developper can develop the SW anytime 
    """

    
    def __init__(self,allowable_divide, bound):

        self.bound = bound    
        self.allowable_divide = allowable_divide
        
        print("optmon has created")
        self.count = 0
        self.con = sqlite3.connect("kospisample.db")
        self.sample = {}
        self.dataload()
        
        self.optcodetool = OptCodeTool()
        self.tmanager = timeManager()
        self.kospi_info = KOSPIHISTORYINFO()
         
        self.optpurse = optPurse()
        self.optvis = OptVisualizeTool()
        
                        
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
            
            if curr_year in ["2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018"]  :
            #if curr_year in ["2017","2018"]  :
            
            
                #self.optvis.showProfitDistribution( self.optpurse, cur_kospi_price, expire_month)
                ## 구입 strategy를 여기에서 부터 진행        
                
                #잔여일 계산
                remaining_days = self.kospi_info.get_remaining_days(currday_dash,expire_month)
                #HV 계산
                HV = self.kospi_info.get90dayHistorcalVol(currday_dash)
                #HV = self.kospi_info.get30dayHistorcalVol(currday_dash)


                upperTarget, lowerTarget = self.kospi_info.currentTargetOptBand(cur_kospi_price,HV,remaining_days)
    
                #해당 달의 최악의 경우 손실
                minvalue = self.optpurse.MinEstForCurrentPortfolio(cur_kospi_price,expire_month)
                #1달 허용투자
                #allowable_expense = self.optpurse.deposit/3.0*-1
                allowable_expense = self.optpurse.deposit/self.allowable_divide*-1
                
                unit  = int(self.optpurse.deposit/30000000)+1
                #if  minvalue > -10000000 :
                if minvalue > allowable_expense :
    
                    ##################################################################           
                    #             safety call put buy 
                    #safe_bound = 10.0  #maximum loss 250000*safe_bound
                    safe_bound = self.bound  #maximum loss 250000*safe_bound
                    safe_call_opt_code = self.optcodetool.optcode_gen(upperTarget+safe_bound,expire_month,'call')
                    safe_put_opt_code = self.optcodetool.optcode_gen(lowerTarget-safe_bound,expire_month,'put')
                    
                    safe_call_presence = False

                    try:
                        calloptdata = pd.read_csv("./data/K"+safe_call_opt_code+".csv",sep=",")
                        matchingdayindex = (calloptdata[calloptdata['일자'] == currday_dash])
                        print(matchingdayindex.iloc[0]['시가'])
                        
                        self.optpurse.BuyOption(safe_call_opt_code,matchingdayindex.iloc[0]['시가'],unit)#1)
                        #print('현재날짜',currday_dash)

                        safe_call_presence = True
        
                    except:
                        print("safe call option has not been solved" )

                    
                    safe_put_presence = False

                    try: 
                        putoptdata = pd.read_csv("./data/K"+safe_put_opt_code+".csv",sep=",")
                        matchingdayindex = (putoptdata[putoptdata['일자'] == currday_dash])
                        print(matchingdayindex.iloc[0]['시가'])
                        #print('현재날짜',currday_dash)
                        
                        self.optpurse.BuyOption(safe_put_opt_code,matchingdayindex.iloc[0]['시가'],unit)#1)

                        safe_put_presence = True
                    except:
                        print("safe put option has not been solved")
                
                    ####################################################   
        
        



                    target_call_opt_code = self.optcodetool.optcode_gen(upperTarget,expire_month,'call')
                    target_put_opt_code = self.optcodetool.optcode_gen(lowerTarget,expire_month,'put')
                    print(k, self.df["현재지수"][index],curr_year+curr_month, cur_kospi_price,expire_month,target_call_opt_code, target_put_opt_code )#,k[0:4])
                
                    if safe_call_presence == True:            

                        try:
                            calloptdata = pd.read_csv("./data/K"+target_call_opt_code+".csv",sep=",")
                            matchingdayindex = (calloptdata[calloptdata['일자'] == currday_dash])
                            print(matchingdayindex.iloc[0]['시가'])
                            
                            self.optpurse.SellOption(target_call_opt_code,matchingdayindex.iloc[0]['시가'],unit)#1)
                            #print('현재날짜',currday_dash)
            
                        except:
                            print("option has not been solved" )
                    
                    if  safe_put_presence == True:

                        try: 
                            putoptdata = pd.read_csv("./data/K"+target_put_opt_code+".csv",sep=",")
                            matchingdayindex = (putoptdata[putoptdata['일자'] == currday_dash])
                            print(matchingdayindex.iloc[0]['시가'])
                            #print('현재날짜',currday_dash)
                            
                            self.optpurse.SellOption(target_put_opt_code,matchingdayindex.iloc[0]['시가'],unit)#1)
                        except:
                            print("option has not been solved")
                    
                    

    
    
    
                #날짜 검색해서 만기일이면 가지고 있는 옵션 결산
                current_year_month = curr_year+curr_month
                
                if self.kospi_info.get_expiration_date(current_year_month) == currday_dash:
                      code = self.optpurse.ExpirationOptionScan(current_year_month)
                      print("코드:",code)
                      
                      for i in code:
                          self.optpurse.ClearingOption(pd.to_numeric(cur_kospi_price),i)
                      
                      
                      print("총액", self.optpurse.deposit)  
                      
                      
                      
                #option deposit history를 모두 도시
                self.optvis.stackDate(currday_dash)
                
                self.optvis.stackDeposit("111",self.optpurse.deposit)         
                self.optvis.stackKospi200("111",cur_kospi_price)             
                self.optvis.stackUpperBound("111",upperTarget)   
                self.optvis.stackLowerBound("111",lowerTarget)  
                print("index", index,"expirateion month", expire_month)
                expire_value = self.kospi_info.get_expiration_value(expire_month)
                self.optvis.stackExpirationValue(expire_value)
                self.optvis.stackMinValue(minvalue)
                #해당월 option을 모두 검색  
        
            
                        
          
            
          
            
            
        
    
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
#                #ATMS, deal_signal, sell_code, sell_price, buy_code, buy_price = optcodetool.extract_call_gap(df1, 12.8, ATMS) 
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

        #data = pd.read_csv("kospi200data_2012_.csv",sep=",")
        data = pd.read_csv("kospi200data.csv",sep=",")
        data.head()
        self.df = data[["일자","현재지수"]]




    def getSampleSize(self):
        return len(self.sample)
 

    
   #unit test code    
if __name__ == "__main__":
   # app = QApplication(sys.argv)
   
    optdata =  OptData() 
    for i in [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0]:
        for j in [5, 10, 15 ,20]:
            optmon = PyOptHogaMonSimul(i,j)
            print(optmon.getSampleSize())
                #opthogamon observer 등록
            optmon.register_subject(optdata)
            
            try:
                optmon.start("201810")
            except:
                optmon.optvis.showDepositHistory()
                optmon.optvis.showKospi200History()
                del optmon

