#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 17:43:40 2020

@author: rodolfodollinger
"""

import pandas as pd
from vendas_preprocessing import vendas
from vendas_garcom import garcomVendas
from vendas_notaFiscal import vendasNF
from vendas import vendasProcessado
from vendas_produto import produtos


def preVendas(df_vendas):
    df_vendas_filtered = vendas.run(df_vendas)
    df_vendas_garcom = garcomVendas.run(df_vendas_filtered)        
    df_vendas_nf =  vendasNF.run(df_vendas_garcom) 
    df_vendas_saida = vendasProcessado.run(df_vendas_nf)
    vendas_produto = produtos.run(df_vendas_filtered)
    return(df_vendas_saida,vendas_produto)


data_path = '../../data/'   
df_vendas = pd.read_excel(data_path+'VENDAS Jan a Mar 2020 Lucas Natan.xlsx')

vendasSaida, vendasProduto = preVendas(df_vendas)

del data_path,df_vendas 
