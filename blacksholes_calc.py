# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 19:05:49 2021

@author: USER
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


class BlackSholes_calc:


    #def __init__(self):
   
            

    def getCallPrice(self, K, S0, r, sigma, T):
   
        d1 = (math.log(S0/K)+(r+sigma*sigma/2.0)*T)/(sigma*math.sqrt(T))
        d2 = (math.log(S0/K)+(r-sigma*sigma/2.0)*T)/(sigma*math.sqrt(T))
        
        call_price = S0*norm.cdf(d1)-K*math.exp(-r*T)*norm.cdf(d2)
        return call_price
    
    def getPutPrice(self, K, S0, r, sigma, T):
  
        
        d1 = (math.log(S0/K)+(r+sigma*sigma/2.0)*T)/(sigma*math.sqrt(T))
        d2 = (math.log(S0/K)+(r-sigma*sigma/2.0)*T)/(sigma*math.sqrt(T))
        
        
        put_price = K*math.exp(-r*T)*norm.cdf(-d2)-S0*norm.cdf(-d1)
        return put_price
    
    def getCallDelta(self, K, S0, r, sigma, T):

        d1 = (math.log(S0/K)+(r+sigma*sigma/2.0)*T)/(sigma*math.sqrt(T))
        
        
        return norm.cdf(d1)
        
    
    def getPutDelta(self, K, S0, r, sigma, T):
     
        d1 = (math.log(S0/K)+(r+sigma*sigma/2.0)*T)/(sigma*math.sqrt(T))
          
        return norm.cdf(d1)-1
    
    def getCallIV(self, K, S0, r, T, Vm):
        
        sigma = 0.5
        tol = 1.0e-6
        d1 = (math.log(S0/K)+(r+sigma*sigma/2.0)*T)/(sigma*math.sqrt(T))
        d2 = d1-sigma*math.sqrt(T)
        call_price = S0*norm.cdf(d1)-K*math.exp(-r*T)*norm.cdf(d2)
        vega = S0*math.sqrt(T)*norm.pdf(d1)

        while math.fabs(call_price - Vm) > tol:
            sigma = sigma - (call_price - Vm)/vega
            d1 = (math.log(S0/K)+(r+sigma*sigma/2.0)*T)/(sigma*math.sqrt(T))
            d2 = d1-sigma*math.sqrt(T)      
            call_price = S0*norm.cdf(d1)-K*math.exp(-r*T)*norm.cdf(d2)
            vega = S0*math.sqrt(T)*norm.pdf(d1)
        
        return str(sigma*100)

    def getPutIV(self, K, S0, r, T, Vm):
        sigma = 0.5
        tol = 1.0e-6
        d1 = (math.log(S0/K)+(r+sigma*sigma/2.0)*T)/(sigma*math.sqrt(T))
        d2 = d1-sigma*math.sqrt(T)
        put_price = K*math.exp(-r*T)*norm.cdf(-d2)-S0*norm.cdf(-d1)
        vega = S0*math.sqrt(T)*norm.pdf(d1)
        print(vega)
        while math.fabs(put_price - Vm) > tol:
            sigma = sigma - (put_price - Vm)/vega
            d1 = (math.log(S0/K)+(r+sigma*sigma/2.0)*T)/(sigma*math.sqrt(T))
            d2 = d1-sigma*math.sqrt(T)      
            put_price = K*math.exp(-r*T)*norm.cdf(-d2)-S0*norm.cdf(-d1)
            vega = S0*math.sqrt(T)*norm.pdf(d1)
        
        return str(sigma*100)
    

if __name__ == "__main__":
   # app = QApplication(sys.argv)
   K = 377.5
   S0= 419.2    
   r = 0.02
   sigma = 0.2314
   T = 43/365
   per_rate = 1.29  #1.03 85%  1.29 90%

   bscalc = BlackSholes_calc()

   z_high = math.log(S0)+(r-sigma*sigma/2.0)*T+per_rate*sigma*math.sqrt(T)
   S_high = math.exp(z_high)
   z_low = math.log(S0)+(r-sigma*sigma/2.0)*T-per_rate*sigma*math.sqrt(T)
   S_low = math.exp(z_low)
        
   print("high ",S_high," low ", S_low, " norm ",norm.cdf(1.29), " call_price ",bscalc.getCallPrice(K, S0, r, sigma, T)," put_price ",bscalc.getPutPrice( K, S0, r, sigma, T) )
   print("implied call" , bscalc.getCallIV(447, 423.5, 0.03, 32/365, 0.96))
   print("implied put" , bscalc.getPutIV(410, 423.5, 0.03, 32/365, 2.89))