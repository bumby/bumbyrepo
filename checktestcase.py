# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 11:09:22 2019

@author: USER
"""

import unittest
from kospi_history import *

class TestKospiHistoryInfo(unittest.TestCase):
     
    
    def test_getTargetMonth(self):
        
        kospi_info = KOSPIHISTORYINFO()
               
        self.assertEqual(kospi_info.get_expiration_date("201602"),"2016/02/11")
        self.assertEqual(kospi_info.get_expiration_date("200002"),"There is no information for argument year month")
        
    def test_get_remaining_days(self):
        kospi_info = KOSPIHISTORYINFO()
        
        self.assertEqual(kospi_info.get_remaining_days("2016/02/22","201603"),12)
        self.assertEqual(kospi_info.get_remaining_days("2016/02/22","202203"),-1)
        
    def test_get90dayHistorcalVol(self):
        kospi_info = KOSPIHISTORYINFO()
        print(kospi_info.get90dayHistorcalVol("2016/02/23"))
        self.assertEqual(int(kospi_info.get90dayHistorcalVol("2016/02/23")),15)
        
    
      






if __name__ == '__main__':
    unittest.main()