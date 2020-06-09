# -*- coding: utf-8 -*-
"""
Objective: Module responsible for cleaning and prepare the purchase's input for LojaDoSapo
Created on Wed May 20 18:27:06 2020
@author: hmilagres
"""
import math
import pandas as pd



class compras:
    def filter_str(df,column,string,na):
        df = df[~df[column].str.contains(string, na = na)]
        return(df)
        
    
    def excludeUnnamedCols(df,cols,pattern):
        excludeCols = [s for s in cols if pattern in s]
        df = df.drop(columns = excludeCols)
        return(df)
        
    
    def fill_nan_values_list(x,y):
        try:
            if math.isnan(x):
                x = y.copy()
        except:
            pass
        return(x)
    
    def fill_nan_values(x,y):
        try:
            if math.isnan(x):
                x = y
        except:
            pass
        return(x)
    
    def define_pagamento(PARCELA,F_PGT,V_PGT,F_PRAZO,V_PRAZO,T_F_N):
        if PARCELA == 0:
            F_PGT = "DÉBITO"
            V_PGT = T_F_N
            F_PRAZO = "DÉBITO"
            V_PRAZO = T_F_N
        elif PARCELA == 1:
            F_PGT = "CRÉDITO A VISTA"
            V_PGT = T_F_N
            F_PRAZO = "CRÉDITO A VISTA"
            V_PRAZO = T_F_N   
        else:
            F_PGT = "CRÉDITO PARCELADO"
            V_PGT = T_F_N
            F_PRAZO = "CRÉDITO PARCELADO"
            V_PRAZO = T_F_N        
        return F_PGT,V_PGT,F_PRAZO,V_PRAZO
    
    def cria_parcela(V_PRAZO,PARCELA,T_F_N):
        if V_PRAZO == 0:
            PARCELA = 0
        else:
            PARCELA = round(T_F_N / V_PRAZO, 0)
        return PARCELA   
    
    
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
        # Excluding cpf/cnpj cells
        df_filtered = compras.filter_str(df,'CPF/CNPJ:', 'CPF/CNPJ:', na = False)
        df_filtered = compras.filter_str(df_filtered,'Tipo Operação', 'E', na = False)
        df_filtered = compras.filter_str(df_filtered,'Tipo Operação', 'S', na = False)
        
        cols = list(df_filtered)
        df_filtered = compras.excludeUnnamedCols(df_filtered, cols, 'Unnamed')
        cols = list(df_filtered)
        
        df_filtered = df_filtered.reset_index(drop=True)
        
        t_f_n = list(df_filtered['Total Nota Fiscal'])
        f_pgt = list(df_filtered['F.PGT'])
        v_pgt = list(df_filtered['V.PGT'])
        f_prazo = list(df_filtered['Prazo'])
        v_prazo = list(df_filtered['V.Prazo'])
        parcela = list(df_filtered['Parcelas'])
        
        ## ADIVINHA FORMA PAGAMENTO
        v_prazo = list(map(lambda x: 0 if math.isnan(x) else x, v_prazo))      
                
        
        parcela = list(map(compras.cria_parcela,v_prazo,parcela,t_f_n))
        f_pgt,v_pgt,f_prazo,v_prazo = zip(*map(compras.define_pagamento,parcela,f_pgt,v_pgt,f_prazo,v_prazo,t_f_n))
         
        
        ## FORMA A PRAZO
        df_filtered['Forma a prazo'] = list(map(compras.prazo,f_pgt,f_prazo))
          
        ## FORMA A VISTA
        df_filtered['Forma a vista'] = list(map(compras.avista,f_pgt,f_prazo))
        
        ## VALOR A PRAZO
        df_filtered['Valor a prazo'] = list(map(compras.valor_prazo,df_filtered['Forma a prazo'],
                                                        df_filtered['Forma a vista'],
                                                        t_f_n,f_prazo,v_pgt,v_prazo))
         
        
        ## PARCELA = 0 vira 1 e sem prazo parcela = 1
        df_filtered['Parcelas'] = list(map(compras.parcela_value,parcela,df_filtered['Forma a prazo']))
        
        ## VALOR A VISTA      
        df_filtered['Valor a vista'] = list(map(compras.valor_a_vista,t_f_n,df_filtered['Valor a prazo']))
        
        ## VALOR PARCELA 
        df_filtered['Valor Parcela'] = list(map(compras.valor_parcela,df_filtered['Forma a prazo'],
                                                        df_filtered['Valor a vista'],
                                                        df_filtered['Valor a prazo'], 
                                                        df_filtered['Parcelas']))
        
        
 

        return(df_filtered) 
    
 

if __name__ == '__main__':
    
    data_path = '../../data/'
    df = pd.read_excel(data_path+'Compras Jan a Mar 2020 Lucas Natan.xlsx')
    
    df_filtered = compras.run(df)
    #df_filtered.to_csv('compras', sep='\t')
    del data_path,df        
         