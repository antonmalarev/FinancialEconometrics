# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 11:10:01 2020

@author: Anton Malarev
"""

def benford(df):
    from matplotlib.pyplot import hist
    
    df["Functional Amount first number"] = df["Functional Amount"].apply(lambda x: x[0])
    
    df_Benford = df.groupby(["Functional Amount first number"]).agg({"Functional Amount first number": 'count'})
    df_Benford.columns = ["Functional Amount first number count"]
    df_Benford = df_Benford.reset_index()
    df_Benford = df_Benford.drop([0,1])
    
    #plot
    return hist(df_Benford["Functional Amount first number"], weights=df_Benford["Functional Amount first number count"])
