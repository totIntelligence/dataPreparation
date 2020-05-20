# -*- coding: utf-8 -*-
"""
Objective: Module responsible for cleaning and prepare the purchase's input for LojaDoSapo
Created on Wed May 20 18:27:06 2020
@author: hmilagres
"""

import pandas as pd
data_path = '../../data/'
from preprocessing import preprocessing as p
df = pd.read_excel(data_path+'Compras Jan a Mar 2020 Lucas Natan.xlsx')


# Excluding cpf/cnpj cells

df_filtered = p.filter_str(df,'CPF/CNPJ:', 'CPF/CNPJ:', na = False)
df_filtered = p.filter_str(df_filtered,'Tipo Operação', 'E', na = False)
df_filtered = p.filter_str(df_filtered,'Tipo Operação', 'S', na = False)

cols = list(df_filtered)
df_filtered = p.excludeUnnamedCols(df_filtered, cols, 'Unnamed')
cols = list(df_filtered)

df_filtered = df_filtered.reset_index(drop=True)

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


