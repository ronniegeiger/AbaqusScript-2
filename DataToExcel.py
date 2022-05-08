import openpyxl
import string
file_name = 'Data.txt'
with open(file_name,'r') as DA:
    Data=DA.read().strip()
# Pkeys=str.split(Data[0],' ')
# print(Pkeys)
print(Data[1])