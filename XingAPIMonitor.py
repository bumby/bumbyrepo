# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 11:37:34 2020

@author: USER
"""
from OptStatusMonitor import *
from subject import *
from timeManager import *

from PyOptHogaMon import *
from PyOptChegyolMon import *
from PyOptCurrentPriceMon import *

from subject import *

class XingAPIMonitor(OptStatusMonitor):
    def __init__(self):
        super(XingAPIMonitor, self).__init__()


         #option monitor 생성 및 등록   
        self.timemanager = timeManager()             
        self.Option_expiration_mon = self.timemanager.getTargetMonth()  #만기 달 설정 현재보다 1달 많은 다음달 
  
        
        
        print("monitor source comes from XingAPI")
            
        self.optmon = PyOptHogaMon.get_instance()
        self.chekyolmon  = PyOptChegyolMon.get_instance()
        self.HVmon = PyOptCurrentPriceMon() # 역사적 변동성 
     
            
     
        
        
    def start(self,optdata):
        
        self.register_subject(optdata)
        
        print('optdata has been pushed')  
        print( self.Option_expiration_mon +' is target expiration')
        
        self.optmon.start(self.Option_expiration_mon)  
        time.sleep(1)
        self.chekyolmon.start(self.Option_expiration_mon)
        time.sleep(1)
        self.HVmon.start(self.Option_expiration_mon)       

        
    def register_subject(self,optdata):
        
        self.optmon.register_subject(optdata)    
        self.chekyolmon.register_subject(optdata)  
        self.HVmon.register_subject(optdata)
        
        
from bestConnect import *
        
        
#unit test code    
if __name__ == "__main__":
    
       
    optmon = XingAPIMonitor()
    
    secinfo = secInfo()                        #계좌 정보 holder
    best = BestAccess()                        #Login class 생성
    accounts_list = best.comm_connect(secinfo) #Login
   
    optdata = OptData()
    optmon.start(optdata)