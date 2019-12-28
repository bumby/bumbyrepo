# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 17:56:12 2019

@author: USER
"""

import json

class TargetOptHistory:
    def __init__(self):
        self.targetOptData = {}
        
    def setOptData(self,time_, optcode_, offerho1_, bidho1_, theory_ ):
        optdata = {'optcode' : optcode_,
                   'offerho' : offerho1_,
                   'bidho'   : bidho1_,
                   'theory'  : theory_}
        self.targetOptData[time_] = optdata
    
    
    def saveTargetOptHistory(self, filename):
        with open(filename, "w") as fp:
            json.dump(self.targetOptData, fp)
            
            