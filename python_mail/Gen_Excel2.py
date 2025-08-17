import pandas as pd
from datetime import datetime
import os
import xlsxwriter

file_name = "HRLOS_Summary.xlsx"  # แทนชื่อไฟล์ Excel ที่ต้องการอ่าน
file_path = "data/HRLOS_Summary.xlsx"
sheet_name = "SC1_jtl"


df = pd.read_excel(file_path, sheet_name=sheet_name)
print(df.dtypes)
print(df.head())

select_columns = ['Label','# Samples', 'Average','Error %', 'Min', 'Max', '95% Line', 'Throughput']
df = df[select_columns]
df = df.rename(columns = {'# Samples': 'Transaction'})

df['95% Line'] = df['95% Line'] / 1000 
df['95% Line'] = df['95% Line'].round(2)  # แปลงเป็นทศนิยม 2 ตำแหน่ง


print(df.shape)
df = df[df['Label'] != 'TOTAL']
#df = df.sort_values(by = '95% Line', ascending = False)
print(df.head())
print(df.info())
print(df.describe())

print(df.head())