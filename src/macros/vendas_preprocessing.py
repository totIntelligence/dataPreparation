# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:57:59 2020

@author: rodnv
"""

import math
import pandas as pd

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
        
    def parcela_value(parcela,forma_a_prazo):
        if parcela == 0:
            return(1)
        elif forma_a_prazo == 'SEM PRAZO':
            return(1)
        else:
            return(parcela)
        
    def valor_a_vista(tfn,valor_a_prazo):
        return(tfn - valor_a_prazo)
    
    def valor_parcela(forma_a_prazo,valor_a_vista,valor_a_prazo,parcela):
        if forma_a_prazo == 'SEM PRAZO':
            return(valor_a_vista)
        else:
            return(valor_a_prazo/parcela)
        
        
    def run(df):
        df_filtered = vendas.filter_str(df,'CPF/CNPJ:', 'CPF/CNPJ:', na = False)
        df_filtered = vendas.filter_str(df_filtered,'Tipo Operação', 'E', na = False)
        
        cols = list(df_filtered)
        df_filtered = vendas.excludeUnnamedCols(df_filtered, cols, 'Unnamed')
        cols = list(df_filtered)
        
        df_filtered = df_filtered.reset_index(drop=True)
        
        cols = list(df_filtered)
        
        
        t_f_n = list(df_filtered['Total Nota Fiscal'])
        f_pgt = list(df_filtered['F.PGT'])
        v_pgt = list(df_filtered['V.PGT'])
        f_prazo = list(df_filtered['Prazo'])
        v_prazo = list(df_filtered['V.Prazo'])
        parcela = list(df_filtered['Parcelas'])
        
        f_prazo = list(map(vendas.fill_nan_values,f_prazo,f_pgt))
        df_filtered['Prazo'] = f_prazo.copy()
        
        v_prazo = list(map(vendas.fill_nan_values,v_prazo,v_pgt))
        df_filtered['V.Prazo'] = v_prazo.copy()
        
        df_filtered['Forma a prazo'] = list(map(vendas.prazo,f_pgt,f_prazo))
        df_filtered['Forma a vista'] = list(map(vendas.avista,f_pgt,f_prazo))
        df_filtered['Valor a prazo'] = list(map(vendas.valor_prazo,df_filtered['Forma a prazo'],
                                                df_filtered['Forma a vista'],
                                                t_f_n,f_prazo,v_pgt,v_prazo))
        
        df_filtered['Parcela'] = list(map(vendas.parcela_value,parcela,df_filtered['Forma a prazo']))
        df_filtered['Valor a vista'] = list(map(vendas.valor_a_vista,t_f_n,df_filtered['Valor a prazo']))
        df_filtered['Valor Parcela'] = list(map(vendas.valor_parcela,df_filtered['Forma a prazo'],
                                                df_filtered['Valor a vista'],
                                                df_filtered['Valor a prazo'], 
                                                df_filtered['Parcela']))
        return(df_filtered)


if __name__ == '__main__':
    
    data_path = '../../data/'
    df = pd.read_excel(data_path+'VENDAS Jan a Mar 2020 Lucas Natan.xlsx')
    
    df_filtered = vendas.run(df)
    df_filtered.to_csv('vendas', sep='\t') 
    del data_path,df        
        