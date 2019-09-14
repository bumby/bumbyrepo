# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 21:57:09 2019

@author: USER
"""
from pandas import DataFrame
import sqlite3

from subject import *
from observer import *
import time
from time import sleep


class PyOptHogaMonSimul(Observer):
    """
    this class generates the simulation data from Hoga Event
    Real Event cannot be used in off the market time.
    Using this class developper can develop the SW anytime 
    """
    _instance = None
    
    def __init__(self):
        if self._instance is not None:
            raise ValueError("An instance already exists")
        print("optmon has created")
        self.count = 0
            
        self.con = sqlite3.connect("kospisample.db")
        self.sample = {}
        self.dataload()
        
        
                
    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        """
        observer implementaion
        """
        print(호가시간_, 단축코드_, 매도호가1_, 매수호가1_)

    
   
    def register_subject(self, subject):
        """
        observer implementaion
        """
        self.subject = subject
        self.subject.register_observer(self)


    def start(self,  Option_expiration_mon):
        """
        db에서 data  load
        """
        for i in self.sample:
            self.subject.change_optprice(self.sample[i]["time"], self.sample[i]["time"], self.sample[i]["time"], self.sample[i]["time"])
            sleep(1)
  
    def dataload(self):
        

    
    #    hhtot = ["09","10","11","12","13","14"]
    #    mmtot = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19", "20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39", "40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59"];
          
    #    hhtot = ["09"]    
    #    mmtot = ["24","25"]
    #    sstot = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19", "20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39", "40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59"];
    
        store_index = ["option190910224214","option190910224455","option190910225052","option190910230617"]    
        
      
        for store in store_index:
          
                   
            self.sample[store]={}
            try:
                df = pd.read_sql("SELECT * from "+store, self.con, index_col = "index")
                #ATMS, deal_signal, sell_code, sell_price, buy_code, buy_price = dbanal.extract_call_gap(df1, 12.8, ATMS) 
                self.sample[store]["time"] = store
                self.sample[store]["offerho1"] =df['offerho1']
                self.sample[store]["bidho1"]   =df['bidho1']
                self.sample[store]["optcode"]  = df['optcode']
                

  #              for i in range(0,offerho1.size-1):
 #                   self.subject.change_optprice(hh+mm+ss,optcode[i], offerho1[i], bidho1[i])
  

            except Exception:
                    # Catching this exception works fine if, for example,
                    # I enter the wrong username and password
                pass
                #print("\nNo such table")

    def getSampleSize(self):
        return len(self.sample)
 
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PyOptHogaMonSimul()
        return cls._instance

  
    
   #unit test code    
if __name__ == "__main__":
   # app = QApplication(sys.argv)
   
    optdata =  OptData() #ㅐ
    optmon = PyOptHogaMonSimul().get_instance()
    print(optmon.getSampleSize())
        #opthogamon observer 등록
    optmon.register_subject(optdata)
    optmon.start("201909")

