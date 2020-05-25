# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:42:53 2020

@author: rodnv
"""

import pandas as pd
data_path = '../../data/'
from preprocessing import vendas as p
df = pd.read_excel(data_path+'VENDAS Jan a Mar 2020 Lucas Natan.xlsx')


# Excluding cpf/cnpj cells

df_filtered = p.filter_str(df,'CPF/CNPJ:', 'CPF/CNPJ:', na = False)
df_filtered = p.filter_str(df_filtered,'Tipo Operação', 'E', na = False)

cols = list(df_filtered)
df_filtered = p.excludeUnnamedCols(df_filtered, cols, 'Unnamed')
cols = list(df_filtered)

df_filtered = df_filtered.reset_index(drop=True)

cols = list(df_filtered)


t_f_n = list(df_filtered['Total Nota Fiscal'])
f_pgt = list(df_filtered['F.PGT'])
v_pgt = list(df_filtered['V.PGT'])
f_prazo = list(df_filtered['Prazo'])
v_prazo = list(df_filtered['V.Prazo'])
parcela = list(df_filtered['Parcelas'])

f_prazo = list(map(p.fill_nan_values,f_prazo,f_pgt))
df_filtered['Prazo'] = f_prazo.copy()

v_prazo = list(map(p.fill_nan_values,v_prazo,v_pgt))
df_filtered['V.Prazo'] = v_prazo.copy()

df_filtered['Forma a prazo'] = list(map(p.prazo,f_pgt,f_prazo))
df_filtered['Forma a vista'] = list(map(p.avista,f_pgt,f_prazo))
df_filtered['Valor a prazo'] = list(map(p.valor_prazo,df_filtered['Forma a prazo'],
                                        df_filtered['Forma a vista'],
                                        t_f_n,f_prazo,v_pgt,v_prazo))
