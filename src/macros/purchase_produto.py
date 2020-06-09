# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 19:14:07 2020

@author: henrique.milagres
"""

import pandas as pd
from purchase_preprocessing import *
from purchase_garcom import *
import datetime
from datetime import timedelta 
import calendar 

class comprasProdutos:
    
    def copyDf(df):
        produtos = df[['CPF/CNPJ:',
                       'Documento:',
                       'Emissão:',
                       'Chave.NFe',
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
        compra_produtos =  comprasProdutos.copyDf(df)
        compra_produtos['Loja'] = list(map(comprasProdutos.loja,compra_produtos['CPF/CNPJ:']))
        return(compra_produtos)
        
if __name__ == '__main__':
    
    data_path = '../../data/'
    df = pd.read_excel(data_path+'Compras Jan a Mar 2020 Lucas Natan.xlsx')
    df = compras.run(df)
    
    df_produto = comprasProdutos.run(df)

    