# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:24:08 2019

@author: USER
"""
from datetime import datetime


class timeManager:
    
    def __init__(self):
        self.now = datetime.now()
            
    def getCurrentDash(self):
        self.now = datetime.now()
        mon = str(self.now.month)
        mon = mon.zfill(2)
        self.currentdash = str(self.now.year)+"/"+mon+"/"+str(self.now.day)
        return self.currentdash

    def getTodayMonth(self):
        self.now = datetime.now()
        self.currmonth  = str(self.now.year)+str(self.now.month)
        return self.currmonth
        
    #다음달 잔여일 30일 이상 차월 선택 
    def getTargetMonth(self):
        self.now = datetime.now()
        self.nextmonthyear = self.now.year
        self.nextmonth = ((self.now.month)%12)+1
        if self.nextmonth == 1:
            self.nextmonthyear = self.nextmonthyear + 1 
        self.targetmonth = str(self.nextmonthyear)+str(self.nextmonth).zfill(2)
        return self.targetmonth
    
    def getCurrentHourMinSec(self):
        self.now = datetime.now()
        self.currentHMS=self.now.hour*10000+self.now.minute*100+self.now.second
        return str(self.currentHMS)
    #다음달 잔여일 30일 이하 2달후 선택 
#    def getTargetMonth(self):
#        self.now = datetime.now()
#        self.nextmonthyear = self.now.year
#        self.next2month = ((self.now.month)%12)+2
#        if self.next2month == 1:
#            self.nextmonthyear = self.nextmonthyear + 1 
#        elif self.next2month == 2:
#            self.nextmonthyear = self.nextmonthyear + 1 
#        self.target2month = str(self.nextmonthyear)+str(self.next2month).zfill(2)
#        return self.target2month
#    
       
        
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
    print(timemanager.getPrevYearMonth(2000,12))
    print(timemanager.getCurrentDash())
    print(timemanager.getCurrentHourMinSec())