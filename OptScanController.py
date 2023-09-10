# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 20:56:43 2019

@author: USER
"""
#from HTrader import *
from ControllerInterface import *
from subject import *


from accessDB import *
from PyOptHogaMon import *
from PyOptChegyolMon import *
from DBanal import *
from timeManager import *
from PyOptCurrentPriceMon import *
from optPurse import *
from OptStatusMonitor import *

from OptStrategy import *

import time

class OptScanContoller(ControllerInterface):
    
    
    def __init__(self, optdata,_monitor_mode, mode):
        super(OptScanContoller,self).__init__()
                #subject 생성
     
        
                #로그인 프로세스
        if mode == "XingAPI":
            self.secinfo = secInfo()
            self.best = BestAccess()
            self.accounts_list = self.best.comm_connect(self.secinfo)
            self.passwd =  self.secinfo.getOrderPasswd()  
        elif mode == "simulation":
            self.passwd = "1234"
        else:
            print("not adequate mode has been selected")
        
        
        #option monitor 생성 및 등록   
        self.timemanager = timeManager()             
        self.Option_expiration_mon = self.timemanager.getTargetMonth()  #만기 달 설정 현재보다 1달 많은 다음달 
  
        
     
        
        
        self.monitor_mode = _monitor_mode
        self.optstatmon = _monitor_mode
        self.optstatmon.register_subject(optdata)


        # db 생성 및 observer 등록
#        self.access_db = accessDB()
#        self.access_db.register_subject(optdata)     
             

        #db analysis 생성 및 observer 등록
        #self.dbanal = DBalalysis(self.Option_expiration_mon, mode)   
        #self.dbanal.register_subject(optdata)
        
        
        #self.strategy = BasicStrategy()
        #self.strategy = StaticStrategy()
        self.strategy = StaticWinningRate()
        self.strategy.register_subject(optdata)
         
       
    def Start(self,optdata):
        print('start has been pushed')  
        
        
#        self.optmon.start(self.Option_expiration_mon)  
#        time.sleep(1)
#        self.chekyolmon.start(self.Option_expiration_mon)
#        time.sleep(1)
#        self.HVmon.start(self.Option_expiration_mon) 
        #self.optstatmon.register_subject(optdata)
        self.optstatmon.start(optdata)

    
    def End(self):
        print("종료")
        self.optstatmon.end()
        
       # self.dbanal.optvis.showDepositHistory()
      #  self.dbanal.optvis.showKospi200History()
   #     self.dbanal.closeDBanal()
        
    def AutoTradeOn(self):
        
        pass
    
      
    
    def AutoTradeOff(self):
    
        pass
    
    
from XingAPIMonitor import *
from OptStatMonitorSimul import *
        
#unit test code    
if __name__ == "__main__":
    
    optdata = OptData()
    optstatmon = optStatMonitorSimul()
    optmon  = OptScanContoller(optdata,optstatmon)
            
    secinfo = secInfo()                        #계좌 정보 holder
    best = BestAccess()                        #Login class 생성
    accounts_list = best.comm_connect(secinfo) #Login
    #optmon  = OptScanContoller(optdata,"XingAPI")
           
    optmon.Start(optdata)
        