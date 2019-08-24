# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 23:37:49 2019

@author: USER
"""

from abc import  abstractmethod



class Observer:


    @abstractmethod

    def update(self):

        pass


    @abstractmethod

    def register_subject(self, subject):

        pass

#class Emotion(Observer):
#
#    def update(self, happiness,sadness): #업데이트 메서드가 실행되면 변화된 감정내용을 화면에 출력해줍니다
#
#        self.happiness=happiness
#
#        self.sadness=sadness
#
#        self.display()
#
#
#    def display(self):
#
#        print ('weejiwon Emotion happiness:',self.happiness,' sadness:',self.sadness)
#
#
