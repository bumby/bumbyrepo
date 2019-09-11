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
   
    _instance = None
    
    def __init__(self):
        if self._instance is not None:
            raise ValueError("An instance already exists")
        print("optmon has created")
        self.count = 0
            
        self.con = sqlite3.connect("D:\work\Y2018\option\kospi.db")
        
                
#------------------------------observer implementaion ---------------        
    def update(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
        self.호가시간=호가시간_
        self.단축코드=단축코드_
        self.매도호가1=매도호가1_
        self.매수호가1=매수호가1_
    
        
        self.display()

    def register_subject(self, subject):
        self.subject = subject
        self.subject.register_observer(self)

    def display(self):
        print ('호가시간:',self.호가시간, '단축코드:',self.단축코드 ,' 매도호가1:',self.매도호가1, ' 매수호가1:',self.매수호가1)
#----------------------------------------------------------     
       
    def start(self,  Option_expiration_mon):
        """
        db에서 data  load
        """
     
      
        #data 호가 분류 
        
        # 가상 데이터 생성 시간 구성
        
        # 데이터 생성 
        
        # 데이터 전송 
        

    
        hhtot = ["09","10","11","12","13","14"]
        mmtot = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19", "20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39", "40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59"];
        sstot = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19", "20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39", "40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59"];
    
#        self.count = self.count + 1
#        sstot_index = int(self.count%60)
#        mmtot_index = int(((self.count/60)%60)+1)
#        hhtot_index = int((self.count/3600)+1)
#        print(hhtot_index)
#        
#        store = "call190712"+hhtot[hhtot_index]+mmtot[mmtot_index]+sstot[sstot_index] 
#        print(store)
#        try: 
#            df = pd.read_sql("SELECT * from "+store, self.con, index_col = "index")
#            #ATMS, deal_signal, sell_code, sell_price, buy_code, buy_price = dbanal.extract_call_gap(df1, 12.8, ATMS) 
#            
#            offerho1 = df['offerho1']
#            bidho1   = df['bidho1']
#            optcode  = df['optcode']
#
#            for i in range(0,offerho1.size-1):
#                print(hh+mm+ss)
#                self.subject.change_optprice(hh+mm+ss,optcode[i], offerho1[i], bidho1[i])
#          
#
#
#        except Exception:
#                # Catching this exception works fine if, for example,
#                # I enter the wrong username and password
#            pass
        
    
        for hh in hhtot:
            for mm in mmtot:
                for ss in sstot:
                    store = "call190712"+hh+mm+ss
                    #print(store)
                    #df1 = pd.read_sql("SELECT * from "+store, con, index_col = "index")
                    #print(df1)
                    #df1 = pd.read_sql("SELECT * from call190624090001", con, index_col = "index")
                   
                    try:
                        df = pd.read_sql("SELECT * from "+store, self.con, index_col = "index")
                        #ATMS, deal_signal, sell_code, sell_price, buy_code, buy_price = dbanal.extract_call_gap(df1, 12.8, ATMS) 
                        
                        offerho1 = df['offerho1']
                        bidho1   = df['bidho1']
                        optcode  = df['optcode']
        
                        for i in range(0,offerho1.size-1):
                            self.subject.change_optprice(hh+mm+ss,optcode[i], offerho1[i], bidho1[i])
  
        
                    except Exception:
                            # Catching this exception works fine if, for example,
                            # I enter the wrong username and password
                        pass
                        #print("\nNo such table")
  
    

    
  
    
  #  @classmethod
  #  def get_Instance(cls):
  #      return cls.__instance




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
        #opthogamon observer 등록
    optmon.register_subject(optdata)
    optmon.start("201909")

