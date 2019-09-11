# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 23:17:27 2019

@author: USER
"""
from abc import ABCMeta, abstractmethod

class ControllerInterface:
    
    __metaclass__=ABCMeta
    
  
    @abstractmethod
    
    def Start(self):
    
        pass
        
    
    @abstractmethod
    
    def End(self):
    
        pass
    
    
    
    @abstractmethod
    
    def AutoTradeOn(self):
    
        pass
    
    
    @abstractmethod
    
    def AutoTradeOff(self):
    
        pass