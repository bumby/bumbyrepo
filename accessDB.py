# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 22:54:43 2019

@author: USER
"""

import pandas as pd
import sqlite3
import datetime

from subject import *
from observer import *

class accessDB(Observer):
    def __init__(self,):
        super().__init__()
        #subject 생성
        self.count = 0
        self.con = sqlite3.connect("D:\work\Y2019\optdata\kospi.db")
        
        dt = datetime.datetime.now().strftime("%y%m%d%H%M%S")
        self.opt_hoga_table_name = "option"+dt
        
#------------------------------observer implementaion ---------------        
      
    def update(self, hogaTime_, optCode_, offerho1_, bidho1_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        self.optCode=optCode_
        self.hogaTime=hogaTime_
        self.offerho1=offerho1_
        self.bidho1=bidho1_

        
        self.display()
     #   self.saveToDB()

    def register_subject(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def display(self):
        print ('DB updated')


#----------------------------------------------------------     
    def saveToDB(self):
       
        ohlcv = {'hogatime':[], 'optcode':[], 'offerho1':[], 'bidho1':[]}
        ohlcv['hogatime'].append(self.hogaTime)
        ohlcv['optcode'].append(self.optCode)
        ohlcv['offerho1'].append(self.offerho1)
        ohlcv['bidho1'].append(self.bidho1)
    
      
        opt_hoga_change = pd.DataFrame(ohlcv, columns = ['optcode','offerho1','bidho1'], index=ohlcv['hogatime'])
        
        opt_hoga_change.to_sql(self.opt_hoga_table_name, self.con, if_exists='append') #speedup required
 