# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 19:14:07 2020

@author: rodnv
"""

import pandas as pd
from vendas_preprocessing import *
from vendas_garcom import *
import datetime
from datetime import timedelta 
import calendar 

class produtos:
    
    def copyDf(df):
        produtos = df[['CPF/CNPJ:',
                       'Documento:',
                       'Emissão:',
                       'Cod. Cliente/Fornecedor:',
                       'Cliente/Fornecedor:',
                       'UF',
                       'Cod Vendedor',
                       'Vendedor',
                       'Código',
                       'Descrição',
                       'Qtd.',
                       'Custo',
                       'Vl. Unit. ',
                       'Vl. Desc. ',
                       'Vl. Acrés. ',
                       'Vl. Total (ITEM)']]
        return(produtos)
        
    
    def loja(cnpj):
        if str(cnpj) == '28.608.143/0001-08':
            return('Sede')
        elif str(cnpj) == '28608143000108':
            return('Del Rey')
        elif str(cnpj) == '27.809.544/0001-55':
            return('Cidade')
        
    def run(df):
        venda_produtos =  produtos.copyDf(df)
        venda_produtos['Loja'] = list(map(produtos.loja,venda_produtos['CPF/CNPJ:']))
        return(venda_produtos)
        
if __name__ == '__main__':
    
    data_path = '../../data/'
    df = pd.read_excel(data_path+'VENDAS Jan a Mar 2020 Lucas Natan.xlsx')
    df = vendas.run(df)
    
    vendas_produto = produtos.run(df)
