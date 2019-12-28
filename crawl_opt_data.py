# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 20:33:41 2019

@author: USER
"""

#www.krx.co.kr 에서 옵션데이타를 획득하는 파일
#request를 통해 크롤링을 진행한는 과정


import pandas as pd
import numpy as np
import requests
from io import BytesIO
from datetime import datetime, timedelta
import time
import json
from DBanal import *
from timeManager import *


tmanager = timeManager()

data = pd.read_csv("kospi200data.csv",sep=",")
data.head()
df = data[["일자","현재지수"]]
print(df["일자"])

#크롤링할 option data를 지정하는 과정
# kospi 과거데이타를 확보하고 과거데이터에서 call의 경우 한달 전 -30, +50 범위의 
#옵션을 대상범위로 놓고 put의 경우에는 -50,+30 범위의 옵션을 대상범위로 놓는다. 
yytot = ['2018','2017','2016','2015','2014','2013','2012','2011','2010']
mmtot = ['01','02','03','04','05','06','07','08','09','10','11','12']

dbanal = DBalalysis('2')

for i in yytot:
    for j in mmtot:
     #   for target
     
        #scan 범위를 지정  
        scanmonth = tmanager.getPrevYearMonth(pd.to_numeric(i),pd.to_numeric(j))
        fromdate = scanmonth+'01'
        todate = scanmonth+'31'
        
        
        kospi_at_target = 0  #target kospi 에 대하여 
        index = 0
        print('scanmonth',scanmonth)
        for k in df["일자"]:
            targetmon_kospi_price = i+'/'+j
            index = index + 1
            #print(k[0:7])
            if targetmon_kospi_price == k[0:7]:  #현재 값에 비해 날짜가 01, 02 03일때 월초의 최초일의 날짜에 대한 한번만  검색 
                  print(k,df["현재지수"][index])
                  kospi_at_target = df["현재지수"][index]
                  break;
            
                  
            #print(k)
        #kospi 200 지점에서 높은 곳으로 40.0 spread
        #a = np.arange(kospi_at_target-30, kospi_at_target+50,2.5)  #call
        a = np.arange(kospi_at_target-50, kospi_at_target+30,2.5)  #put
        print('targetmon_kospi_price',targetmon_kospi_price,'kospi_at_target',kospi_at_target, a)
     
        
        for k in a:
   
            for codeindex in range(0,10):
               # optcode = dbanal.optcode_gen(k,i+j,"call")        #dbanal optcode_gen 은 '년/월' 형태가 아니라 '년월'
                optcode = dbanal.optcode_gen(k,i+j,"put")
                
               # print('optcode' + optcode)
                if optcode[7] == '2' or optcode[7]=='7':
                    opt_price = optcode[5:8]+'.5'
                else :
                    opt_price = optcode[5:8]+'.0'
            
                targetmon_wo_slash = targetmon_kospi_price[0:4]+targetmon_kospi_price[5:7]
                
                isu_cd = 'KR4'+optcode+str(codeindex)
                #isu_nm = '코스피200 '+'C '+targetmon_wo_slash+' '+opt_price
                isu_nm = '코스피200 '+'P '+targetmon_wo_slash+' '+opt_price
                isu_cdnm = isu_nm+'/'+isu_cd
                isu_srt_cd = 'K'+optcode
               
                                

        
        
#        해당월에 상응하는 데이타 확보 code 명
#        201903은  isu_cdnm '코스피200 C 202003 320.0/KR4201Q33205' 라는 코드를 생성
#        isu_cd는 KR4201Q33205 라는 코드 생성
#        날짜는 201902 한달의 내용을 입력
        

                gen_otp_url = "http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx"
#                gen_otp_data = {
#                'name': 'fileDown',
#                'filetype': 'csv',
#                'url': 'MKD/06/0601/06010200/mkd06010200_04',
#                #'isu_cdnm': '코스피200 C 202003 320.0',
#                'isu_cdnm': '코스피200 C 202003 322.5/KR4201Q33221',
#                'isu_cd': 'KR4201Q33221',
#                'isu_nm': '코스피200 C 202003 322.5',
#                'isu_srt_cd': 'K201Q3322',
#                'fromdate': '20191120',
#                'todate': '20191220',
#                'gubun': '2',
#                'acsFlag': 'N',
#                'pagePath': '/contents/MKD/06/0602/06020200/MKD06020200.jsp',
#                }
                
                gen_otp_data = {
                'name': 'fileDown',
                'filetype': 'csv',
                'url': 'MKD/06/0601/06010200/mkd06010200_04',
                #'isu_cdnm': '코스피200 C 202003 320.0',
                'isu_cdnm': isu_cdnm,
                'isu_cd': isu_cd,
                'isu_nm': isu_nm,
                'isu_srt_cd': isu_srt_cd,
                'fromdate': fromdate,
                'todate': todate,
                'gubun': '2',
                'acsFlag': 'N',
                'pagePath': '/contents/MKD/06/0602/06020200/MKD06020200.jsp',
                }
                
                
                gen_header = {
                'User-Agent': 'Mozilla/5.0',
                }
                req = requests.get(url=gen_otp_url, params=gen_otp_data, headers=gen_header) 
                code = req.content

                
                
                gen_url = 'http://file.krx.co.kr/download.jspx'
                gen_header = {
                'User-Agent': 'Mozilla/5.0',
                'Referer':'http://marketdata.krx.co.kr/mdi',
                'Host':'file.krx.co.kr'
                }
                form_data = {
                        'code':code
                    }
                p = requests.post(gen_url,form_data,headers = gen_header)
                print('length', len(p.content), 'isu_cd',isu_cd)
                if len(p.content) > 200:
                    p.encoding = "utf-8-sig"
                 
                    print('결과')
                    f2 = pd.read_csv(BytesIO(p.content), header=0, thousands=',')
                    
                    export_csv = f2.to_csv ('./data/'+isu_srt_cd+'.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path
                    print(f2)
                    
                    print(isu_cd)
                    print(isu_nm)
                    print(isu_cdnm) 
                    print(isu_srt_cd)
                
                
