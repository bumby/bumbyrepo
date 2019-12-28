# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:24:08 2019

@author: USER
"""
from datetime import datetime


class timeManager:
    
    def __init__(self):
        self.now = datetime.now()
            
    def getTodayMonth(self):
        self.now = datetime.now()
        self.currmonth  = str(self.now.year)+str(self.now.month)
        return self.currmonth
        
    def getTargetMonth(self):
        self.now = datetime.now()
        self.nextmonthyear = self.now.year
        self.nextmonth = ((self.now.month)%12)+1
        if self.nextmonth == 1:
            self.nextmonthyear = self.nextmonthyear + 1 
        self.targetmonth = str(self.nextmonthyear)+str(self.nextmonth).zfill(2)
        return self.targetmonth
        
    def getNextYearMonth(self, curr_year,curr_month):
        nextmonthyear = curr_year
        nextmonth = ((curr_month)%12)+1
        if nextmonth == 1:
            nextmonthyear = nextmonthyear + 1 
        targetmonth = str(nextmonthyear)+str(nextmonth).zfill(2)
        return targetmonth    
    
    def getPrevYearMonth(self, curr_year,curr_month):
        prevmonthyear = curr_year
        prevmonth = (curr_month-1)%12
        if prevmonth == 0:
            prevmonth = 12
            prevmonthyear = prevmonthyear - 1 
        targetmonth = str(prevmonthyear)+str(prevmonth).zfill(2)
        return targetmonth    
        

if __name__ == "__main__":
   # app = QApplication(sys.argv)
   
    timemanager =  timeManager() #ㅐ
    print(timemanager.getTargetMonth())
    print(timemanager.getPrevYearMonth(2000,1))