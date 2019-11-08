# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 20:56:43 2019

@author: USER
"""
from HTrader import *
from ControllerInterface import *
from subject import *


from accessDB import *
from PyOptHogaMon import *
from PyOptChegyolMon import *
#from PyOptHogaMonSimul import *

import time

class OptScanContoller(ControllerInterface):
    
    
    def __init__(self, optdata):
        super(OptScanContoller,self).__init__()
                #subject 생성

        
        
         #option monitor 생성 및 등록                
        self.Option_expiration_mon = "201912"
                
        #simulation
        #self.optmon = PyOptHogaMonSimul.get_instance()
        #real data
        self.optmon = PyOptHogaMon.get_instance()
        
        #opthogamon observer 등록
        self.optmon.register_subject(optdata)
         
              
        
        # db 생성 및 observer 등록
        self.access_db = accessDB()
        self.access_db.register_subject(optdata)     
        
        
              
        
        
        #체결 생성 등록
        self.chekyolmon  = PyOptChegyolMon.get_instance()
        self.chekyolmon.register_subject(optdata)
         
       
    def Start(self):
        print('start has been pushed')  
        self.optmon.start(self.Option_expiration_mon)  
        time.sleep(1)
        self.chekyolmon.start(self.Option_expiration_mon)
        

    
    def End(self):
    
        pass
    
    
    
        
    def AutoTradeOn(self):
        
        pass
    
    
    
    
    def AutoTradeOff(self):
    
        pass