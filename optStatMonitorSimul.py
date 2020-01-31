# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 13:08:52 2020

@author: USER
"""
import threading
from OptStatusMonitor import *
from subject import *
from kospi_history import *
from timeManager import *
from OptCodeTool import *

from optPurse import *

class optStatMonitorSimul(OptStatusMonitor):
    def __init__(self):
        super(optStatMonitorSimul, self).__init__()

        #option monitor 생성 및 등록   
        self.count = 0
        self.dataload()
        self.tmanager = timeManager()
        self.kospi_info = KOSPIHISTORYINFO()
        self.optcodetool = OptCodeTool()
        
       

    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_, 이론가_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        pass
 
    
    def dataload(self):
        data = pd.read_csv("kospi200data_2012_.csv",sep=",")
        #data = pd.read_csv("kospi200data.csv",sep=",")
        data.head()
        self.df = data[["일자","현재지수"]] 
        
        
        
        
        
    def OnReceiveRealData(self): # event handler
        """
        이베스트 서버에서 ReceiveRealData 이벤트 받으면 실행되는 event handler
        """

        self.count += 1     
     
            
        cur_kospi_price = pd.to_numeric(self.df["현재지수"][self.count])
        k = self.df["일자"][self.count]
        curr_year = k[0:4]
        curr_month = k[5:7]
        curr_day = k[8:10]
        currday_dash = curr_year+'/'+curr_month+'/'+curr_day
        expire_month = self.tmanager.getNextYearMonth(pd.to_numeric(curr_year),pd.to_numeric(curr_month))
        
        
        mintick = int(cur_kospi_price-50.0)
        maxtick = int(cur_kospi_price+50.0)
        
        
        #옵션 환경 정보 공유
        #잔여일 계산
        remaining_days = self.kospi_info.get_remaining_days(currday_dash,expire_month)
        #HV 계산
        HV = self.kospi_info.get90dayHistorcalVol(currday_dash)
        
        
        self.subject.change_envStatus("kospi200Index",self.df["현재지수"][self.count])
        self.subject.change_envStatus("HV",HV)
        self.subject.change_envStatus("옵션잔존일",remaining_days)

        
        forprinting_opt_call_index = []
        forprinting_opt_call_code = []
        forprinting_opt_call_price = []
        
        forprinting_opt_put_index = []
        forprinting_opt_put_code = []
        forprinting_opt_put_price = []
        
        index_range = np.arange(mintick, maxtick, 2.5) #2.5 간격으로 옵션 인덱스 범위 지정
        
        
                  
        
        if curr_year in ["2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018"]  :
            for i in index_range:
                opt_code = self.optcodetool.optcode_gen(i,expire_month,'call')
                
                try:
                    calloptdata = pd.read_csv("./data/K"+opt_code+".csv",sep=",")
                    matchingdayindex = (calloptdata[calloptdata['일자'] == currday_dash])
                    
                    호가시간 = k
                    매도호가1 = matchingdayindex.iloc[0]['시가']
                    매수호가1 = matchingdayindex.iloc[0]['시가']
                    단축코드 = opt_code
                    이론가 = "11"   
        
                    self.subject.change_optprice(호가시간,단축코드, 매도호가1,매수호가1,이론가) 
                    
                    forprinting_opt_call_index.append(i)
                    forprinting_opt_call_code.append(opt_code)
                    forprinting_opt_call_price.append(매도호가1)               

                except:
                    #print("safe call option has not been solved" )
                    pass
                

                
                opt_code = self.optcodetool.optcode_gen(i,expire_month,'put')
                try:
                    putoptdata = pd.read_csv("./data/K"+opt_code+".csv",sep=",")
                    matchingdayindex = (putoptdata[putoptdata['일자'] == currday_dash])
                    
                    호가시간 = k
                    매도호가1 = matchingdayindex.iloc[0]['시가']
                    매수호가1 = matchingdayindex.iloc[0]['시가']
                    단축코드 = opt_code
                    이론가 = "11"   
    
                    self.subject.change_optprice(호가시간,단축코드, 매도호가1,매수호가1,이론가)
                    
                    forprinting_opt_put_index.append(i)
                    forprinting_opt_put_code.append(opt_code)
                    forprinting_opt_put_price.append(매도호가1)               
    
                except:
                    #print("safe call option has not been solved" )
                    pass
                
        
        
    
        
        print("call" ,forprinting_opt_call_price)
        print("put",forprinting_opt_put_price)
        
        
        #만기일 지나가면 optchart에서 모두 제거
        current_year_month = curr_year+curr_month
        
        if self.kospi_info.get_expiration_date(current_year_month) == currday_dash:
            self.subject.clear_optchart() #챠트에서 기존
                
        threading.Timer(0.1,self.OnReceiveRealData).start()
        return True
        
    




    
    
    def start(self,optdata):
        
        self.register_subject(optdata)
        
        self.OnReceiveRealData()
        
    def register_subject(self, subject):
        self.subject = subject
        self.subject.register_observer(self)
        
        
        
#unit test code    
if __name__ == "__main__":
    
       
    optmon = optStatMonitorSimul()
    
    optdata = OptData()
    optmon.start(optdata)