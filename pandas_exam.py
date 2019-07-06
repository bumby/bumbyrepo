# -*- coding: utf-8 -*-
"""
Created on Tue May 29 22:10:34 2018

@author: USER
"""

from pandas import Series, DataFrame

mystock = ['kakao', 'naver']
print(mystock[0])
print(mystock[1])

for stock in mystock:
    print(stock)
    
kakao_daily_closing_prices = {'2016-02-19': 92600,
                              '2016-02-18': 92400,
                              '2016-02-17': 92100,
                              
                              }

print(kakao_daily_closing_prices['2016-02-19'])


kakao = Series([92600, 92400, 92100, 94300, 92300])
print(kakao)

kakao2 = Series([92600, 92400, 92100, 94300, 92300], index = ['2016-02-19',
                                                             '2016-02-18',
                                                             '2016-02-17',
                                                             '2016-02-16',
                                                             '2016-02-15'])
print(kakao2)

mine = Series([10, 20, 30], index = ['naver','sk','kt'])
friend = Series([10, 30, 20], index = ['kt','naver','sk'])

merge = mine + friend

print(merge)

#DataFrame 예제
raw_data = {'col0':[1,2,3,4],
            'col1':[10, 20, 30, 40],
            'col2':[100,200,300,400]}

data = DataFrame(raw_data)
print(data)
