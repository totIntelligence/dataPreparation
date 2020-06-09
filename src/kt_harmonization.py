# -*- coding: utf-8 -*-

from purchase_preprocessing import compras
from purchase_garcom import garcomCompras
from purchase_nf import purchaseNF
from purchase_produto import comprasProdutos 

from vendas_preprocessing import vendas
from vendas_garcom import garcomVendas
from vendas_notaFiscal import vendasNF
from vendas_produto import produtos



import pandas as pd


if __name__ == '__main__':
    
    data_path = '../../data/'   
    
    df_vendas = pd.read_excel(data_path+'VENDAS Jan a Mar 2020 Lucas Natan.xlsx')  
    df_vendas_filtered = vendas.run(df_vendas)
    df_vendas_garcom = garcomVendas.run(df_vendas_filtered)        
    df_vendas_nf =  vendasNF.run(df_vendas_garcom) 
    df_vendas_produto =  produtos.run(df_vendas_filtered)  
    
    df_compras = pd.read_excel(data_path+'Compras Jan a Mar 2020 Lucas Natan.xlsx')  
    df_compras_filtered = compras.run(df_compras)
    df_compras_garcom = garcomCompras.run(df_compras_filtered)        
    df_compras_nf =  purchaseNF.run(df_compras_garcom) 
    df_compras_produto =  comprasProdutos.run(df_compras_filtered)        

    
     