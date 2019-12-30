# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 19:32:25 2019

@author: USER
"""
import math
import pandas as pd

class OptCodeTool:
            
    def optcode_gen(self, optstrike, expirationdate, putncall):

        # target price  



        #put and sell code and kospi200
        if putncall == "call" :
            opt_putncall_code = "201"
            price_divide = int(math.floor(optstrike/2.5))
            opt_index = int((price_divide+1)*2.5)
            opt_index_str = str(opt_index)
            #print(opt_index_str)
        elif putncall == "put" :
            opt_putncall_code = "301"
            price_divide = int(math.floor(optstrike/2.5))
            opt_index = int((price_divide)*2.5)
            opt_index_str = str(opt_index)
           # print(opt_index_str)
        else :
            print("no such code")
            raise Exception('no such code')  


        #target expiration year
        expiration_year = expirationdate[0:4]
        if  expiration_year=="2019" :
            expiration_year_code = "P"
        elif expiration_year=="2020" :
            expiration_year_code = "Q"
        elif expiration_year=="2021" :
            expiration_year_code = "R"
        elif expiration_year=="2022" :
            expiration_year_code = "S"
        elif expiration_year=="2023" :
            expiration_year_code = "T"
        elif expiration_year=="2024" :
            expiration_year_code = "V"
        elif expiration_year=="2025" :
            expiration_year_code = "W"  
            
        elif expiration_year=="2018" :
            expiration_year_code = "N"  
        elif expiration_year=="2017" :
            expiration_year_code = "M"
        elif expiration_year=="2016" :
            expiration_year_code = "L"
        elif expiration_year=="2015" :
            expiration_year_code = "K"    
        elif expiration_year=="2014" :
            expiration_year_code = "J"
        elif expiration_year=="2013" :
            expiration_year_code = "H"
        elif expiration_year=="2012" :
            expiration_year_code = "G"
        elif expiration_year=="2011" :
            expiration_year_code = "F"            
        elif expiration_year=="2010" :
            expiration_year_code = "E"
        elif expiration_year=="2009" :
            expiration_year_code = "D"
        elif expiration_year=="2008" :
            expiration_year_code = "C"
        elif expiration_year=="2007" :
            expiration_year_code = "B"
        elif expiration_year=="2006" :
            expiration_year_code = "A"
            
        
        
        else :
            print("option code is available only for 2025")
            raise Exception("option code is available only for 2025")

        #target expiration month
        expiration_month  = expirationdate[4:6]
        if  expiration_month=="01" :
            expiration_month_code = "1"
        elif expiration_month=="02" :
            expiration_month_code = "2"
        elif expiration_month=="03" :
            expiration_month_code = "3"
        elif expiration_month=="04" :
            expiration_month_code = "4"
        elif expiration_month=="05" :
            expiration_month_code = "5"
        elif expiration_month=="06" :
            expiration_month_code = "6"
        elif expiration_month=="07" :
            expiration_month_code = "7"    
        elif expiration_month=="08" :
            expiration_month_code = "8"
        elif expiration_month=="09" :
            expiration_month_code = "9"
        elif expiration_month=="10" :
            expiration_month_code = "A"
        elif expiration_month=="11" :
            expiration_month_code = "B" 
        elif expiration_month=="12" :
            expiration_month_code = "C"
        else :
            print("choose only for 1~12")
            raise Exception("choose only for 1~12")

        optcode = opt_putncall_code + expiration_year_code+ expiration_month_code + opt_index_str
        #print(optcode)
        return optcode
        
    
    def optcode_encode(self, optcode):

        # target price  



        #put and sell code and kospi200
        if optcode[0:3] == "201":
            putncall = "call"
        elif optcode[0:3] == "301":
            putncall = "put"
        else:
            print("no such code")
        
        #target expiration year
        
        expiration_year_code = optcode[3]
        
        if  expiration_year_code == "P":
            expiration_year="2019" 
            
        elif expiration_year_code == "Q":
            expiration_year="2020" 
            
        elif expiration_year_code == "R":
            expiration_year="2021" 
            
        elif expiration_year_code == "S":
            expiration_year="2022" 
            
        elif expiration_year_code == "T":
            expiration_year="2023" 
            
        elif expiration_year_code == "V":
            expiration_year="2024" 
            
        elif expiration_year_code == "W":
            expiration_year="2025" 
                        
        elif expiration_year_code == "N" :
            expiration_year="2018" 
            
        elif expiration_year_code == "M":
            expiration_year="2017" 
            
        elif expiration_year_code == "L":
            expiration_year="2016" 
            
        elif expiration_year_code == "K":
            expiration_year="2015" 
                
        elif expiration_year_code == "J":
            expiration_year="2014" 
            
        elif expiration_year_code == "H":
            expiration_year="2013" 
            
        elif expiration_year_code == "G":
            expiration_year="2012" 
            
        elif expiration_year_code == "F":
            expiration_year="2011" 
            
        elif expiration_year_code == "E":
            expiration_year="2010" 
            
        elif expiration_year_code == "D":
            expiration_year="2009" 
            
        elif expiration_year_code == "C":
            expiration_year="2008" 
            
        elif expiration_year_code == "B":
            expiration_year="2007" 
            
        elif expiration_year_code == "A":
            expiration_year="2006" 
            
   
        
        else :
            print("option code is available only for 2025")
            raise Exception("option code is available only for 2025")

        #target expiration month
        expiration_month_code = optcode[4]  
               

        if  expiration_month_code == "1":
            expiration_month="01" 
            
        elif expiration_month_code == "2":
            expiration_month="02" 
            
        elif expiration_month_code == "3":
            expiration_month="03" 
            
        elif expiration_month_code == "4":
            expiration_month="04" 
            
        elif expiration_month_code == "5":
            expiration_month="05" 
            
        elif expiration_month_code == "6":
            expiration_month="06" 
            
        elif expiration_month_code == "7":
            expiration_month="07" 
            
        elif expiration_month_code == "8":
            expiration_month="08" 
            
        elif expiration_month_code == "9":
            expiration_month="09" 
            
        elif expiration_month_code == "A":
            expiration_month="10" 
            
        elif expiration_month_code == "B" :
            expiration_month="11" 
            
        elif expiration_month_code == "C":
            expiration_month="12" 
            
        else :
            print("choose only for 1~12")
            raise Exception("choose only for 1~12")


        optstrike = pd.to_numeric(optcode[5:7])
        if optcode[7] == '0':
            optstrike = optstrike*10.0
        elif optcode[7] == '2':
            optstrike = optstrike*10.0 + 2.5
        elif optcode[7] == '5':
            optstrike = optstrike*10.0 + 5.0
        elif optcode[7] == '7':
            optstrike = optstrike*10.0 + 7.5
        else:
            print("no such code")

       
        #print(optcode)
        return putncall,expiration_year,expiration_month,optstrike
     

