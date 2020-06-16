# -*- coding: utf-8 -*-
from vendas_preprocessing import vendas
from vendas_garcom import garcomVendas
from vendas_notaFiscal import vendasNF 
import math

from datetime import date  

import pandas as pd

class vendasProcessado:
    
    def criaStatus(forma_a_vista,data_previsao):
        if (forma_a_vista == 'DINHEIRO (PENDENTE ACERTO)'):
            return ('Não Recebido')
        else:
            if data_previsao < date.today():
                return 'Recebido'
            else:
                return 'A Receber'

    def formaPagamento(formaAPrazo,valorAPrazo,formaAVista,valorAVista):
        if (valorAPrazo > valorAVista):
            return formaAPrazo
        else:
            return formaAVista

    def run(df):
        forma_a_prazo = list(df['formaAPrazo'])
        valor_a_prazo = list(df['valorAPrazo'])        
        forma_a_vista = list(df['formaAVista'])        
        valor_a_vista = list(df['valorAVista'])  
        df_saida = pd.DataFrame({
                    'pdv': df['loja'],
                    'fatura': len(df)*[math.nan] ,
                    'id_documento_sistema': df['idDocumento'],
                    'dth_emissao': df['dataEmissao'],                    
                    'id_cliente_fornecedor': df['cpfCnpjCliente'],                    
                    'nome_cliente': df['nomeCliente'],
                    'cep_cliente': df['cepCliente'],
                    'valor': df['valor_a_receber'],                    
                    'qtd_parcelas': df['qtdParcelas'],                    
                    'parcela': df['parcela'],
                    'dth_previsto': df['data_previsao'],       
                    'status': list(map(vendasProcessado.criaStatus,forma_a_vista,df['data_previsao'])),
                    'tipo_documento': len(df)*['Vendas'] ,                    
                    'natureza': len(df)*['Recebimentos'] ,
                    'forma_pagamento':  list(map(vendasProcessado.formaPagamento,forma_a_prazo,valor_a_prazo,forma_a_vista,valor_a_vista)),
                    'observacao': len(df)*[math.nan],                   
                    'dth_real': len(df)*[math.nan] 
                    }) 
        return(df_saida)





if __name__ == '__main__':    
    data_path = '../../data/'   
    
    df_vendas = pd.read_excel(data_path+'VENDAS Jan a Mar 2020 Lucas Natan.xlsx')  
    df_vendas_filtered = vendas.run(df_vendas)
    df_vendas_garcom = garcomVendas.run(df_vendas_filtered)        
    df_vendas_nf =  vendasNF.run(df_vendas_garcom) 
    
    df_vendas_saida = vendasProcessado.run(df_vendas_nf)
#----------------------------    
 
 