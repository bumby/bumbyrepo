# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 20:59:51 2018

@author: USER
"""

import sys
from PyQt5.QtWidgets import *

def clicked_slot():
    print('clicked')



app = QApplication(sys.argv)
label = QLabel("Hello, PyQt")
label.show()


app.exec_()
