# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 18:06:05 2020

@author: Anton Malarev
"""


def chowtest(series,p,q,bp):
    
    from statsmodels.tsa.arima_model import ARIMA
    import numpy as np
    from scipy.stats import f
    
    #Fit ARMA(p,q) to the whole series
    model = ARIMA(series, order=(p,0,q))
    model_fit = model.fit(trend = 'nc',disp=0)
    
    #Compute RSS
    resid = model_fit.resid
    RSS = np.mat(resid) * np.mat(resid).transpose()
    RSS = RSS[0,0]
    
    #Divide series into two groups and fit ARMA(p,q)
    series1 = series[:bp]
    model1 = ARIMA(series1, order=(p,0,q))
    model_fit1 = model1.fit(trend = 'nc',disp=0)
    
    series2 = series[bp:]
    model2 = ARIMA(series2, order=(p,0,q))
    model_fit2 = model2.fit(trend = 'nc',disp=0)
    
    #Compute RSS1
    resid1 = model_fit1.resid
    RSS1 = np.mat(resid1) * np.mat(resid1).transpose()
    RSS1 = RSS1[0,0]
    
    #Compute RSS2
    resid2 = model_fit2.resid
    RSS2 = np.mat(resid2) * np.mat(resid2).transpose()
    RSS2 = RSS2[0,0]
    
    #Chow Test
    #Compute the Chow F-statistic

    K = p+q+1
    N1 = len(series1)
    N2 = len(series2)
    chow_statistic = ((RSS-RSS1-RSS2)/K)/((RSS1+RSS2)/(N1+N2-(2*K)))

    #Compare the statistics to the critical values of F distribution

    h = chow_statistic > f.ppf(0.95, K, N1+N2-(2*K))
    
    #Null hypothesis: no break point
    #Reject the null hypothesis (there is break point) if your calculated F-value falls into the rejection region 
    #(i.e. if the calculated F-value is greater than the F-critical value)
    
    if h:
        h = 'There is a break point at '+ str(bp)
    else:
        h = 'No break point detected'
    
    return h