# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:57:59 2020

@author: rodnv
"""

import math

class vendas:
    
    
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
    
    def prazo(f_pgt,f_prazo):
        if (f_pgt == 'CRÉDITO PARCELADO') | (f_prazo == 'CRÉDITO PARCELADO'):
            return('CRÉDITO PARCELADO')
        elif (f_pgt == 'CRÉDITO A VISTA') | (f_prazo == 'CRÉDITO A VISTA'):
            return('CRÉDITO A VISTA')
        elif (f_pgt == '30 DIAS - SITE') | (f_prazo == '30 DIAS - SITE'):
            return('30 DIAS - SITE')
        else:
            return('SEM PRAZO')
        
    def avista(f_pgt,f_prazo):
        if (f_pgt == 'DÉBITO') | (f_prazo == 'DÉBITO'):
            return('DÉBITO')
        elif (f_pgt == 'DINHEIRO') | (f_prazo == 'DINHEIRO'):
            return('DINHEIRO')
        elif (f_pgt == 'DINHEIRO ( PENDENTE ACERTO)') | (f_prazo == 'DINHEIRO ( PENDENTE ACERTO)'):
            return('DINHEIRO ( PENDENTE ACERTO)')
        elif (f_pgt == 'TRANFÊNCIA ITAU') | (f_prazo == 'TRANFÊNCIA ITAU'):
            return('TRANFÊNCIA ITAU')
        elif (f_pgt == 'TRANFÊNCIA SANTANDER') | (f_prazo == 'TRANFÊNCIA SANTANDER'):
            return('TRANFÊNCIA SANTANDER')
        elif (f_pgt == 'TROCA') | (f_prazo == 'TROCA'):
            return('TROCA')
        else:
            return('A PRAZO')
        
    def valor_prazo(forma_a_prazo,forma_a_vista,tfn,f_prazo,v_pgt,v_prazo):
        if (forma_a_prazo == 'SEM PRAZO'):
            return(0)
        elif (forma_a_prazo != 'SEM PRAZO') & (forma_a_vista == 'A PRAZO'):
            return(tfn)
        elif forma_a_prazo == f_prazo:
            return(tfn - v_pgt)
        else:
            return(tfn - v_prazo)
        
        
        
        
        
        
        
        
        
        