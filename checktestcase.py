# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 11:09:22 2019

@author: USER
"""

import unittest
from kospi_history import *
from optPurse import *

class TestKospiHistoryInfo(unittest.TestCase):
     
    
    def test_getTargetMonth(self):
        
        kospi_info = KOSPIHISTORYINFO()
               
        self.assertEqual(kospi_info.get_expiration_date("201602"),"2016/02/11")
        self.assertEqual(kospi_info.get_expiration_date("200002"),"There is no information for argument year month")
        
    def test_get_remaining_days(self):
        kospi_info = KOSPIHISTORYINFO()
        
        self.assertEqual(kospi_info.get_remaining_days("2016/02/22","201603"),12)
        self.assertEqual(kospi_info.get_remaining_days("2016/02/22","202203"),-1)
        
    def test_get90dayHistorcalVol(self):
        kospi_info = KOSPIHISTORYINFO()
        #print(kospi_info.get90dayHistorcalVol("2016/02/23"))
        self.assertEqual(int(kospi_info.get90dayHistorcalVol("2016/02/23")),15)
        
    
class TestoptPurse(unittest.TestCase):
    
    def test_purse(self):
        optpurse = optPurse("XingAPI")
        
        # 2월 220 call option 매도  5000000 총액 35000000
        optpurse.SellOption("201P2220",20.0,1)
        self.assertEqual(optpurse.deposit,35000000)  
       
        #2월 220 call option 매도 2500000 추가   총액 37500000
        optpurse.SellOption("201P2220",10.0,1)
        self.assertEqual(optpurse.deposit,37500000)  
        print(optpurse.soldopt)
        print("deposit",optpurse.deposit)
    
         #2월 220 call option 매도 15000000 추가 총액 52500000
        optpurse.SellOption("201P2220",20.0,3)
        self.assertEqual(optpurse.deposit,52500000)  
        print(optpurse.soldopt)
        print("deposit",optpurse.deposit)
        
        #2월 230 call option 매도 15000000  감소 총액 67500000
        optpurse.SellOption("201P2230",20.0,3)
        self.assertEqual(optpurse.deposit,67500000)  
        print(optpurse.soldopt)
        print("deposit",optpurse.deposit)
        
        #2월 220 call option 매수 15000000 감소 총액 52500000
        optpurse.BuyOption("201P2220",20.0,3)
        self.assertEqual(optpurse.deposit,52500000)  
        print(optpurse.boughtopt)
        print("deposit",optpurse.deposit)
        
        #2월 230 call option 매수 15000000 감소 총액 37500000 
        optpurse.BuyOption("201P2230",20.0,3)
        self.assertEqual(optpurse.deposit,37500000)  
        print(optpurse.boughtopt)
        print("deposit",optpurse.deposit)
        
        print(" ")
        print("매도",optpurse.soldopt)
        print("매수",optpurse.boughtopt)
        print("deposit",optpurse.deposit)
        
        #2월 220 모두 청산 240-220 손해 20*250000*5 25000000 감소 총액  12500000
        #2월 사놓았던              이익 20*250000*3 15000000 증가 총액  27500000
        
        
        
        
        code = optpurse.ExpirationOptionScan("201902")
        self.assertEqual(code[0],'201P2220')
        self.assertEqual(code[1],'201P2230')
        self.assertEqual(code[2],'201P2220')
        self.assertEqual(code[3],'201P2230')
        print("코드:",code)
    
        
    
        code = optpurse.ExpirationOptionScan("201902")
        print("코드:",code)
        
        
        print(optpurse.soldopt) 
        print(optpurse.boughtopt)
        est = optpurse.expireEstForCurrentPortfolio(230.0,"201902")
        print("만기추정", est)
        self.assertEqual(est,-5000000)
        #230 모두 청산 230-220 손해 10*250000*5 12500000  감소 총액   -12500000
                         #  이익 10*250000*3 75000000 증가 총액   +75000000         
    
        
        #2월 220 모두 청산 240-220 손해 20*250000*5 25000000 감소 총액  12500000
        #2월 230 모두 청산 230-220 손해 10*250000*3 7500000  감소 총액   5000000
        #2월 사놓았던      240-220 이익 20*250000*3 15000000 증가 총액  20000000  
        #2월 사놓았던      230-220 이익 10*250000*3 7500000  증가 총액  27500000  
        for i in code:
            optpurse.ClearingOption(240.0,i)
            
        self.assertEqual(optpurse.deposit,27500000)
        print("매도",optpurse.soldopt)
        print("매수",optpurse.boughtopt)
        print("deposit",optpurse.deposit)
        
        
        



if __name__ == '__main__':
    unittest.main()