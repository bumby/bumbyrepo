# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 20:10:57 2019

@author: USER
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from timeManager import *
import math


#data = pd.read_csv("kospi200data.csv",sep=",")
#
#data.head()
#df = data[["일자","현재지수"]]
#print(df["일자"])
#
#dff = df["현재지수"]
#
#res = []
#
#
#opt_expire_date = [
#    "2013/01/10","2013/02/14","2013/03/14","2013/04/11","2013/05/09","2013/06/13","2013/07/11","2013/08/08","2013/09/12","2013/10/10","2013/11/14","2013/12/12",
#    "2014/01/09","2014/02/13","2014/03/13","2014/04/10","2014/05/08","2014/06/12","2014/07/10","2014/08/14","2014/09/11","2014/10/08","2014/11/13","2014/12/11",
#    "2015/01/08","2015/02/12","2015/03/12","2015/04/09","2015/05/14","2015/06/11","2015/07/09","2015/08/13","2015/09/10","2015/10/08","2015/11/12","2015/12/10",
#    "2016/01/14","2016/02/11","2016/03/10","2016/04/14","2016/05/12","2016/06/09","2016/07/14","2016/08/11","2016/09/08","2016/10/13","2016/11/10","2016/12/08",
#    "2017/01/12","2017/02/09","2017/03/09","2017/04/13","2017/05/11","2017/06/08","2017/07/13","2017/08/10","2017/09/14","2017/10/12","2017/11/09","2017/12/14",
#    "2018/01/11", "2018/02/08", "2018/03/08", "2018/04/12","2018/05/10", "2018/06/14","2018/07/12", "2018/08/09","2018/09/13","2018/10/11","2018/11/08","2018/12/13"
#    "2019/01/10","2019/02/14","2019/03/14","2019/04/11", "2019/05/09","2019/06/13","2019/07/11","2019/08/08","2019/09/11","2019/10/10","2019/11/14","2019/12/12"
#    ]
#
#
#
#
#expire_index = 1
##for i in range(2994,df["현재지수"].size):
#
##HV 산출
#
#
#
#
#for i in range(2994,4428):
#    j=0
#    while  df["일자"][i+j]!=opt_expire_date[expire_index]: #만기일 찾기
#        j=j+1
#
#        
#    print(i, df["일자"][i],df["일자"][i+j],opt_expire_date[expire_index], j, df["현재지수"][i+j],df["현재지수"][i] ,(df["현재지수"][i+j]-df["현재지수"][i])/df["현재지수"][i])
#    res.append((df["현재지수"][i+j]-df["현재지수"][i])/df["현재지수"][i]) #만기일의 지수값과 현재 지수값의 차이 추출
#
#    if df["일자"][i]==df["일자"][i+j]:
#        expire_index = expire_index + 1
#    
#
#print(res)
#
##plt.plot.line(res)
#reslist = pd.Series(res)
#plt.figure(1)
#reslist.plot.hist(grid=True, bins=50, rwidth=1, color='#607c8e')
#plt.title('target option 괴리율 distribution')
#plt.xlabel('괴리율')
#plt.ylabel('counts')
#plt.grid(axis='y', alpha=0.75)
##res.plot.hist(grid=True, bins=50, rwidth=1, color='#607c8e')
#
##print(opt_expire_date)
#plt.show()    


class HistVol:
    def __init__(self):
        
        self.S=[147.82, 149.5, 149.78, 149.86, 149.93, 150.89, 152.39, 153.74, 152.79, 151.23, 151.78]
        self.N = len(self.S)
            
    def getHV(self, data):
        self.S = data
        self.N = len(self.S)
    
        R = []
        sum = 0
        for i in range(0,self.N-1):
            R.append(math.log(self.S[i+1]/self.S[i]))
            sum = sum + R[i]
            #print(i, self.S[i])
        
        #print('sum',sum, 'sumsum', math.log(self.S[10]/self.S[0]))
        R_mean = sum/(self.N-1)
       
        sum = 0
        Rt = []
        for i in range(0,self.N-1):
            Rt.append((R[i]-R_mean)**2)
            sum = sum + Rt[i]
            #print(i, Rt[i])
            
        #print(Rt)
        STD = math.sqrt(sum/(self.N-2))*100
        self.HV  = STD*math.sqrt(252)
        #print("STD",STD ,"HV", self.HV)
        return self.HV
    
    
    
        
    
    

class KOSPIHISTORYINFO:
    def __init__(self):
        
       
        self.data = pd.read_csv("kospi200data.csv",sep=",")
        self.data.head()
        self.df = self.data[["일자","현재지수"]]
        #print(self.df["일자"])
        #self.dff = df["현재지수"] 

        self.opt_expire_dict = { "201301":"2013/01/10","201302":"2013/02/14","201303":"2013/03/14","201304":"2013/04/11","201305":"2013/05/09","201306":"2013/06/13","201307":"2013/07/11","201308":"2013/08/08","201309":"2013/09/12","201310":"2013/10/10","201311":"2013/11/14","201312":"2013/12/12"\
                                ,"201401":"2014/01/09","201402":"2014/02/13","201403":"2014/03/13","201404":"2014/04/10","201405":"2014/05/08","201406":"2014/06/12","201407":"2014/07/10","201408":"2014/08/14","201409":"2014/09/11","201410":"2014/10/08","201411":"2014/11/13","201412":"2014/12/11"\
                                ,"201501":"2015/01/08","201502":"2015/02/12","201503":"2015/03/12","201504":"2015/04/09","201505":"2015/05/14","201506":"2015/06/11","201507":"2015/07/09","201508":"2015/08/13","201509":"2015/09/10","201510":"2015/10/08","201511":"2015/11/12","201512":"2015/12/10"\
                                ,"201601":"2016/01/14","201602":"2016/02/11","201603":"2016/03/10","201604":"2016/04/14","201605":"2016/05/12","201606":"2016/06/09","201607":"2016/07/14","201608":"2016/08/11","201609":"2016/09/08","201610":"2016/10/13","201611":"2016/11/10","201612":"2016/12/08"\
                                ,"201701":"2017/01/12","201702":"2017/02/09","201703":"2017/03/09","201704":"2017/04/13","201705":"2017/05/11","201706":"2017/06/08","201707":"2017/07/13","201708":"2017/08/10","201709":"2017/09/14","201710":"2017/10/12","201711":"2017/11/09","201712":"2017/12/14"\
                                ,"201801":"2018/01/11","201802":"2018/02/08","201803":"2018/03/08","201804":"2018/04/12","201805":"2018/05/10","201806":"2018/06/14","201807":"2018/07/12","201808":"2018/08/09","201809":"2018/09/13","201810":"2018/10/11","201811":"2018/11/08","201812":"2018/12/13"\
                                }
                                #,"2019/01/10","2019/02/14","2019/03/14","2019/04/11", "2019/05/09","2019/06/13","2019/07/11","2019/08/08","2019/09/11","2019/10/10","2019/11/14","2019/12/12"

        self.timemanager =  timeManager()
        self.histvol = HistVol()
        
        
    def get_expiration_info(self, curr_date_index):    
        """  
        Returns the expiration date of the target month, remaining days, the kospi200 index at expiration date 
        
        
        
        Returns:
            expire_date :  the 
        """
        curr_date = self.df["일자"][curr_date_index] 
        curr_date_split = curr_date.split('/')
        
        target_expire_month = self.timemanager.getNextYearMonth(int(curr_date_split[0]),int(curr_date_split[1]))
        expire_date = self.opt_expire_dict[target_expire_month]
        #print(expire_date)
        
        remained_day = 0
        while self.df["일자"][curr_date_index+remained_day]!= expire_date:
            #print(self.df["일자"][curr_date_index+remained_day], expire_date )
            remained_day = remained_day + 1
            
        expired_kospi200 = self.df["현재지수"][i+remained_day]
        return expire_date, remained_day, expired_kospi200
    
    
    
    def get_expiration_date(self, expiration_year_month):
        """
        Returns the expiration date for given "year+month" information
        
        Args:
            expiration_year_month : "year+month" 
        
        Returns:
            expiration_year_month_day : "year/month/day"
    
        bound [201301 ~ 201812]
        
        ex) 
            get_expiration_date("201602")
            "2016/02/11"
            
            get_expiration_date("200001")
            "There is no information for argument year month"            

        """
        try:
            expiration_year_month_day = self.opt_expire_dict[expiration_year_month] 
            return expiration_year_month_day
        except:
            print("error at get_expiration_date!!!", expiration_year_month )
            return "There is no information for argument year month"
    


        
    def get_remaining_days(self, current_year_month_date, expiration_year_month):
        """
        Returns no of day between the expiration date of target month and current year/monthfor/date 
        
        Args:
            current_year_month_date : "year/month/date" 
            expiration_year_month   : "year+month"
            
        Returns:
            remaining_days : "remaining days"
    
        bound [201301 ~ 201812]
        
        ex) 
            get_expiration_date("2016/02/23","201603")
                       
            error case 1 return -1
            the current date is exceeds the end of the bound
            get_expiration_date("2017/02/23","201603")
            
            error case 2 return -1
            the current date is exceeds the target month 
            get_expiration_date("2020/02/23","201603")
      
        """
       # selected_table = self.df['일자'].loc([current_year_month_date,self.get_expiration_date(expiration_year_month)])
        try:
            f1 = self.df[self.df['일자']==current_year_month_date]
            f2 = self.df[self.df['일자']==self.get_expiration_date(expiration_year_month)]
            
            remaining_days = f2.index[0]-f1.index[0]
            
            if remaining_days < 0 :
                print("error at get_remaining_days!!!", "current_year_month_date", current_year_month_date, "expiration_year_month",expiration_year_month )
                return -1
            else:
                return remaining_days
            
        except:
            print("error at get_remaining_days!!!", "current_year_month_date", current_year_month_date, "expiration_year_month",expiration_year_month )
            return -1
        
        
    
    def get90dayHistorcalVol(self, curr_year_month_date):
        """
        Returns 90days Historcal Volatility from year/monthfor/date 
        
        Args:
            curr_date_index : "year/month/date" 
         
            
        Returns:
            HV : 90days Historcal Volatility
    
        bound [201301 ~ 201812]
        
        ex) 
            get90dayHistorcalVol("2016/02/23")
                       
            error case 1 return -1
            the current date is exceeds the end of the bound
            get_expiration_date("2020/02/23")
            

      
        """
        f1 = self.df[self.df['일자']==curr_year_month_date]
        curr_date_index = f1.index[0]
        
        
        if(curr_date_index < 90):
            print("data is less than 90days0!!!")
            exit()
        
        i = curr_date_index-90
        self.stack_90day = []
        while i<curr_date_index:
            i=i+1
            self.stack_90day.append(self.df["현재지수"][i])
        #print(self.stack_90day)
        return self.histvol.getHV(self.stack_90day)
  
      
    def currentTargetOptBand(self, current_kospi_200, current_HV, remained_day):
        kospi200price = pd.to_numeric(current_kospi_200)
        
        jandatecnt = remained_day
        HV = current_HV
        #jandatecnt = pd.to_numeric(remained_day)
        #HV =  pd.to_numeric(current_HV) #1.2 는 증폭 ratio이다. 
        #self.HV = 13.46 #전광판엑서 제공한함 다른 방법 필요
        
               
        sigma = HV/100.0*math.sqrt(jandatecnt/252.0)
        upperTarget = math.exp(math.log(kospi200price)+sigma*1.3) #1.3은 normal distribution 90% 범위
        lowerTarget = math.exp(math.log(kospi200price)-sigma*1.3) #1.3은 normal distribution 90% 범위     
        return upperTarget, lowerTarget      
    

if __name__ == '__main__':
    
    kospi_info = KOSPIHISTORYINFO()
    
    print(kospi_info.get_expiration_date("201602"))
    print(kospi_info.get_expiration_date("200001"))
    
    print(kospi_info.get_remaining_days("2016/02/22","201603"))
    print(kospi_info.get_remaining_days("2016/02/22","202203"))
    
    
        
    print(kospi_info.get90dayHistorcalVol("2016/02/23"))
    
#    for index in range(3000,3200):
#        ex_date, remain_day, expire_kospi = kospi_info.get_expiration_info(index)
#        #print(ex_date, remain_day, expire_kospi)
#        hv = kospi_info.get90dayHistorcalVol(index)
#        #print(hv)
#        curr_kospi_200 = df["현재지수"][index]
#        up,low = kospi_info.currentTargetOptBand(curr_kospi_200,hv, remain_day)
#        print("날짜",df["일자"][index], "현재지수", curr_kospi_200, "up",up,"low", low, "잔여일", remain_day, "HV", hv, "만기", ex_date)
        
    
    
        
    