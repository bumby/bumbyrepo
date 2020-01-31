# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 09:53:56 2020

@author: USER
"""



from abc import ABCMeta, abstractmethod


class OptStatusMonitor:
    
    __metaclass__=ABCMeta
    
  
    @abstractmethod
    
    def start(self):
    
        pass
    
 
    
    @abstractmethod

    def register_subject(self, subject):

        pass
        
    