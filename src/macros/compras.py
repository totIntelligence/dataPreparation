# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 18:34:18 2020

@author: rodnv
"""

# -*- coding: utf-8 -*-
from purchase_preprocessing import compras
from purchase_garcom import garcomCompras
from purchase_nf import purchaseNF 
import math

from datetime import date  

import pandas as pd

class purchaseProcessado:
    
    def criaStatus(data_previsao):
        if data_previsao < date.today():
            return 'Pago'
        else:
            return 'A Pagar'

    def formaPagamento(formaAPrazo,valorAPrazo,formaAVista,valorAVista):
        if (valorAPrazo >= valorAVista):
            return formaAPrazo
        else:
            return formaAVista
        
    def run(df_purchase_nf):
        df_purchase_nf['Status'] = list(map(purchaseProcessado.criaStatus,df_purchase_nf['data_previsao']))
        df_purchase_nf['tipo_documento'] = len(df_purchase_nf)*['Insumos']
        df_purchase_nf['natureza'] = len(df_purchase_nf)*['Despesas']
        df_purchase_nf['forma_pagamento'] = list(map(purchaseProcessado.formaPagamento,
                                                     df_purchase_nf['formaAPrazo'],
                                                     df_purchase_nf['valorAPrazo'],
                                                     df_purchase_nf['formaAVista'],
                                                     df_purchase_nf['valorAVista']))
        df_purchase_nf['observacao'] = len(df_purchase_nf)*[math.nan]
        df_purchase_nf['dth_real'] = len(df_purchase_nf)*[math.nan]
        
        df_purchase_nf = df_purchase_nf.drop(columns=['cnpjLoja','valorNotaFiscal',
                                              'formaAPrazo','valorAPrazo',
                                              'formaAVista','valorAVista'])
        
        df_purchase_nf.columns = ['pdv','id_documento_sistema','dth_emissao',
                                 'fatura','id_cliente_fornecedor','nome_cliente_fornecedor',
                                 'cep_cliente_fornecedor','valor','qtd_parcelas',
                                 'parcelas','dth_previsto','status','tipo_documento',
                                 'natureza','forma_pagamento','observacao',
                                 'dth_real']
        return(df_purchase_nf)



if __name__ == '__main__':    
    data_path = '../../data/'   
    
    df_purchase = pd.read_excel(data_path+'Compras Jan a Mar 2020 Lucas Natan.xlsx')  
    df_purchase_filtered = compras.run(df_purchase)
    df_purchase_garcom = garcomCompras.run(df_purchase_filtered)        
    df_purchase_nf =  purchaseNF.run(df_purchase_garcom) 
    
    df_purchase_saida = purchaseProcessado.run(df_purchase_nf)
