# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 14:51:43 2020

@author: USER
"""
from matplotlib import pyplot as plt
from optPurse import *
import numpy as np

class OptVisualizeTool():
    """
    This class is a tool for visualizing the options trade.
    """
    def __init__(self):
#        self.analtool =  DBalalysis("2");
        #date history
        self.date_history = []
        
        
        self.kospi200_history = []
        
        self.deposit_history = []
        self.upperbound_history = []
        self.lowerbound_history = []
        self.upperbound_IV_history = []
        self.lowerbound_IV_history = []
        self.insideband_history = [] # 1: 만기시 band kospi가 band 안에 존재 0: 존재 X
        self.callProfitRatio_history = []
        self.putProfitRatio_history = []
             
        self.expiration_value_history = []
        self.optmin_history = []
        self.HV_history = []
        self.IV_history = []
             
        self.fig = plt.figure()
 
             
    def stackDeposit(self, date, deposit):
        """
        from date and deposit data 
        stack the information 
        
        
        
        Args:
            option date :     "yyyy/mm/dd"
                   deposit :  deposit
        Returns:
            output:  deposit_history
    
        """
        self.deposit_history.append(deposit)
        
        

    
    def stackDate(self, curDate):
        self.date_history.append(curDate) 
        
    def stackKospi200(self, date, kospi200):
        self.kospi200_history.append(kospi200) 
    
    def stackUpperBound(self, date, upperboud):
        self.upperbound_history.append(upperboud) 

    def stackLowerBound(self, date, lowerbound):
        self.lowerbound_history.append(lowerbound) 
        
    def stackUpperIVBound(self, date, upperbound_IV):
        self.upperbound_IV_history.append(upperbound_IV) 

    def stackLowerIVBound(self, date, lowerbound_IV):
        self.lowerbound_IV_history.append(lowerbound_IV) 
        
    def stackinsideBand(self, date, inside_state):
        self.insideband_history.append(inside_state)
        
    def stackExpirationValue(self, expirationvalue):
        self.expiration_value_history.append(expirationvalue) 
        
    def stackCallProfitRatio(self, date, callProfitRatio):
        self.callProfitRatio_history.append(callProfitRatio) 

    def stackPutProfitRatio(self, date, putProfitRatio):
        self.putProfitRatio_history.append(putProfitRatio) 
        
        

    def stackMinValue(self, minvalue):
        self.optmin_history.append(minvalue)     
   
    def stackHVValue(self, HV):
        self.HV_history.append(HV)     
        
    def stackIVValue(self, IV):
        self.IV_history.append(IV)     
               
    def showDepositHistory(self):
        self.a = self.fig.add_subplot(4,1,1)
        step = 90
        plt.xticks(np.arange(0,len(self.date_history),step),self.date_history[1:len(self.date_history):step],rotation=20)
        self.a.plot(self.deposit_history)
        self.a.plot(self.optmin_history)
        self.a.legend(['deposit','optmin'])
            
    
    def showKospi200History(self):
        self.b = self.fig.add_subplot(4,1,2, sharex = self.a)
        self.b.plot(self.kospi200_history,label=['kospi200_history'])
        self.b.plot(self.upperbound_history)
        self.b.plot(self.lowerbound_history)

        self.b.plot(self.expiration_value_history)
        self.b.legend(['kospi200_history','upperbound','lowerbound','expiration_value_history'])
        
        #plt.show()

############################# 옵션 만기 이익 분포도
    def showProfitDistribution(self, optpurse, current_price, expiration_year_month):
        self.fig2 = plt.figure()
        self.c = self.fig2.add_subplot(1,1,2)
        
        
        mintick = int(current_price-30.0)
        maxtick = int(current_price+30.0)
        
        index = []
        valuetot = []
        
        premiumValue = optpurse.totalPremiumForCurrentPortfolio(expiration_year_month)
        for i in range(mintick, maxtick):
            expirationValue = optpurse.expireEstForCurrentPortfolio(i, expiration_year_month)
            currvalue = expirationValue + premiumValue;
            index.append(i)
            valuetot.append(currvalue)
            
        self.c.plot(index, valuetot)
        self.fig2.show()
        plt.show()
        
    def showSuccessProbability(self):
        self.d = self.fig.add_subplot(4,1,3, sharex = self.a)
        self.d.plot(self.insideband_history)
        self.d.plot(self.HV_history)
        self.d.plot(self.IV_history)
        #self.b.plot(self.upperbound_IV_history)
        #self.b.plot(self.lowerbound_IV_history)
        self.d.legend(['insideband_ratio', '30HV','IV'])
       # self.fig3.show()
        #plt.show()
    
    def showProfitRatio(self):
        self.f = self.fig.add_subplot(4,1,4, sharex = self.a)
        self.f.plot(self.callProfitRatio_history)
        self.f.plot(self.putProfitRatio_history)
        self.f.legend(['callProfitRatio','putProfitRatio'])
       # self.fig3.show()
        plt.show()
    
   #unit test code    
 
    
if __name__ == "__main__":

    optvis = OptVisualizeTool()
   
    optvis.stackDeposit("123",11)
    optvis.stackDeposit("123",15)
    optvis.stackDeposit("123",16)
    optvis.stackDeposit("123",17)
   
    optvis.showDepositHistory()
    optpurse = optPurseSimul()
    
    #2월 220 call option 매도  5000000 총액 35000000
    optpurse.SellOption("201P2220",20.0,1)
    print(optpurse.soldopt)
    print("deposit",optpurse.deposit)
    
    #2월 220 call option 매도 2500000 추가   총액 37500000
    optpurse.SellOption("201P2220",10.0,1)
    print(optpurse.soldopt)
    print("deposit",optpurse.deposit)
    #2월 220 call option 매도 15000000 추가 총액 52500000
    optpurse.SellOption("201P2220",20.0,3)
    print(optpurse.soldopt)
    print("deposit",optpurse.deposit)
    
    #3월 230 call option 매도 15000000  감소 총액 67500000
    optpurse.SellOption("201P2230",20.0,3)
    print(optpurse.soldopt)
    print("deposit",optpurse.deposit)
    
    #2월 220 call option 매수 15000000 감소 총액 52500000
    optpurse.BuyOption("201P2220",20.0,3)
    print(optpurse.boughtopt)
    print("deposit",optpurse.deposit)
    
    #3월 230 call option 매수 15000000 감소 총액 37500000 
    optpurse.BuyOption("201P2230",20.0,3)
    print(optpurse.boughtopt)
    print("deposit",optpurse.deposit)
    
    print(" ")
    print("매도",optpurse.soldopt)
    print("매수",optpurse.boughtopt)
    print("deposit",optpurse.deposit)
    

    optpurse.BuyOption("201P2240",20.0,1)
    optpurse.BuyOption("201P2250",20.0,1)
    optpurse.SellOption("201P2260",20.0,1)
    optpurse.BuyOption("201P2270",20.0,1)


    min = optpurse.MinEstForCurrentPortfolio(230,"201902")
    print("최소",min)
 
    optvis.showProfitDistribution( optpurse, 230.0, "201902")


# 서버에서 로드 후 visualization    
    optpurse.Initialization()
    optpurse.getOptInfoFromDeposit()
    print(optpurse.soldopt)
    print(optpurse.boughtopt)
    optvis.showProfitDistribution(optpurse,300.0,"202002")
    
    
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   