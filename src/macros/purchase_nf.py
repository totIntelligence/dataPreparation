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

class purchaseNF:
    
    def qtdParcelasLinha(forma_a_vista,forma_a_prazo,qtd_parcelas):
        if (forma_a_vista == 'A PRAZO') & (forma_a_prazo == 'SEM PRAZO'):
            return(int(qtd_parcelas) + 1)
        else:
            return(int(qtd_parcelas))

    def loja(cnpj):
        if str(cnpj) == '28.608.143/0001-08':
            return('Sede')
        elif str(cnpj) == '28608143000108':
            return('Del Rey')
        elif str(cnpj) == '27.809.544/0001-55':
            return('Cidade')
            
    
    def run(df_garcom):
        cnpjLoja = df_garcom['cnpj_loja'].copy()
        idDocumento = df_garcom['id_documento'].copy()
        dataEmissao = df_garcom['data_emissao'].copy()
        numeroNota = df_garcom['numero_nota'].copy()
        cpfCnpjCliente = df_garcom['cpf_cnpj_cliente'].copy()
        nomeCliente = df_garcom['nome_cliente'].copy()
        cepCliente = df_garcom['cep_cliente'].copy()
        valorNotaFiscal = df_garcom['valor_nota_fiscal'].copy()
        formaAPrazo = df_garcom['forma_a_prazo'].copy()
        valorAPrazo = df_garcom['valor_a_prazo'].copy()
        formaAVista = df_garcom['forma_a_vista'].copy()
        valorAVista = df_garcom['valor_a_vista'].copy()
        valorParcelas = df_garcom['valor_parcelas'].copy()
        qtdParcelas = df_garcom['qtd_parcelas'].copy()
        
        qtdParcelasLinha = list(map(purchaseNF.qtdParcelasLinha,formaAVista,formaAPrazo,qtdParcelas))
 
        
        notafiscal = []
        
        for i in range(0,len(cnpjLoja)):
            
            for j in range(qtdParcelasLinha[i]):
                
                if ((qtdParcelasLinha[i] > qtdParcelas.iloc[i]) | (qtdParcelas.iloc[i] == 1)) & (formaAPrazo.iloc[i] == 'SEM PRAZO'):
                    parcela = j
                else:
                    parcela = j + 1
            
                if parcela == 0:
                    valor_a_receber = valorAVista.iloc[i]
                else:
                    valor_a_receber = valorParcelas.iloc[i]
                
                qts_dias_prazo = (30*parcela) + 1
                
                data_previsao = datetime.datetime.strptime(dataEmissao.iloc[i], '%d/%m/%Y') + \
                                timedelta(days=qts_dias_prazo)
                
                if data_previsao.weekday() == 4: # 4 sexta
                    data_previsao = data_previsao + timedelta(days=3)
                elif data_previsao.weekday() == 5: # 4 sexta
                    data_previsao = data_previsao + timedelta(days=2)
                elif data_previsao.weekday() == 6: # 4 sexta
                    data_previsao = data_previsao + timedelta(days=1)
        
                    
                if (formaAVista.iloc[i] == 'DINHEIRO') | (formaAVista.iloc[i] == "DINHEIRO ( PENDENTE ACERTO)") & (parcela == 0):
                    data_previsao = datetime.datetime.strptime(dataEmissao.iloc[i], '%d/%m/%Y')
        
                notafiscal.append([cnpjLoja.iloc[i],
                                  idDocumento.iloc[i],
                                  dataEmissao.iloc[i],
                                  numeroNota.iloc[i],
                                  cpfCnpjCliente.iloc[i],
                                  nomeCliente.iloc[i],
                                  cepCliente.iloc[i],
                                  valorNotaFiscal.iloc[i],
                                  formaAPrazo.iloc[i],
                                  valorAPrazo.iloc[i],
                                  formaAVista.iloc[i],
                                  valorAVista.iloc[i],
                                  valor_a_receber,
                                  qtdParcelas.iloc[i],
                                  parcela,
                                  data_previsao])
        
        notafiscal = pd.DataFrame(notafiscal)

        notafiscal.columns = ['cnpjLoja',
                              'idDocumento',
                              'dataEmissao',
                              'numeroNota',
                              'cpfCnpjCliente',
                              'nomeCliente',
                              'cepCliente',
                              'valorNotaFiscal',
                              'formaAPrazo',
                              'valorAPrazo',
                              'formaAVista',
                              'valorAVista',
                              'valor_a_receber',
                              'qtdParcelas',
                              'parcela',
                              'data_previsao'
                              ]
        
        notafiscal['loja'] = list(map(purchaseNF.loja,notafiscal['cnpjLoja']))
        
        notafiscal = notafiscal[['loja',
                              'cnpjLoja',
                              'idDocumento',
                              'dataEmissao',
                              'numeroNota',
                              'cpfCnpjCliente',
                              'nomeCliente',
                              'cepCliente',
                              'valorNotaFiscal',
                              'formaAPrazo',
                              'valorAPrazo',
                              'formaAVista',
                              'valorAVista',
                              'valor_a_receber',
                              'qtdParcelas',
                              'parcela',
                              'data_previsao'
                              ]]
        return(notafiscal)

    
if __name__ == '__main__':
    
    data_path = '../../data/'
    df = pd.read_excel(data_path+'Compras Jan a Mar 2020 Lucas Natan.xlsx')
    df = compras.run(df)
    df_garcom = garcomCompras.run(df)       
 
    
    notaFiscal = purchaseNF.run(df_garcom)
    
    
    
    
    
    
    
    