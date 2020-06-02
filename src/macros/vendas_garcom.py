# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 18:22:53 2020

@author: rodnv
"""

from vendas_preprocessing import vendas
import pandas as pd

class garcomVendas:
    
    def create_idx(Doc,cnpj,emissao,codCliente):
        return(str(Doc)+'-'+str(cnpj)+'-'+\
               str(emissao)+'-'+str(codCliente))
    
    def defParcela(formaPrazo,parcelas):
        if formaPrazo == 'SEM PRAZO':
            return(1)
        else:
            return(parcelas)

    
    def run(df):
        dfGarcom = pd.DataFrame({
                    'cnpj_loja': df.iloc[:,0].copy(),
                    'id_doc_client': list(map(garcomVendas.create_idx,df['Documento:'],df['CPF/CNPJ:'],
                                         df['Emissão:'],df['Cod. Cliente/Fornecedor:'])),
                    'id_documento': df['Documento:'].copy(),
                    'data_emissao': df['Emissão:'].copy(),
                    'cpf_cnpj_cliente': df['Cod. Cliente/Fornecedor:'].copy(),
                    'nome_cliente': df['Cliente/Fornecedor:'].copy(),
                    'cep_cliente': df['UF'].copy(),
                    'valor_nota_fiscal': df['Total Nota Fiscal'].copy(),
                    'forma_a_prazo': df['Forma a prazo'].copy(),
                    'valor_a_prazo': df['Valor a prazo'].copy(),
                    'forma_a_vista': df['Forma a vista'].copy(),
                    'valor_a_vista': df['Valor a vista'].copy(),
                    'valor_parcelas': df['Valor Parcela'].copy(),
                    'qtd_parcelas': list(map(garcomVendas.defParcela,df['Forma a prazo'].copy(),df['Parcela'])) 
                    })
        dfGarcom = dfGarcom.drop_duplicates()
        return(dfGarcom)
        
if __name__ == '__main__':

    data_path = '../../data/'
    df = pd.read_excel(data_path+'VENDAS Jan a Mar 2020 Lucas Natan.xlsx')
    df = vendas.run(df)
    dfGarcom = garcomVendas.run(df)
    