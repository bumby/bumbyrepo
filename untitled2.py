# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 22:17:39 2019

@author: USER
"""

from news_acq import *

if __name__ == "__main__":


    xreal = XReal_NWS_.get_instance()
    xreal.start()
    while xreal.count < 100:
        pythoncom.PumpWaitingMessages()