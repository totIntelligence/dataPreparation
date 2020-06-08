# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 18:06:50 2020

@author: rodnv
"""

import pandas as pd
from vendas_preprocessing import *
from vendas_garcom import *
import datetime
from datetime import timedelta 
import calendar 

class vendasNF:
    
    def qtdParcelasLinha(forma_a_vista,forma_a_prazo,qtd_parcelas):
        if (forma_a_vista == 'A PRAZO') & (forma_a_prazo == 'SEM PRAZO'):
            return(qtd_parcelas + 1)
        else:
            return(qtd_parcelas)

    def loja(cnpj):
        if str(cnpj) == '28.608.143/0001-08':
            return('Sede')
        elif str(cnpj) == '28608143000108':
            return('Del Rey')
        elif str(cnpj) == '27.809.544/0001-55':
            return('Cidade')
            
    
    def run(dfGarcom):
        cnpjLoja = dfGarcom['cnpj_loja'].copy()
        idDocumento = dfGarcom['id_documento'].copy()
        dataEmissao = dfGarcom['data_emissao'].copy()
        cpfCnpjCliente = dfGarcom['cpf_cnpj_cliente'].copy()
        nomeCliente = dfGarcom['nome_cliente'].copy()
        cepCliente = dfGarcom['cep_cliente'].copy()
        valorNotaFiscal = dfGarcom['valor_nota_fiscal'].copy()
        formaAPrazo = dfGarcom['forma_a_prazo'].copy()
        valorAPrazo = dfGarcom['valor_a_prazo'].copy()
        formaAVista = dfGarcom['forma_a_vista'].copy()
        valorAVista = dfGarcom['valor_a_vista'].copy()
        valorParcelas = dfGarcom['valor_parcelas'].copy()
        qtdParcelas = dfGarcom['qtd_parcelas'].copy()
        
        qtdParcelasLinha = list(map(vendasNF.qtdParcelasLinha,formaAVista,formaAPrazo,qtdParcelas))
        
        
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
        
        notafiscal['loja'] = list(map(vendasNF.loja,notafiscal['cnpjLoja']))
        
        notafiscal = notafiscal[['loja',
                              'cnpjLoja',
                              'idDocumento',
                              'dataEmissao',
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
    df = pd.read_excel(data_path+'VENDAS Jan a Mar 2020 Lucas Natan.xlsx')
    df = vendas.run(df)
    dfGarcom = garcomVendas.run(df)
    dfGarcom = dfGarcom.reset_index(drop = True)
    
    notaFiscal = vendasNF.run(dfGarcom)
    
    
    
    
    
    
    
    