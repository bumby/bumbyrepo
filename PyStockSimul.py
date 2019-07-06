# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 09:52:51 2018

@author: USER
"""
from PyMon import *

class MyAsset:
    def __init__(self):
        self.Deposit = 10000000
        self.stock_amt = 0 #보유수 현재가
        
    def buy_stock(self,  st_num, st_price):
        if  st_price*st_num < self.Deposit :        
            self.Deposit = self.Deposit - st_price*st_num
            self.stock_amt = self.stock_amt + st_num
        else:
            print("잔고 부족")
            
  
    def sell_stock(self, st_num, st_price):
        if self.stock_amt < st_num:
            self.Deposit = self.Deposit + st_price*st_num
            self.stock_amt = self.stock_amt - st_num
        else:
            print("보유주식 부족")
            
    def eval_asset(self, st_price):
        print("자산가치", self.Deposit + self.stock_amt*st_price)
        

class Strategy:
    def __init__(self, hist):
        self.hist = hist      
        
    def get_chart_sim(self, date):
        prices = self.hist['close']
        volumes = self.hist['volumn']
        date_list = list(prices.keys())

        date_ext = []
        price_ext = []
        volume_ext = []
        i = 0
        while date_list[i] != date:
            i= i+1;
        
        while i < len(prices):
            price_ext.append(prices[i])
            volume_ext.append(volumes[i])
            date_ext.append(date_list[i])
            i=i+1
            

     #   print("date",date, "date ext", date_ext)
        return price_ext, volume_ext
                      
    def basic(self, date, price, volume):
        prices, volumes = self.get_chart_sim(date)
            
        if len(volumes)<21:
            return False
        sum_vol20 = 0
        today_vol = 0

        for i, vol in enumerate(volumes):

                    
            if i==0:
                today_vol = vol
            elif 1 <= i <= 20:
                sum_vol20 += vol
            else:
                break
            
        avg_vol20 = sum_vol20 / 20
        print("평균",avg_vol20,"거래",today_vol)
        if today_vol > avg_vol20*5:
            print("급등 거래")
            return True
        
        
        
 
        
   
class Simul:
    def __init__(self):
        self.myasset = MyAsset()  #자산 관리
        self.pymon = PyMon()      #모니터 프로그램
        today = datetime.datetime.today().strftime("%Y%m%d")
        self.hist = self.pymon.get_ohlcv("036540", "20180320", today)  #일당 주식 데이타 
        self.strt = Strategy(self.hist)
                
    def step(self, date, price, volume):
        if self.strt.basic(date, price, volume):
            self.myasset.buy_stock(10,price)
        self.myasset.eval_asset(price)
               
    def run(self):
        prices = self.hist['close']
        volumes = self.hist['volumn'] 
        date_list = list(prices.keys())
        for i,vol in reversed(list(enumerate(volumes))): #enumerate(volumes):
            self.step(date_list[i], prices[date_list[i]], volumes[date_list[i]]) # 날짜, 주가, 거래량 전달
          
       
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    simul = Simul()
    simul.run()     
