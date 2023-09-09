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
from timeManager import *
from kospi_history import *
from optPurse import *
from OptVisualizeTool import *
from OptStrategy import *
from blacksholes_calc import *
from collections import deque

import numpy as np

from subject import *




class PreprocessingUtility:

    def __init__(self, df, tmanager, optcodetool):
        self.df = df
        self.tmanager = tmanager
        self.optcodetool = optcodetool

    def extract_date_parts(self, date_str):
        curr_year = date_str[0:4]
        curr_month = date_str[5:7]
        curr_day = date_str[8:10]
        return curr_year, curr_month, curr_day

    def calculate_HV(self, currday_dash):
        return self.kospi_info.get30dayHistorcalVol(currday_dash)

    def generate_option_code(self, target, month, type):
        return self.optcodetool.optcode_gen(target, month, type)

    def get_next_expiration_month(self, curr_year, curr_month):
        return self.tmanager.getNextYearMonth(pd.to_numeric(curr_year), pd.to_numeric(curr_month))


class Strategy:

    def __init__(self, optpurse, bound, optcodetool, bscalc, profit_ratio_thres):
        self.optpurse = optpurse
        self.bound = bound
        self.optcodetool = optcodetool
        self.bscalc = bscalc
        self.profit_ratio_thres = profit_ratio_thres


    #option code 와 현재 날짜 가 있을때 현재 가격 출력 
    def loadOptPriceFromCSV(self, code, currday_dash):
        try:
            optdata = pd.read_csv("./data/K"+code+".csv",sep=",")
            matchingdayindex = (optdata[optdata['일자'] == currday_dash])
            opt_price = matchingdayindex.iloc[0]['종가']
            return opt_price
           
        except:
            print(code, "option can't open" )


    def execute_strategy(self, expire_month, upperTarget, lowerTarget, cur_kospi_price, remaining_days, currday_dash, unit):
        call_profit_ratio = 0
        put_profit_ratio = 0

        safe_bound = self.bound
        safe_call_opt_code = self.optcodetool.optcode_gen(upperTarget+safe_bound,expire_month,'call')
        safe_put_opt_code = self.optcodetool.optcode_gen(lowerTarget-safe_bound,expire_month,'put')

        safe_call_presence = False
        try:
            safe_call_opt_price = self.loadOptPriceFromCSV(safe_call_opt_code, currday_dash)
            safe_call_Target_IV = self.bscalc.getCallIV(upperTarget+safe_bound, pd.to_numeric(cur_kospi_price), 0.03, pd.to_numeric(remaining_days)/365, safe_call_opt_price)
            safe_call_presence = True
        except:
            print("safe call option has not been solved")
                    
        safe_put_presence = False
        try:
            safe_put_opt_price = self.loadOptPriceFromCSV(safe_put_opt_code, currday_dash)
            safe_put_Target_IV = self.bscalc.getPutIV(lowerTarget-safe_bound, pd.to_numeric(cur_kospi_price), 0.03, pd.to_numeric(remaining_days)/365, safe_put_opt_price)
            safe_put_presence = True
        except:
            print("safe put option has not been solved")
            
        target_call_opt_code = self.optcodetool.optcode_gen(upperTarget,expire_month,'call')
        target_put_opt_code = self.optcodetool.optcode_gen(lowerTarget,expire_month,'put')

        if safe_call_presence == True: 
            try:
                target_call_opt_price = self.loadOptPriceFromCSV(target_call_opt_code, currday_dash)
            except:
                print("option has not been solved" )

        if  safe_put_presence == True:
            try:
                target_put_opt_price = self.loadOptPriceFromCSV(target_put_opt_code, currday_dash)
            except:
                print("option has not been solved")

        try:
            call_profit_ratio = (target_call_opt_price - safe_call_opt_price) / self.bound    
            put_profit_ratio = (target_put_opt_price - safe_put_opt_price) / self.bound

            if call_profit_ratio > self.profit_ratio_thres:
                self.optpurse.BuyOption(safe_call_opt_code, safe_call_opt_code, safe_call_opt_price, unit)
                self.optpurse.SellOption(target_call_opt_code, target_call_opt_code, target_call_opt_price, unit)

            if put_profit_ratio > self.profit_ratio_thres:
                self.optpurse.BuyOption(safe_put_opt_code, safe_put_opt_code, safe_put_opt_price, unit)
                self.optpurse.SellOption(target_put_opt_code, target_put_opt_code, target_put_opt_price, unit)

        except:
            call_profit_ratio = 0
            put_profit_ratio = 0

        return call_profit_ratio, put_profit_ratio


class VisualizationReporting:

    def __init__(self, optvis):
        self.optvis = optvis

    def visualize_data(self, currday_dash, deposit, cur_kospi_price, upperTarget, lowerTarget, upperTarget_IV, lowerTarget_IV, expire_value, minvalue, HV, call_profit_ratio, put_profit_ratio):
        self.optvis.stackDate(currday_dash)
        self.optvis.stackDeposit("111", deposit)
        self.optvis.stackKospi200("111", cur_kospi_price)
        self.optvis.stackUpperBound("111", upperTarget)
        self.optvis.stackLowerBound("111", lowerTarget)
        self.optvis.stackUpperIVBound("111", upperTarget_IV)
        self.optvis.stackLowerIVBound("111", lowerTarget_IV)
        self.optvis.stackExpirationValue(expire_value)
        self.optvis.stackMinValue(minvalue)
        
        try:
            self.optvis.stackHVValue(pd.to_numeric(HV))
            self.optvis.stackIVValue(pd.to_numeric(upperTarget_IV))
        except:
            self.optvis.stackHVValue(0)
            self.optvis.stackIVValue(0)
            
        self.optvis.stackCallProfitRatio("111", call_profit_ratio * 100)
        self.optvis.stackPutProfitRatio("111", put_profit_ratio * 100)

    def report_probability(self, SuccessNo_inBand, Total_GambleNo, NoinBandQueue):
        print("Gamble Probability ", SuccessNo_inBand / Total_GambleNo)
        self.optvis.stackinsideBand("111", sum(NoinBandQueue) / NoinBandQueue.maxlen * 100)


class Kospi200Simul:
    """
    this class generates the simulation data from Hoga Event
    Real Event cannot be used in off the market time.
    Using this class developper can develop the SW anytime 
    """

    
    def __init__(self,allowable_divide, bound, coverage_sigma, profit_ratio_thres): #allowable_divide : 전체 자산 분할 3이면 자산/3 만큼 한달에 투자  bound :   coverage sigma : 승률 (80%는 이기는 승률)  

        

        
        self.allowable_divide = allowable_divide
        self.bound = bound    
        self.coverage_sigma = coverage_sigma  #0.84 80% 1.03 85%  1.29 90%
        self.profit_ratio_thres = profit_ratio_thres      # 0.2      0.15      0.1
        
        print("optmon has created")
        self.count = 0
        self.con = sqlite3.connect("kospisample.db")
        self.sample = {}
        #self.dataload()
        
        self.optcodetool = OptCodeTool()
        self.tmanager = timeManager()
        self.kospi_info = KOSPIHISTORYINFO()
        self.df = self.kospi_info.df
         
        #self.optpurse = optPurse("simulation")
        self.optpurse = optPurseSimul()
        self.optvis = OptVisualizeTool()
       # self.strategy = optStrategy()
        
        self.strategy = StaticStrategy()
        
        
        
        #확률 분석
        self.SuccessNo_inBand = 0
        self.Total_GambleNo = 0
       
        self.call_profit_ratio = 0
        self.put_profit_ratio = 0
        
        self.NoinBandQueue = deque(maxlen=300)

        
        
                        
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
        bscalc = BlackSholes_calc()
        util = PreprocessingUtility(self.df, self.tmanager, self.optcodetool)
        visualizer = VisualizationReporting(self.optvis)
        strategy_executor = Strategy(self.optpurse, self.bound, self.optcodetool, bscalc, self.profit_ratio_thres)
        #volatility_model = ForecastVolatility()   
        
        kospi_at_target = 0  #target kospi 에 대하여 
        index = 0
        for k in self.df["일자"]:
            print("cuurent data",k)
            index = index + 1
            cur_kospi_price = pd.to_numeric(self.df["현재지수"][index])
            curr_year, curr_month, curr_day = util.extract_date_parts(k)
            currday_dash = curr_year+'/'+curr_month+'/'+curr_day
            expire_month = util.get_next_expiration_month(curr_year, curr_month)
            volatility_model.update_price(price) # garch를 활용한 변동성
            
            
            if curr_year in ["2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023"]  :
                print("current year", curr_year)
 
                remaining_days = self.kospi_info.get_remaining_days(currday_dash,expire_month)                  # 잔여일 계산
                HV = self.kospi_info.get30dayHistorcalVol(currday_dash)                                         # 30일 HV 계산
                #HV = volatility_model.get_forecast_volatility()
                
                # 팔고싶은 옵션 가격 coverage_sigma를 통하여 승률 조정 현재 1.08은 80%w정도 승률 
                upperTarget, lowerTarget = self.kospi_info.currentTargetOptBand(cur_kospi_price,HV,remaining_days, self.coverage_sigma)
                 
                #IV 산출을 위한 임시 코드
                ###################################################################################################

                target_call_opt_code = self.optcodetool.optcode_gen(upperTarget,expire_month,'call')
                target_put_opt_code = self.optcodetool.optcode_gen(lowerTarget,expire_month,'put')
                
                try:
                    
                    #callPrice = self.loadOptPriceFromCSV(target_call_opt_code , currday_dash)   
                    callPrice = strategy_executor.loadOptPriceFromCSV(target_call_opt_code , currday_dash)   
                    upperTarget_IV = bscalc.getCallIV(upperTarget, pd.to_numeric(cur_kospi_price),0.03, pd.to_numeric(remaining_days)/365, callPrice)
              
                    
                    #putPrice = self.loadOptPriceFromCSV(target_put_opt_code, currday_dash)
                    putPrice = strategy_executor.loadOptPriceFromCSV(target_put_opt_code, currday_dash) 
                    lowerTarget_IV = bscalc.getPutIV(lowerTarget, pd.to_numeric(cur_kospi_price),0.03, pd.to_numeric(remaining_days)/365, putPrice)

 
                except :
                    upperTarget_IV = 0.0
                    lowerTarget_IV = 0.0
                    print("no file")
               

     
                minvalue = self.optpurse.MinEstForCurrentPortfolio(cur_kospi_price,expire_month)      # 해당 달의 최악의 경우 손실
                allowable_expense = self.optpurse.deposit/self.allowable_divide*-1                    # 1달동안 허용된 투자   
                unit  = int(self.optpurse.deposit/20000000)+1                                         # 하루에 살수 있는 수 

                
                                
                if minvalue > allowable_expense :
 
                    self.call_profit_ratio, self.put_profit_ratio = strategy_executor.execute_strategy(expire_month, upperTarget, lowerTarget, cur_kospi_price, remaining_days, currday_dash, unit)
                    
                        
                #날짜 검색해서 만기일이면 가지고 있는 옵션 결산
                current_year_month = curr_year+curr_month
                
                if self.kospi_info.get_expiration_date(current_year_month) == currday_dash:
                   code = self.optpurse.ExpirationOptionScan(current_year_month)
                   print("코드:",code)
                      
                   for i in code:
                      self.optpurse.ClearingOption(pd.to_numeric(cur_kospi_price),i)
                      
                      
                   print("총액", self.optpurse.deposit)  
                      
                      
                      

                expire_value = self.kospi_info.get_expiration_value(expire_month)

                self.Total_GambleNo = self.Total_GambleNo +1 ;
                if upperTarget >= expire_value and expire_value >= lowerTarget:
                    insideBound  = 1
                    self.SuccessNo_inBand = self.SuccessNo_inBand +1 ;    
        
                else:
                    insideBound = 0
                print("Gamble Probability ", self.SuccessNo_inBand/self.Total_GambleNo)
                
                self.NoinBandQueue.append(insideBound)
#          
                visualizer.visualize_data(currday_dash, self.optpurse.deposit, cur_kospi_price, upperTarget, lowerTarget, upperTarget_IV, lowerTarget_IV, expire_value, minvalue, HV, self.call_profit_ratio, self.put_profit_ratio)
                visualizer.report_probability(self.SuccessNo_inBand, self.Total_GambleNo, self.NoinBandQueue)
    
#kospi date load 초기화     
    def dataload(self):
        self.df = self.kospi_info.df


    def getSampleSize(self):
        return len(self.sample)
 

    
   #unit test code    
if __name__ == "__main__":
   # app = QApplication(sys.argv)
   
    optdata =  OptData() 
    optmon = Kospi200Simul(3.0,2.5,0.84,0.18)  # allowable_divide, bound, coverage_sigma, profit_ratio_thres):
    print(optmon.getSampleSize())
        #opthogamon observer 등록
    optmon.register_subject(optdata)
    
    try:
        optmon.start("201810")
    except:
        optmon.optvis.showDepositHistory()
        optmon.optvis.showKospi200History()
        optmon.optvis.showSuccessProbability()
        optmon.optvis.showProfitRatio()
        del optmon
