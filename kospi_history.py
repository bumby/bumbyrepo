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
        return self.HV
    
    
    
        
    
    

class KOSPIHISTORYINFO:
    def __init__(self):
        
       
        self.data = pd.read_csv("kospi200_added_To_2022.csv",sep=",")
        #self.data = pd.read_csv("kospi200.csv",sep=",")
        self.data.head()
        self.df = self.data[["일자","현재지수"]]
        
        print("df",self.df)
     
        self.opt_expire_dict = { "200601":"2006/01/12","200602":"2006/02/09","200603":"2006/03/09","200604":"2006/04/13","200605":"2006/05/11","200606":"2006/06/08","200607":"2006/07/13","200608":"2006/08/10","200609":"2006/09/14","200610":"2006/10/12","200611":"2006/11/09","200612":"2006/12/14"\
                                ,"200701":"2007/01/11","200702":"2007/02/08","200703":"2007/03/08","200704":"2007/04/12","200705":"2007/05/10","200706":"2007/06/14","200707":"2007/07/12","200708":"2007/08/09","200709":"2007/09/13","200710":"2007/10/11","200711":"2007/11/08","200712":"2007/12/13"\
                                ,"200801":"2008/01/10","200802":"2008/02/14","200803":"2008/03/13","200804":"2008/04/10","200805":"2008/05/08","200806":"2008/06/12","200807":"2008/07/10","200808":"2008/08/14","200809":"2008/09/11","200810":"2008/10/09","200811":"2008/11/13","200812":"2008/12/11"\
                                ,"200901":"2009/01/08","200902":"2009/02/12","200903":"2009/03/12","200904":"2009/04/09","200905":"2009/05/14","200906":"2009/06/11","200907":"2009/07/09","200908":"2009/08/13","200909":"2009/09/10","200910":"2009/10/08","200911":"2009/11/12","200912":"2009/12/10"\
                                ,"201001":"2010/01/14","201002":"2010/02/11","201003":"2010/03/11","201004":"2010/04/08","201005":"2010/05/13","201006":"2010/06/10","201007":"2010/07/08","201008":"2010/08/12","201009":"2010/09/09","201010":"2010/10/14","201011":"2010/11/11","201012":"2010/12/09"\
                                ,"201101":"2011/01/13","201102":"2011/02/10","201103":"2011/03/10","201104":"2011/04/14","201105":"2011/05/12","201106":"2011/06/09","201107":"2011/07/14","201108":"2011/08/11","201109":"2011/09/08","201110":"2011/10/13","201111":"2011/11/10","201112":"2011/12/08"\
                                ,"201201":"2012/01/12","201202":"2012/02/09","201203":"2012/03/08","201204":"2012/04/12","201205":"2012/05/10","201206":"2012/06/14","201207":"2012/07/12","201208":"2012/08/09","201209":"2012/09/13","201210":"2012/10/11","201211":"2012/11/08","201212":"2012/12/13"\
                                ,"201301":"2013/01/10","201302":"2013/02/14","201303":"2013/03/14","201304":"2013/04/11","201305":"2013/05/09","201306":"2013/06/13","201307":"2013/07/11","201308":"2013/08/08","201309":"2013/09/12","201310":"2013/10/10","201311":"2013/11/14","201312":"2013/12/12"\
                                ,"201401":"2014/01/09","201402":"2014/02/13","201403":"2014/03/13","201404":"2014/04/10","201405":"2014/05/08","201406":"2014/06/12","201407":"2014/07/10","201408":"2014/08/14","201409":"2014/09/11","201410":"2014/10/08","201411":"2014/11/13","201412":"2014/12/11"\
                                ,"201501":"2015/01/08","201502":"2015/02/12","201503":"2015/03/12","201504":"2015/04/09","201505":"2015/05/14","201506":"2015/06/11","201507":"2015/07/09","201508":"2015/08/13","201509":"2015/09/10","201510":"2015/10/08","201511":"2015/11/12","201512":"2015/12/10"\
                                ,"201601":"2016/01/14","201602":"2016/02/11","201603":"2016/03/10","201604":"2016/04/14","201605":"2016/05/12","201606":"2016/06/09","201607":"2016/07/14","201608":"2016/08/11","201609":"2016/09/08","201610":"2016/10/13","201611":"2016/11/10","201612":"2016/12/08"\
                                ,"201701":"2017/01/12","201702":"2017/02/09","201703":"2017/03/09","201704":"2017/04/13","201705":"2017/05/11","201706":"2017/06/08","201707":"2017/07/13","201708":"2017/08/10","201709":"2017/09/14","201710":"2017/10/12","201711":"2017/11/09","201712":"2017/12/14"\
                                ,"201801":"2018/01/11","201802":"2018/02/08","201803":"2018/03/08","201804":"2018/04/12","201805":"2018/05/10","201806":"2018/06/14","201807":"2018/07/12","201808":"2018/08/09","201809":"2018/09/13","201810":"2018/10/11","201811":"2018/11/08","201812":"2018/12/13"\
                                ,"201901":"2019/01/10","201902":"2019/02/14","201903":"2019/03/14","201904":"2019/04/11","201905":"2019/05/09","201906":"2019/06/13","201907":"2019/07/11","201908":"2019/08/08","201909":"2019/09/11","201910":"2019/10/10","201911":"2019/11/14","201912":"2019/12/12"\
                                ,"202001":"2020/01/09","202002":"2020/02/13","202003":"2020/03/12","202004":"2020/04/09","202005":"2020/05/14","202006":"2020/06/11","202007":"2020/07/09","202008":"2020/08/13","202009":"2020/09/10","202010":"2020/10/08","202011":"2020/11/12","202012":"2020/12/10"\
                                ,"202101":"2021/01/14","202102":"2021/02/10","202103":"2021/03/11","202104":"2021/04/08","202105":"2021/05/13","202106":"2021/06/10","202107":"2021/07/08","202108":"2021/08/12","202109":"2021/09/09","202110":"2021/10/14","202111":"2021/11/11","202112":"2021/12/09"\
                                ,"202201":"2022/01/13","202202":"2022/02/10","202203":"2022/03/10","202204":"2022/04/14","202205":"2022/05/12","202206":"2022/06/09","202207":"2022/07/14","202208":"2022/08/11","202209":"2022/09/08","202210":"2022/10/13","202211":"2022/11/10","202212":"2022/12/08"}
        
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
    

    def get_expiration_value(self, expiration_year_month):
        """
        Returns the expiration date for given "year+month" information
        
        Args:
            expiration_year_month : "year+month" 
        
        Returns:
            expiration_value : "kospi value at expiration day"
    
        bound [201301 ~ 201812]
        
        ex) 
            get_expiration_date("201602")
            226.7
            
            get_expiration_date("200001")
            "There is no information for argument year month"            

        """
        try:
            expiration_year_month_day = self.opt_expire_dict[expiration_year_month] 
            f1 = self.df[self.df['일자']==expiration_year_month_day]
            return f1.iloc[0,1]
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
            
            print("f1", f1, "f2", f2, "remaining_days", remaining_days  )
            
            if remaining_days < 0 :
                print("Excel Date format should be yyyy/mm/dd","error at get_remaining_days!!! ", "remaining day=", remaining_days, " current_year_month_date", current_year_month_date, "expiration_year_month",expiration_year_month )
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
  

        
    
    def get30dayHistorcalVol(self, curr_year_month_date):
        """
        Returns 30days Historcal Volatility from year/monthfor/date 
        
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
        
        
        if(curr_date_index < 30):  #한달의 약 
            print("data is less than 90days0!!!")
            exit()
        
        i = curr_date_index - 30
        self.stack_30day = []
        while i<curr_date_index:
            i=i+1
            self.stack_30day.append(self.df["현재지수"][i])
        #print(self.stack_90day)
        return self.histvol.getHV(self.stack_30day)
  

  
      
#    def currentTargetOptBand(self, current_kospi_200, current_HV, remained_day):
#        kospi200price = pd.to_numeric(current_kospi_200)
#        
#        jandatecnt = remained_day
#        HV = current_HV
#        #jandatecnt = pd.to_numeric(remained_day)
#        #HV =  pd.to_numeric(current_HV) #1.2 는 증폭 ratio이다. 
#        #self.HV = 13.46 #전광판엑서 제공한함 다른 방법 필요
#        
#        target_sigma = 0.8 # 기준 1.3 은 90% 승률       
#        sigma = HV/100.0*math.sqrt(jandatecnt/252.0)
#        upperTarget = math.exp(math.log(kospi200price)+sigma*target_sigma) #1.3은 normal distribution 90% 범위
#        lowerTarget = math.exp(math.log(kospi200price)-sigma*target_sigma) #1.3은 normal distribution 90% 범위     
#        return upperTarget, lowerTarget      
    
    def currentTargetOptBand(self, current_kospi_200, current_HV, remained_day, per_rate): #0.84 80% 1.03 85%  1.29 90%
        kospi200price = pd.to_numeric(current_kospi_200)
        jandatecnt = pd.to_numeric(remained_day)
        HV = pd.to_numeric(current_HV)
        #jandatecnt = pd.to_numeric(remained_day)
        #HV =  pd.to_numeric(current_HV) #1.2 는 증폭 ratio이다. 
        #self.HV = 13.46 #전광판엑서 제공한함 다른 방법 필요
        
        #new approach
        r = 0.01
        sigma = HV/100.0
        #T = jandatecnt/365.0
        T = jandatecnt/252.0
        #per_rate = 1.03  #1.03 85%  1.29 90%
        #per_rate = 1.03  #1.03 85%  1.29 90%
        #per_rate = 0.84  #0.84 80% 1.03 85%  1.29 90%
        
        z_high = math.log(kospi200price)+(r-sigma*sigma/2.0)*T+per_rate*sigma*math.sqrt(T)
        upperTarget = math.exp(z_high)
        z_low = math.log(kospi200price)+(r-sigma*sigma/2.0)*T-per_rate*sigma*math.sqrt(T)
        lowerTarget = math.exp(z_low)
        return upperTarget, lowerTarget 

if __name__ == '__main__':
    
    kospi_info = KOSPIHISTORYINFO()
    
    print(kospi_info.get_expiration_date("201602"))
    print(kospi_info.get_expiration_date("200001"))
    
    print(kospi_info.get_remaining_days("2016/02/22","201603"))
    print(kospi_info.get_remaining_days("2016/02/22","202203"))
    
    
        
    print(kospi_info.get90dayHistorcalVol("2016/02/23"))
    
    print(kospi_info.get_expiration_value("201602"))
    
#    for index in range(3000,3200):
#        ex_date, remain_day, expire_kospi = kospi_info.get_expiration_info(index)
#        #print(ex_date, remain_day, expire_kospi)
#        hv = kospi_info.get90dayHistorcalVol(index)
#        #print(hv)
#        curr_kospi_200 = df["현재지수"][index]
#        up,low = kospi_info.currentTargetOptBand(curr_kospi_200,hv, remain_day)
#        print("날짜",df["일자"][index], "현재지수", curr_kospi_200, "up",up,"low", low, "잔여일", remain_day, "HV", hv, "만기", ex_date)
       