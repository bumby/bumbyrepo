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
  
        #현재 kospi정보 
       # self.envStatus = {"kospi200Index":"0", "HV":"0", "옵션잔존일":"0"}        
       #수정  
        self.envStatus = {"kospi200Index":"0", "HV":"0", "옵션잔존일":"0", "콜대표IV":"0", "풋대표IV":"0"}        
        
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


  

    def notify_observers(self): 
        """
        notyfy observer about the change event 
        """
        
        #호가시간_, 단축코드_, 매도호가1_, 매수호가1_, 이론가 
              
        for observer in self._observer_list:
            observer.update(self.optChart[self.currentCode]["hogaTime"], self.currentCode, self.optChart[self.currentCode]["offerho1"], self.optChart[self.currentCode]["bidho1"], self.optChart[self.currentCode]["theoryPrice"]) 
             

    def optChanged(self):
        self.notify_observers()

    
    def change_envStatus(self,key,value):
        self.envStatus[key] = value 
        #self.optChanged()
        
        
    def change_hogaprice(self, hogaTime_, m_optCode_, offerho1_, bidho1_, offerho2_, bidho2_, theoryprice_ ):
       
        print("002 option change 스프레드 반영")
        
        self.currentCode = m_optCode_ 
        
        opt = {}
        if m_optCode_ in self.optChart: 
            opt = self.optChart[m_optCode_]             
        else: #새로받은 옵션 정보가 기존에 없는 옵션이면 현재 option에서는 이론가와  IV 항을 가지고 있지 않으므로 강제적으로 할당
            opt["theoryPrice"] = ""
            opt["Iv"] = ""
            
            
        opt["hogaTime"] = hogaTime_
        opt["offerho1"] = offerho1_
        opt["bidho1"] = bidho1_
        opt["offerho2"] = offerho2_
        opt["bidho2"] = bidho2_


        if theoryprice_ != "":
            opt["theoryPrice"] = theoryprice_

        self.optChart[m_optCode_] = opt
        self.optChanged()  

    
    # 외부에서 옵션 가격이 변화했을 경우 
    def change_optprice(self, hogaTime_, m_optCode_, offerho1_, bidho1_, theoryprice_ ):
        """
        From hoga RC change_optprice changes the optchart which include hogaTime_, offerprice bid price
        changed kospi price, IV also can added new data
        """
        print("002 option change 스프레드 반영")
        
        self.currentCode = m_optCode_ 
        
        opt = {}
        if m_optCode_ in self.optChart: 
            opt = self.optChart[m_optCode_]             
        else: #새로받은 옵션 정보가 기존에 없는 옵션이면 현재 option에서는 이론가와  IV 항을 가지고 있지 않으므로 강제적으로 할당
            opt["theoryPrice"] = ""
            opt["Iv"] = ""
            
     
        
        opt["hogaTime"] = hogaTime_
        opt["offerho1"] = offerho1_
        opt["bidho1"] = bidho1_

        if theoryprice_ != "":
            opt["theoryPrice"] = theoryprice_

        self.optChart[m_optCode_] = opt
        self.optChanged()
        
  

    def clear_optchart(self):
        self.optChart = {}
    
    def get_optChart(self):
        return self.optChart

    def get_optEnvStatus(self, key):
        return self.envStatus[key]
    
    def print_opt(self):
        print(self.optChart) 