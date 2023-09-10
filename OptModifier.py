# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 10:59:02 2023

@author: USER
"""
import datetime
import random
from subject import *
from OptCodeTool import OptCodeTool
from blacksholes_calc import BlackSholes_calc

class OptModifier:
    def __init__(self, opt_data=None):
 #       if opt_data is None:
 #           self.opt_data = OptData()
 #       else:
 #           self.opt_data = opt_data
        self.tool = OptCodeTool()

    def initialize_optChart(self, opt_data, hogaTime, num_options=10 ):
        hogaTime = "20230910"
        S0 = 336.0
        r = 0.02
        T = 1.0/12.0

        bs = BlackSholes_calc()

        for _ in range(num_options):
            # ... [생략] ...

            opt_strike = S0 + random.choice([-20, -15, -10, -5, 0, 5, 10, 15, 20])  # 현재의 kospi200 가격을 중심으로 strike 값을 선택합니다.
            opt_month = "10"
            opt_year = "2023"
            put_or_call = random.choice(["call", "put"])
            
            opt_tool = OptCodeTool()
            m_optCode = opt_tool.optcode_gen(opt_strike, opt_year + opt_month, put_or_call)
            
            if put_or_call == "call":
                sigma = 0.11
                theoretical_price = bs.getCallPrice(opt_strike, S0, r, sigma, T)
            else:
                sigma = 0.13
                theoretical_price = bs.getPutPrice(opt_strike, S0, r, sigma, T)

            # 임의의 가격 변동을 추가하여 offerho1 및 bidho1 값을 설정합니다.
            offerho1 = str(theoretical_price + random.uniform(0, 1))  
            bidho1 = str(theoretical_price - random.uniform(0, 1))
            
            opt_data.change_optprice(hogaTime, m_optCode, offerho1, bidho1, str(theoretical_price))

    def random_modify_opt(self, opt_data, hogaTime,  r=0.02): 

        bs = BlackSholes_calc()
        opt_tool = OptCodeTool()  # OptCodeTool의 인스턴스 생성

        # 호가 타임을 기준으로 만기일까지 남은 시간을 계산합니다.
        hoga_date = datetime.datetime.strptime(hogaTime, '%Y/%m/%d').date()  # 'YYYY/MM/DD' 형식의 문자열을 date 객체로 변환
        expiry_date = datetime.date(hoga_date.year, hoga_date.month, 9)  # 만기일을 대략 9일로 지정
        if hoga_date >= expiry_date:
            if hoga_date.month == 12:
                expiry_date = datetime.date(hoga_date.year + 1, 1, 9)
            else:
                expiry_date = datetime.date(hoga_date.year, hoga_date.month + 1, 9)
        days_to_expiry = (expiry_date - hoga_date).days
        T = days_to_expiry / 365.0
        if T<0.001:
            T = 0.001
    
        # optChart에서 임의의 옵션을 선택합니다.
        random_optCode = random.choice(list(opt_data.keys()))
    
        # 선택된 옵션의 값을 임의로 변경합니다.
        _, _, _, opt_strike = opt_tool.optcode_encode(random_optCode)  # OptCodeTool을 사용하여 S0 값을 가져옵니다.
        S0 = opt_strike
    
        put_or_call = "call" if "C" in random_optCode else "put"  # optCode를 분석하여 call인지 put인지 판별합니다. 
        
        if put_or_call == "call":
            sigma = 0.11
            theoretical_price = bs.getCallPrice(opt_strike, S0, r, sigma, T)
        else:
            sigma = 0.13
            theoretical_price = bs.getPutPrice(opt_strike, S0, r, sigma, T)
    
        # 임의의 가격 변동을 추가하여 offerho1 및 bidho1 값을 설정합니다.
        offerho1 = str(theoretical_price + random.uniform(0, 1))  
        offerho2 = str(theoretical_price + random.uniform(0, 1) + 0.01)  # 적절한 수정 필요
        bidho1 = str(theoretical_price - random.uniform(0, 1))
        bidho2 = str(theoretical_price - random.uniform(0, 1) - 0.01) # 적절한 수정 필
        
        theoryprice = str(theoretical_price)
        return hogaTime, random_optCode, offerho1, bidho1, offerho2, bidho2,  theoryprice
    #opt_data.change_optprice(hogaTime, random_optCode, offerho1, bidho1, theoryprice)


if __name__ == "__main__":
    modifier = OptModifier()

    print("Initial optChart:")
    modifier.initialize_optChart(modifier.opt_data)
    modifier.opt_data.print_opt()

    print("\nModified optChart:")
    modifier.random_modify_opt(modifier.opt_data)
    modifier.opt_data.print_opt()