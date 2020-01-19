# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 13:42:52 2019

@author: USER
"""
import win32com.client
import pythoncom
import math
import pandas as pd


from subject import *
from observer import *



class XAQueryEventHandlerT2101:
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEventHandlerT2101.query_state = 1           
              

       
       
            
class PyOptCurrentPriceMon(Observer):
    def __init__(self):
        self.count = 0


#------------------------------observer implementaion ---------------        
    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_, 이론가_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        pass
    
    def register_subject(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def display(self):
        pass
#----------------------------------------------------------   
        
    
    def getCurrOptPrice(self, optcode):
                    
        instXAQueryT2101 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerT2101)
        instXAQueryT2101.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t2101.res"
        instXAQueryT2101.SetFieldData("t2101InBlock","focode",0,optcode) #"201908" 형테
        instXAQueryT2101.Request(0)
        
        while XAQueryEventHandlerT2101.query_state == 0:
            pythoncom.PumpWaitingMessages()
        XAQueryEventHandlerT2101.query_state = 0
        
        histimpv = instXAQueryT2101.GetFieldData("t2101OutBlock", "histimpv",0)            #역사적 변동성
        print("역사적 변동성 ",histimpv)
        return histimpv
        
        
    def getHistImpv(self, optstrike_, expiredate_):
        code = self.optcode_gen(optstrike_, expiredate_, "call")
        return self.getCurrOptPrice(code)
        
    def updateHistImpv(self, expiredate_):
        kospi200index = self.subject.get_optEnvStatus("kospi200Index")
        print(kospi200index)
        HV = self.getHistImpv(pd.to_numeric(kospi200index), expiredate_)
        if HV == 0:
            print("HV acquisition failed")
            exit()
        self.subject.change_envStatus("HV",HV)
     
        
    
        
    def optcode_gen(self, optstrike, expirationdate, putncall):

        #put and sell code and kospi200
        if putncall == "call" :
            opt_putncall_code = "201"
            price_divide = int(math.floor(optstrike/2.5))
            opt_index = int((price_divide+1)*2.5)
            opt_index_str = str(opt_index)
            #print(opt_index_str)
        elif putncall == "put" :
            opt_putncall_code = "301"
            price_divide = int(math.floor(optstrike/2.5))
            opt_index = int((price_divide)*2.5)
            opt_index_str = str(opt_index)
           # print(opt_index_str)
        else :
            print("no such code")
            raise Exception('no such code')  


        #target expiration year
        expiration_year = expirationdate[0:4]
        if  expiration_year=="2019" :
            expiration_year_code = "P"
        elif expiration_year=="2020" :
            expiration_year_code = "Q"
        elif expiration_year=="2021" :
            expiration_year_code = "R"
        elif expiration_year=="2022" :
            expiration_year_code = "S"
        elif expiration_year=="2023" :
            expiration_year_code = "T"
        elif expiration_year=="2024" :
            expiration_year_code = "V"
        elif expiration_year=="2025" :
            expiration_year_code = "W"    
        else :
            print("option code is available only for 2025")
            raise Exception("option code is available only for 2025")

        #target expiration month
        expiration_month  = expirationdate[4:6]
        if  expiration_month=="01" :
            expiration_month_code = "1"
        elif expiration_month=="02" :
            expiration_month_code = "2"
        elif expiration_month=="03" :
            expiration_month_code = "3"
        elif expiration_month=="04" :
            expiration_month_code = "4"
        elif expiration_month=="05" :
            expiration_month_code = "5"
        elif expiration_month=="06" :
            expiration_month_code = "6"
        elif expiration_month=="07" :
            expiration_month_code = "7"    
        elif expiration_month=="08" :
            expiration_month_code = "8"
        elif expiration_month=="09" :
            expiration_month_code = "9"
        elif expiration_month=="10" :
            expiration_month_code = "A"
        elif expiration_month=="11" :
            expiration_month_code = "B" 
        elif expiration_month=="12" :
            expiration_month_code = "C"
        else :
            print("choose only for 1~12")
            raise Exception("choose only for 1~12")

        optcode = opt_putncall_code + expiration_year_code+ expiration_month_code + opt_index_str
        #print(optcode)
        return optcode


    def start(self,  Option_expiration_mon):
        """
        이베스트 서버에 실시간 data 요청함.
        """
        self.updateHistImpv(Option_expiration_mon)
            
#unit test code 
        
from bestConnect import *
import pandas as pd

if __name__ == "__main__":
   # app = QApplication(sys.argv)
    
    secinfo = secInfo()                        #계좌 정보 holder
    best = BestAccess()                        #Login class 생성
    accounts_list = best.comm_connect(secinfo) #Login 

    pyoptcurrentpricemon = PyOptCurrentPriceMon()
    pyoptcurrentpricemon.getHistImpv(pd.to_numeric(280), "202002")
    
   # while pyoptcurrentpricemon.count < 500:
   #     pythoncom.PumpWaitingMessages()
