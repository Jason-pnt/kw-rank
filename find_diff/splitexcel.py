# -*- coding: utf-8 -*-
import xlrd
import pandas as pd

data = xlrd.open_workbook('test.xlsx')
data.sheet_names()
ASIN = ''.join(data.sheet_names())

table = data.sheet_by_index(0)
col1 = (table.col_values(0))

for i in range(len(col1)):
    col1[i] = str(col1[i]).strip()

num = 0
for i in range(len(col1)):
    if num ==0:
        begin = i
    num = num + 1
    if (num % 100 == 0):
        end = i
        num = 0
        tmp_list = col1[begin:end+1]
        df = pd.DataFrame(tmp_list)
        savename= ASIN + '-'+ str(begin+1) + '-' + str(end+1)+'.xlsx'
        df.to_excel(savename,index=False, sheet_name=ASIN,header=False)
    