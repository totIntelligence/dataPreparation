# -*- coding: utf-8 -*-
from purchase_preprocessing import compras 
import pandas as pd


class garcomCompras:
    
    def create_idx(Doc,user,emissao,codCliente):
        return(str(Doc)+'-'+str(user)+'-'+\
               str(emissao)+'-'+str(codCliente))
    def defParcela(formaPrazo,parcelas):
        if formaPrazo == "SEM PRAZO":
            return 1
        else:
            return(parcelas)
    def run(df):  
        return pd.DataFrame({
        'cnpj_loja': df['CPF/CNPJ:'].copy(),
        'id_doc_client': list(map(garcomCompras.create_idx,df['Documento:'],df['CPF/CNPJ:'],df['Emissão:'],df['Cod. Cliente/Fornecedor:'])) ,
        'id_documento': df['Documento:'].copy(),
        'data_emissao': df['Emissão:'].copy(),
        'numero_nota': df['Chave.NFe'].copy(),
        'cpf_cnpj_cliente': df['Cod. Cliente/Fornecedor:'].copy(),
        'nome_cliente': df['Cliente/Fornecedor:'].copy(),
        'cep_cliente': df['UF'].copy(),
        'valor_nota_fiscal': df['Total Nota Fiscal'].copy(),    
        'forma_a_prazo': df['Forma a prazo'].copy(),    
        'valor_a_prazo': df['Valor a prazo'].copy(),
        'forma_a_vista': df['Forma a vista'].copy(),
        'valor_a_vista': df['Valor a vista'].copy(),  
        'valor_parcelas': df['Valor Parcela'].copy(),        
        'qtd_parcelas':    list(map(garcomCompras.defParcela,df['Forma a prazo'].copy(),df['Parcelas']))
        })
         
 
if __name__ == '__main__':
    data_path = '../../data/'
    df = pd.read_excel(data_path+'Compras Jan a Mar 2020 Lucas Natan.xlsx')
    df = compras.run(df)    
    df_garcom = garcomCompras.run(df)       
    df_garcom.drop_duplicates()     
    

