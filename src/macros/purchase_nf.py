import pandas as pd
from purchase_preprocessing import *
from purchase_garcom import *

class comprasNF:
    
    def qtdParcelasLinha(forma_a_vista,forma_a_prazo,qtd_parcelas):
        if (forma_a_vista == 'A PRAZO') & (forma_a_prazo == 'SEM PRAZO'):
            return(qtd_parcelas + 1)
        else:
            return(qtd_parcelas)


if _name_ == '__main__':
    
    data_path = '../../data/'
    df = pd.read_excel(data_path+'Compras Jan a Mar 2020 Lucas Natan.xlsx')
    df = compras.run(df)
    df_garcom = garcomCompras.run(df)
    
    
 
    
    
    
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
    
    qtdParcelasLinha = list(map(comprasNF.qtdParcelasLinha,formaAVista,formaAPrazo,qtdParcelas))
    
    
    For indice = 0 To QTD_PARCELAS_LINHA
    
    If (QTD_PARCELAS_LINHA > QTD_PARCELAS) Or (QTD_PARCELAS = 1 And FORMA_A_PRAZO = "SEM PRAZO") Then
    PARCELA = indice
    Else
    PARCELA = indice + 1
    End If
    
    If PARCELA = 0 Then
    VALOR_A_RECEBER = VALOR_A_VISTA
    Else
    VALOR_A_RECEBER = VALOR_PARCELAS
    End If
    
    QTD_DIAS_PRAZO = (30 * PARCELA) + 1
    
    DATA_PREVISAO = DateAdd("d", QTD_DIAS_PRAZO, DATA_EMISSAO)
    
    If Weekday(DATA_PREVISAO) = 6 Then
    DATA_PREVISAO = DateAdd("d", 3, DATA_PREVISAO)
    ElseIf Weekday(DATA_PREVISAO) = 7 Then
    DATA_PREVISAO = DateAdd("d", 2, DATA_PREVISAO)
    Else
    DATA_PREVISAO = DATA_PREVISAO
    End If
    
    If (FORMA_A_VISTA = "DINHEIRO" Or FORMA_A_VISTA = "DINHEIRO ( PENDENTE ACERTO)") And PARCELA = 0 Then
    DATA_PREVISAO = DateAdd("d", 0, DATA_EMISSAO)
    Else
    DATA_PREVISAO = DATA_PREVISAO
    End If
    
    
    'Preenche colunas da tabela
    
    Worksheets("Compras_NF").Cells(Linha + indice, 2).Value = CNPJ_LOJA
    Worksheets("Compras_NF").Cells(Linha + indice, 3).Value = ID_DOCUMENTO
    Worksheets("Compras_NF").Cells(Linha + indice, 4).Value = DATA_EMISSAO
    Worksheets("Compras_NF").Cells(Linha + indice, 5).Value = NUMERO_NOTA
    Worksheets("Compras_NF").Cells(Linha + indice, 6).Value = CPF_CNPJ_CLIENTE
    Worksheets("Compras_NF").Cells(Linha + indice, 7).Value = NOME_CLIENTE
    Worksheets("Compras_NF").Cells(Linha + indice, 8).Value = CEP_CLIENTE
    Worksheets("Compras_NF").Cells(Linha + indice, 9).Value = VALOR_NOTA_FISCAL
    Worksheets("Compras_NF").Cells(Linha + indice, 10).Value = FORMA_A_PRAZO
    Worksheets("Compras_NF").Cells(Linha + indice, 11).Value = VALOR_A_PRAZO
    Worksheets("Compras_NF").Cells(Linha + indice, 12).Value = FORMA_A_VISTA
    Worksheets("Compras_NF").Cells(Linha + indice, 13).Value = VALOR_A_VISTA
    Worksheets("Compras_NF").Cells(Linha + indice, 14).Value = VALOR_A_RECEBER
    Worksheets("Compras_NF").Cells(Linha + indice, 15).Value = QTD_PARCELAS
    Worksheets("Compras_NF").Cells(Linha + indice, 16).Value = PARCELA
    Worksheets("Compras_NF").Cells(Linha + indice, 17).Value = DATA_PREVISAO

    
    

   
   If Worksheets("Compras_NF").Cells(Linha + indice, 2).Value = "28.608.143/0001-08" Then
   Worksheets("Compras_NF").Cells(Linha + indice, 1).Value = "Sede"
   ElseIf Worksheets("Compras_NF").Cells(Linha + indice, 2).Value = "28608143000108" Then
   Worksheets("Compras_NF").Cells(Linha + indice, 1).Value = "Del Rey"
   ElseIf Worksheets("Compras_NF").Cells(Linha + indice, 2).Value = "27.809.544/0001-55" Then
   Worksheets("Compras_NF").Cells(Linha + indice, 1).Value = "Cidade"
   End If
   
   
    Next indice    
    
    
    