# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 17:43:10 2019

@author: USER
"""
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import collections

with open('20191212.json') as json_file:
    data = json.load(json_file)
    괴리율list =[]
    dataordered = collections.OrderedDict(sorted(data.items()))
    for p in dataordered:
        print(p,':', pd.to_numeric(data[p]["bidho"])/pd.to_numeric(data[p]["theory"]), ":" , data[p]["optcode"])
        괴리율list.append(pd.to_numeric(data[p]["bidho"])/pd.to_numeric(data[p]["theory"]))
    #print('data', data["142427"]["optcode"])
    #print(괴리율list)
    
    #    
    ## Generate data on commute times.
    #size, scale = 1000, 10
    괴리율 = pd.Series(괴리율list)
    #
    plt.figure(1)
    괴리율.plot.hist(grid=True, bins=50, rwidth=1, color='#607c8e')
    plt.title('target option 괴리율 distribution')
    plt.xlabel('괴리율')
    plt.ylabel('counts')
    plt.grid(axis='y', alpha=0.75)
    
    
    