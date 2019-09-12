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
        #optchart[단축코드] = [0:호가시간, 1:매도호가1, 2:매수호가1, 3:현재가, 4:이론가, 5:내재변동성]
        
        self.optChart = {}
        
              
        #현재 호가 정보 
        self.단축코드 = ""
        self.매도호가1 = 0
        self.매수호가1 = 0
        self.이론가 = 0

        #현재 kospi정보 
        self.호가시간 = 0
        self.kospi200지수 = 0
        self.역사적변동성 = 0       
                
   
        
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
            observer.update( self.호가시간, self.단축코드, self.매도호가1, self.매수호가1)

   
    def optChanged(self):
        self.notify_observers() #감정이 변하면 옵저버에게 알립니다.

    
    def change_optprice(self, 호가시간_, 단축코드_, 매도호가1_, 매수호가1_ ):
        self.호가시간=호가시간_
        self.단축코드=단축코드_
        self.매도호가1=매도호가1_
        self.매수호가1=매수호가1_
      
         
#        found = False
#        for n,s in enumerate(self.optChart):
#            if 단축코드_ in s:
#                self.optChart[n] = [단축코드_, 매도호가1_, 매수호가1_ ]
#                found = True
#        if found == False:
#            self.optChart.append([단축코드_, 매도호가1_, 매수호가1_])
#        
        opt = {}
        opt["호가시간"] = 호가시간_
    #    opt["단축코드"] = 단축코드_
        opt["매도호가1"]= 매도호가1_
        opt["매수호가1"]= 매수호가1_
        
        self.optChart[단축코드_] = opt
        
        self.optChanged()

    def change_base(self, 호가시간_, kospi200지수_, 이론가_, 단축코드_, 내재변동성_, 매도호가1_, 매수호가1_ ):
        self.kospi200지수=kospi200지수_
        self.내재변동성=내재변동성_

        self.호가시간=호가시간_
        self.단축코드=단축코드_
        self.매도호가1=매도호가1_
        self.매수호가1=매수호가1_
        self.이론가=이론가_
        
        found = False
        for n,s in enumerate(self.optChart):
            if 단축코드_ in s:
                self.optChart[n] = [단축코드_, 매도호가1_, 매수호가1_ ]
                found = True
        if found == False:
            #self.optChart = [self.optChart,[단축코드_, 매도호가1_, 매수호가1_]] 
            self.optChart.append([단축코드_, 매도호가1_, 매수호가1_])
        self.optChanged()


    def get_optChart(self):
        return self.optChart

    def print_opt(self):
        print(self.optChart) 