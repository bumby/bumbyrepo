# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 23:21:17 2019

@author: USER
"""



from abc import ABCMeta, abstractmethod
import pandas as pd
 

class Subject:
    
    __metaclass__=ABCMeta
    
  
    @abstractmethod
    
    def register_observer(self):
    
        pass
        
    
    @abstractmethod
    
    def remove_observer(self):
    
        pass
    
    
    
    @abstractmethod

    def notify_observers(self):
    
        pass

    



class OptData(Subject):
    def __init__(self):
        super(OptData, self).__init__()
        self._observer_list = []
       
        
        #현재시간 option 전광판 정보
        #optchart는 dictionary
        #optchart[m_optCode] = [0:hogaTime, 1:offerho1, 2:bidho1, 3:현재가, 4:theoryPrice, 5:Iv]
        
        self.optChart = {}
        
              
        #현재 호가 정보 
        self.m_optCode = ""
        self.offerho1 = 0
        self.bidho1 = 0
        self.theoryPrice = 0
        self.Iv = 0

        #현재 kospi정보 
        self.hogaTime = 0
        self.kospi200Index = 0
        self.Hv = 0       
                
   
        
    def register_observer(self, observer):
        if observer in self._observer_list:
            return "Already exist observer!"
        
        self._observer_list.append(observer)
        return "Success register!"

    def remove_observer(self, observer):
        if observer in self._observer_list:
            self._observer_list.remove(observer)
            return "Success remove!"

        return "observer does not exist."

    def notify_observers(self): #옵저버에게 알리는 부분 (옵저버리스트에 있는 모든 옵저버들의 업데이트 메서드 실행)
        for observer in self._observer_list:
            observer.update( self.hogaTime, self.m_optCode, self.offerho1, self.bidho1)

   
    def optChanged(self):
        self.notify_observers() #감정이 변하면 옵저버에게 알립니다.

    
    def change_optprice(self, hogaTime_, m_optCode_, offerho1_, bidho1_ ):
        self.hogaTime=hogaTime_
        self.m_optCode=m_optCode_
        self.offerho1=offerho1_
        self.bidho1=bidho1_
      
         
#        found = False
#        for n,s in enumerate(self.optChart):
#            if m_optCode_ in s:
#                self.optChart[n] = [m_optCode_, offerho1_, bidho1_ ]
#                found = True
#        if found == False:
#            self.optChart.append([m_optCode_, offerho1_, bidho1_])
#        
        opt = {}
        opt["hogaTime"] = hogaTime_
    #    opt["m_optCode"] = m_optCode_
        opt["offerho1"]= offerho1_
        opt["bidho1"]= bidho1_
        
        self.optChart[m_optCode_] = opt
        
        self.optChanged()

    def change_base(self, hogaTime_, kospi200Index_, theoryPrice_, m_optCode_, Iv_, offerho1_, bidho1_ ):
        self.kospi200Index=kospi200Index_
        self.Iv=Iv_

        self.hogaTime=hogaTime_
        self.m_optCode=m_optCode_
        self.offerho1=offerho1_
        self.bidho1=bidho1_
        self.theoryPrice=theoryPrice_
        
        found = False
        for n,s in enumerate(self.optChart):
            if m_optCode_ in s:
                self.optChart[n] = [m_optCode_, offerho1_, bidho1_ ]
                found = True
        if found == False:
            #self.optChart = [self.optChart,[m_optCode_, offerho1_, bidho1_]] 
            self.optChart.append([m_optCode_, offerho1_, bidho1_])
        self.optChanged()


    def get_optChart(self):
        return self.optChart

    def print_opt(self):
        print(self.optChart) 