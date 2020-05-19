# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:57:59 2020

@author: rodnv
"""

import math

class preprocessing:
    
    
    def filter_str(df,column,string,na):
        df = df[~df[column].str.contains(string, na = na)]
        return(df)
        
    
    def excludeUnnamedCols(df,cols,pattern):
        excludeCols = [s for s in cols if pattern in s]
        df = df.drop(columns = excludeCols)
        return(df)
        
    
    def fill_nan_values(x,y):
        try:
            if math.isnan(x):
                x = y.copy()
        except:
            pass
        return(x)