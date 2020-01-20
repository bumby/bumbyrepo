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

import time

class OptScanContoller(ControllerInterface):
    
    
    def __init__(self, optdata,_monitor_mode):
        super(OptScanContoller,self).__init__()
                #subject 생성
     
        
        #option monitor 생성 및 등록   
        self.timemanager = timeManager()             
        self.Option_expiration_mon = self.timemanager.getTargetMonth()  #만기 달 설정 현재보다 1달 많은 다음달 
        #self.Option_expiration_mon = "201912"
                
        #simulation
        #self.optmon = PyOptHogaMonSimul.get_instance()
        #real data
        
        
        
        self.monitor_mode = _monitor_mode
        if self.monitor_mode == "XingAPI":
            print("monitor source comes from XingAPI")
            
            self.optmon = PyOptHogaMon.get_instance()
      
            self.chekyolmon  = PyOptChegyolMon.get_instance()
            #체결 생성 등록
            #순서 중요(체결정보를 통해서 kospi 지수가 업데이트 된 이후에  진행되어야 함)
            self.HVmon = PyOptCurrentPriceMon() # 역사적 변동성 
     
            
        
        elif self.monitor_mode == "simulation":
            print("monitor source comes from simulation")
            
            self.optmon = PyOptHogaMonSimul.get_instance()
            self.chekyolmon  = PyOptChegyolMonSimul.get_instance()
            self.HVmon = PyOptCurrentPriceMonSimul() # 역사적 변동성 
            
        
        else:
            print("monitor mode is not determined")
            exit()
            
        self.optmon.register_subject(optdata)    
        self.chekyolmon.register_subject(optdata)  
        self.HVmon.register_subject(optdata)
        

        # db 생성 및 observer 등록
        self.access_db = accessDB()
        self.access_db.register_subject(optdata)     
             

        #db analysis 생성 및 observer 등록
        self.dbanal = DBalalysis(self.Option_expiration_mon)   
        self.dbanal.register_subject(optdata)
        
         
       
    def Start(self):
        print('start has been pushed')  
        self.optmon.start(self.Option_expiration_mon)  
        time.sleep(1)
        self.chekyolmon.start(self.Option_expiration_mon)
        time.sleep(1)
        self.HVmon.start(self.Option_expiration_mon)       

    
    def End(self):
        print("종료")
        self.dbanal.closeDBanal()
    
        
    def AutoTradeOn(self):
        
        pass
    
      
    
    def AutoTradeOff(self):
    
        pass
    
    


#unit test code    
if __name__ == "__main__":
   # app = QApplication(sys.argv)
    optdata = OptData()
    optmon  = OptScanContoller(optdata,"simulation")
    optmon.Start()
        