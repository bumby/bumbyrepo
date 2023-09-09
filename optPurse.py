# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 16:49:58 2019

@author: USER
"""

import pandas as pd
import numpy as np
from OptCodeTool import *
from getMyDeposit import *

from abc import ABCMeta, abstractmethod

class optPurseInterface:
    
    __metaclass__=ABCMeta
    
    @abstractmethod
    
    def SellOption(self):
    
        pass
        
    
    @abstractmethod
    
    def BuyOption(self):
    
        pass
        
    
    @abstractmethod
    
    def GetOptInfo(self):
    
        pass
    
    
    @abstractmethod
    
    def GetDepositInfo(self):
    
        pass
    
   
    @abstractmethod
    
    def ExpirationProcess(self):  #simulation 에서만 진행
                                  #XingAPI 에서는 할 필요없음
        pass
  
    
    @abstractmethod
    
    def MinEstForCurrentPortfolio():
    
        pass
    
    
    
from opt_order_tr import *
from getMyDeposit import *
import time

class optPurse:
    def __init__(self):
    
        self.analtool = OptCodeTool()
        self.optorder = OptOrder()
        self.mydeposit = getMyDeposit()
        self.Initialization()
        self.getOptInfoFromServer()
        

    def Initialization(self):
        self.deposit = 30000000
        self.unitprice = 250000
        self.soldopt = np.array([["option","price","no"]])
        self.boughtopt = np.array([["option","price","no"]])  
        
    def SellOption(self, optionname, ordcode, price, no):
        orderno = self.optorder.order_option(optionname, "1", ordcode, price, no)    #ordercode 00 지정가 03 시장가
        print("orderno",orderno)
        #체결 확인 작업
        qty = 1
        cheq = 0
        allowabletime = 0
        success = True
#        while qty != cheq :
#            qty, cheq, ordrem = self.optorder.check_chegyol(optionname, orderno)
#            print("주문번호",orderno, "체결량",cheq, "미체결잔량",  ordrem)
#            time.sleep(1)
#            allowabletime = allowabletime + 1
#            if allowabletime == 10:
#                self.optorder.cancel_option( optionname, orderno, "1")
#                print("order has been canceled")
#                success = False
#                break
#        print("sell option completed")
#        #deposit 갱신
#        time.sleep(1)
#        self.getOptInfoFromServer()
        return success
            
    def BuyOption(self, optionname, ordcode, price, no):
        orderno = self.optorder.order_option(optionname, "2", ordcode, price, no)       #ordercode 00 지정가 03 시장가 
        print("orderno",orderno)
        #체결 확인 작업
        qty = 1
        cheq = 0
        allowabletime = 0
        success = True
#        while qty != cheq :
#            qty, cheq, ordrem = self.optorder.check_chegyol(optionname, orderno)
#            print("주문번호",orderno,"주문량",qty,  "체결량",cheq, "미체결잔량",  ordrem)
#            time.sleep(1)
#            allowabletime = allowabletime + 1
#            if allowabletime == 10:
#                self.optorder.cancel_option( optionname, orderno, "1")
#                print("order has been canceled")
#                success = False
#                break
#        print("buy option completed")
#        #deposit 갱신
#        time.sleep(1)
#        self.getOptInfoFromServer()
        return success        
        
    def GetDepositInfo(self): 
        return self.deposit
 
    def ExpirationProcess(self,current_year_month, kospi200price): 
        pass
    
    def MinEstForCurrentPortfolio(self, current_price,expiration_year_month):    
        #매번 option을 검사해야 하므로 시간이 걸릴 수 있음 
        #self.getOptInfoFromServer()
        
        mintick = int(current_price-100.0)
        maxtick = int(current_price+100.0)
        minvalue = self.expireEstForCurrentPortfolio(mintick, expiration_year_month)

        currvalue = self.expireEstForCurrentPortfolio(maxtick, expiration_year_month)
        
        if minvalue > currvalue :
           minvalue = currvalue
       
        
        return minvalue

        
    def getOptInfoFromServer(self):

        self.Initialization()
        print("Getting Deposit Infomation from server")
        
        self.deposit = pd.to_numeric(self.mydeposit.scanDeposit())
        print("예탁금 총액",self.deposit)
        deposit_stack = self.mydeposit.scanMyOpt()         #input 레코드갯수, 계좌번호, 입력비밀번호, 잔고평가구분, 선물가격평가구분
                                                                              #output 종목번호, 종목명, 매매구분, 미결재수량, 평균가, 현재가, 평가금액
        print(deposit_stack)
        print(deposit_stack.shape[0],deposit_stack.shape[1])
        for index in range(deposit_stack.shape[0]):
            
            FnoIsuNo = deposit_stack[index][0]
            BnsTpCode = pd.to_numeric(deposit_stack[index][2])
            FnoAvrPrc = pd.to_numeric(deposit_stack[index][4])
            UnsttQty = pd.to_numeric(deposit_stack[index][3])
            print(index,FnoIsuNo, BnsTpCode, FnoAvrPrc, UnsttQty)
            if BnsTpCode == 0:
                #self.BuyOption(FnoIsuNo, FnoAvrPrc, UnsttQty)
                
                newopt = np.array([FnoIsuNo, FnoAvrPrc, UnsttQty])
                self.boughtopt = np.vstack((self.boughtopt,newopt))
            else:
                #self.SellOption(FnoIsuNo, FnoAvrPrc, UnsttQty)
                newopt = np.array([FnoIsuNo, FnoAvrPrc, UnsttQty])
                self.soldopt = np.vstack((self.soldopt,newopt))
        
       
    #차월 만기시 추정 이익 만기월 기재 
    def expireEstForCurrentPortfolio(self, expiration_price, expiration_year_month):
        
        est = 0
        optsoldno = len(self.soldopt)       
        for i in range(1,optsoldno):
            putncall,expiration_year,expiration_month,optstrike = self.analtool.optcode_encode(self.soldopt[i,0])
            if  expiration_year_month == (expiration_year+expiration_month) :
                profit = self.CalcProfit(expiration_price, self.soldopt[i,0])
                est = est - pd.to_numeric(self.soldopt[i,2])*profit*self.unitprice # 옵션당

                   
                       
        optboughtno = len(self.boughtopt)       
        for i in range(1,optboughtno):
            putncall,expiration_year,expiration_month,optstrike = self.analtool.optcode_encode(self.boughtopt[i,0])
            if  expiration_year_month == (expiration_year+expiration_month) :
                profit = self.CalcProfit(expiration_price, self.boughtopt[i,0] )
                est = est + pd.to_numeric(self.boughtopt[i,2])*profit*self.unitprice # 옵션당

        return est      
    
            #self.soldopt = np.delete(self.soldopt, (1), axis=0)
    def  CalcProfit(self, current_price, optcode):
       
        call_or_put,expire_year,expire_month,expire_price = self.analtool.optcode_encode(optcode)
                
        if call_or_put == 'call':
            if current_price > expire_price:
                return current_price-expire_price
            else:
                return 0
        
        if call_or_put == 'put':
            if current_price < expire_price:
                return expire_price-current_price
            else:
                return 0
        
        
    
class optPurseSimul:
    def __init__(self):
#        self.analtool =  DBalalysis("2");
        self.analtool = OptCodeTool()      
         
        
#        self.deposit = 30000000
#        self.unitprice = 250000
#        self.soldopt = np.array([["option","price","no"]])
#        self.boughtopt = np.array([["option","price","no"]])
        self.Initialization()
        
    def Initialization(self):
        self.deposit = 30000000
        self.unitprice = 250000
        self.soldopt = np.array([["option","price","no"]])
        self.boughtopt = np.array([["option","price","no"]])       
        
    def SellOption(self, optionname,ordcode,  price, no):
        """
        from option name ,price ,option number
        stack the option information into purse
        
        
        
        Args:
            option name : "201P2220"  
                        
                          "201" call "301" put
                          "P"   year
                          "2"   month
                          "220" price
        
        Returns:
            no
    
        stack soldopt = ['name','price', 'no']
    
        """
        
        print("004 옵션 매도")
        #기존에 있던 option인가? 
        self.deposit = self.deposit + price*no*self.unitprice
        
        #기존에 있는 옵션이면 수치 변경 
        optsoldno = len(self.soldopt) 
        optpresence = False

        for i in range(optsoldno):
            if self.soldopt[i,0] == optionname:
                
                totalprice = pd.to_numeric(self.soldopt[i,1])*pd.to_numeric(self.soldopt[i,2]) + pd.to_numeric(price)*pd.to_numeric(no)
                totalno =  pd.to_numeric(self.soldopt[i,2])+pd.to_numeric(no)
                
                self.soldopt[i,1] = totalprice/totalno
                self.soldopt[i,2] = totalno
                
                
                optpresence = True
                break            
        
        #기존에 없는 옵션이면 추가
        if optpresence == False:
            newopt = np.array([optionname, price, no])
            self.soldopt = np.vstack((self.soldopt,newopt))
    
    
      
            
        
    def BuyOption(self, optionname, ordcode, price, no):
        """
        from option name ,price ,option number
        stack the option information into purse
        
        
        
        Args:
            option name : "201P2220"  
                        
                          "201" call "301" put
                          "P"   year
                          "2"   month
                          "220" price
        
        Returns:
            no
    
        stack soldopt = ['name','price', 'no']
    
        """
        print("buy opttion called")
        
        self.deposit = self.deposit - price*no*self.unitprice
  
        #기존에 있는 옵션이면 수치 변경 
        optboughtno =  len(self.boughtopt) 
        optpresence = False
        for i in range(optboughtno):
            if self.boughtopt[i,0]==optionname:
                
                totalprice = pd.to_numeric(self.boughtopt[i,1])*pd.to_numeric(self.boughtopt[i,2]) + pd.to_numeric(price)*pd.to_numeric(no)
                totalno =  pd.to_numeric(self.boughtopt[i,2])+pd.to_numeric(no)
                
                self.boughtopt[i,1] = totalprice/totalno
                self.boughtopt[i,2] = totalno
                
                
                optpresence = True
                break              
        #기존에 있던 option인가?
        if optpresence == False: 
            newopt = np.array([optionname, price, no])
            self.boughtopt = np.vstack((self.boughtopt,newopt))
        
        
        
        
    def GetDepositInfo(self): 
        return self.deposit      
            
    def ExpirationProcess(self,current_year_month, kospi200price):
        
        code = self.ExpirationOptionScan(current_year_month)
             #  print("코드:",code)
        for i in code:
            self.ClearingOption(kospi200price,i)
    
    
    def ExpirationOptionScan(self, curr_year_month):
        """
        cuur_year_month : "yyyymm"
        """
        current_month_target = [];
        
        optcode = self.analtool.optcode_gen(234.0, curr_year_month, "call")  #code를  234, call로 생성을 했으나 optcode를 사용하기위한 목적이며 year,month 정보만 사용하였다. 
        
        
        optsoldno = len(self.soldopt)       
        for i in range(optsoldno):
            optname = self.soldopt[i,0]            
            if  optcode[3:5]==optname[3:5]:
                current_month_target.append(optname)
                
        
        optboughtno = len(self.boughtopt)       
        for i in range(optboughtno):
            optname = self.boughtopt[i,0]            
            if  optcode[3:5]==optname[3:5]:
                current_month_target.append(optname)
        
        return current_month_target








# 알고리즘 고속화 필요
        #옵션 청산 작업
    def ClearingOption(self, expiration_price, expired_option):
        
              
        profit = self.CalcProfit(expiration_price, expired_option )
       
        optsoldno = len(self.soldopt)       
        for i in range(optsoldno):
            if self.soldopt[i,0]==expired_option:
                self.deposit = self.deposit - pd.to_numeric(self.soldopt[i,2])*profit*self.unitprice # 옵션당
                self.soldopt = np.delete(self.soldopt, (i), axis=0)
                break
        
        optboughtno = len(self.boughtopt)       
        for i in range(optboughtno):
            if self.boughtopt[i,0]==expired_option:
        
                self.deposit = self.deposit + pd.to_numeric(self.boughtopt[i,2])*profit*self.unitprice # 옵션당
                self.boughtopt = np.delete(self.boughtopt, (i), axis=0)
                break
            
            
    #차월 만기시 추정 이익 만기월 기재 
    def expireEstForCurrentPortfolio(self, expiration_price, expiration_year_month):
        
        est = 0
        optsoldno = len(self.soldopt)       
        for i in range(1,optsoldno):
            putncall,expiration_year,expiration_month,optstrike = self.analtool.optcode_encode(self.soldopt[i,0])
            if  expiration_year_month == (expiration_year+expiration_month) :
                profit = self.CalcProfit(expiration_price, self.soldopt[i,0])
                est = est - pd.to_numeric(self.soldopt[i,2])*profit*self.unitprice # 옵션당

                   
                       
        optboughtno = len(self.boughtopt)       
        for i in range(1,optboughtno):
            putncall,expiration_year,expiration_month,optstrike = self.analtool.optcode_encode(self.boughtopt[i,0])
            if  expiration_year_month == (expiration_year+expiration_month) :
                profit = self.CalcProfit(expiration_price, self.boughtopt[i,0] )
                est = est + pd.to_numeric(self.boughtopt[i,2])*profit*self.unitprice # 옵션당

        return est
            
    
    
    #premium 총 각 월의 option 가치 평가에 사용
    def totalPremiumForCurrentPortfolio(self, expiration_year_month):
        est = 0
        optsoldno = len(self.soldopt)       
        for i in range(1,optsoldno):
            putncall,expiration_year,expiration_month,optstrike = self.analtool.optcode_encode(self.soldopt[i,0])
            if  expiration_year_month == (expiration_year+expiration_month) :
                premium = pd.to_numeric(self.soldopt[i,1])
                est = est + pd.to_numeric(self.soldopt[i,2])*premium*self.unitprice # 옵션당

                   
                       
        optboughtno = len(self.boughtopt)       
        for i in range(1,optboughtno):
            putncall,expiration_year,expiration_month,optstrike = self.analtool.optcode_encode(self.boughtopt[i,0])
            if  expiration_year_month == (expiration_year+expiration_month) :
                premium = pd.to_numeric(self.boughtopt[i,1])
                est = est - pd.to_numeric(self.boughtopt[i,2])*premium*self.unitprice # 옵션당
        return est
    
    #최소 옵션치 추정
    def MinEstForCurrentPortfolio(self, current_price,expiration_year_month):     
        mintick = int(current_price-100.0)
        maxtick = int(current_price+100.0)
        minvalue = self.expireEstForCurrentPortfolio(mintick, expiration_year_month)
#        for i in range(mintick, maxtick):
#            currvalue = self.expireEstForCurrentPortfolio(i, expiration_year_month)
#            if minvalue > currvalue :
#                minvalue = currvalue
#        
        currvalue = self.expireEstForCurrentPortfolio(maxtick, expiration_year_month)
        
        if minvalue > currvalue :
           minvalue = currvalue
       
        
        return minvalue
        

                  
        #self.soldopt = np.delete(self.soldopt, (1), axis=0)
    def  CalcProfit(self, current_price, optcode):
       
        call_or_put,expire_year,expire_month,expire_price = self.analtool.optcode_encode(optcode)
                
        if call_or_put == 'call':
            if current_price > expire_price:
                return current_price-expire_price
            else:
                return 0
        
        if call_or_put == 'put':
            if current_price < expire_price:
                return expire_price-current_price
            else:
                return 0
        
        
 
        
    def getOptInfoFromServer(self):

        mydeposit = getMyDeposit()
        
        self.Initialization()
        print("no such data mode")
        
        self.deposit = pd.to_numeric(mydeposit.scanDeposit())
        print("예탁금 총액",self.deposit)
        deposit_stack = mydeposit.scanMyOpt()         #input 레코드갯수, 계좌번호, 입력비밀번호, 잔고평가구분, 선물가격평가구분
                                                                              #output 종목번호, 종목명, 매매구분, 미결재수량, 평균가, 현재가, 평가금액
        print(deposit_stack)
        print(deposit_stack.shape[0],deposit_stack.shape[1])
        for index in range(deposit_stack.shape[0]):
            
            FnoIsuNo = deposit_stack[index][0]
            BnsTpCode = pd.to_numeric(deposit_stack[index][2])
            FnoAvrPrc = pd.to_numeric(deposit_stack[index][4])
            UnsttQty = pd.to_numeric(deposit_stack[index][3])
            print(index,FnoIsuNo, BnsTpCode, FnoAvrPrc, UnsttQty)
            if BnsTpCode == 0:
                self.BuyOption(FnoIsuNo, "00",FnoAvrPrc, UnsttQty)
            else:
                self.SellOption(FnoIsuNo, "00",FnoAvrPrc, UnsttQty)
        print("옵션 추가 총액",self.deposit)
       
        
            
        
if __name__=="__main__":
    
  #hts ordertest  
    
    secinfo = secInfo() #계좌 정보 holder
    
    bestaccess = BestAccess()
    bestaccess.comm_connect(secinfo)
    
    
    optpurse = optPurse()
    #2월 220 call option 매도  5000000 총액 35000000
    optpurse.SellOption("201R4417","00",2.89,1)
    print(optpurse.soldopt)
    print("deposit",optpurse.deposit)
    
#    
#    
#    #2월 220 call option 매도 2500000 추가   총액 37500000
#    optpurse.SellOption("201Q3280","00",2.89,1)
#    print(optpurse.soldopt)
#    print("deposit",optpurse.deposit)
#    #2월 220 call option 매도 15000000 추가 총액 52500000
#    optpurse.SellOption("201Q3280","00",2.89,3)
#    print(optpurse.soldopt)
#    print("deposit",optpurse.deposit)
#    
#    #3월 230 call option 매도 15000000  감소 총액 67500000
#    optpurse.SellOption("201Q3280","00",2.89,3)
#    print(optpurse.soldopt)
#    print("deposit",optpurse.deposit)
#    
#    #2월 220 call option 매수 15000000 감소 총액 52500000
#    optpurse.BuyOption("201Q3280","00",2.89,3)
#    print(optpurse.boughtopt)
#    print("deposit",optpurse.deposit)
#    
#    #3월 230 call option 매수 15000000 감소 총액 37500000 
#    optpurse.BuyOption("201Q3280","00",2.89,3)
#    print(optpurse.boughtopt)
#    print("deposit",optpurse.deposit)
#    
#    print(" ")
#    print("매도",optpurse.soldopt)
#    print("매수",optpurse.boughtopt)
#    print("deposit",optpurse.deposit)
#    
#
#    
#    #code = optpurse.ExpirationOptionScan("201902")
#    optpurse.ExpirationProcess("201902", 280.0)
#    
#    
#    #2월 220 모두 청산 240-220 손해 20*250000*5 25000000 감소 총액  12500000
#    #2월 230 모두 청산 230-220 손해 10*250000*3 7500000  감소 총액   5000000
#    #2월 사놓았던      240-220 이익 20*250000*3 15000000 증가 총액  20000000  
#    #2월 사놓았던      230-220 이익 10*250000*3 7500000  증가 총액  27500000  
#    
#    print(optpurse.soldopt) 
#    print(optpurse.boughtopt)
#    est = optpurse.expireEstForCurrentPortfolio(230.0,"202003")
#    print("만기추정", est)
#    #230 모두 청산 230-220 손해 10*250000*5 12500000  감소 총액   -12500000
#                         #  이익 10*250000*3 75000000 증가 총액   +75000000    
#    min = optpurse.MinEstForCurrentPortfolio(230.0,"202003")
#    print("만기 최소값",min)
#    
#    
#         
#    print("매도",optpurse.soldopt)
#    print("매수",optpurse.boughtopt)
#    print("deposit",optpurse.deposit)
#    

 
    