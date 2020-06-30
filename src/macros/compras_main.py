#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 17:43:37 2020

@author: rodolfodollinger
"""

import pandas as pd
from purchase_preprocessing import compras
from purchase_garcom import garcomCompras
from purchase_nf import purchaseNF
from compras import purchaseProcessado
from purchase_produto import comprasProdutos

def preCompras(df_purchase):
    df_purchase_filtered = compras.run(df_purchase)
    df_purchase_garcom = garcomCompras.run(df_purchase_filtered)        
    df_purchase_nf =  purchaseNF.run(df_purchase_garcom) 
    df_purchase_saida = purchaseProcessado.run(df_purchase_nf)
    df_produto = comprasProdutos.run(df_purchase_filtered)
    return(df_purchase_saida,df_produto)


data_path = '../../data/'   
df_purchase = pd.read_excel(data_path+'Compras Jan a Mar 2020 Lucas Natan.xlsx')

comprasSaida, comprasProduto = preCompras(df_purchase)
del data_path, df_purchase
