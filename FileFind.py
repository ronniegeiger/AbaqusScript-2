from logging import root
import os
import datetime
path= os.getcwd()
filename='Job-1.txt'

'''
for root,dirs,files in os.walk(path):
    for file in files:
        if filename in file:
            print('find')
            continue
        else:
            print("Don't")
'''

'''
for root,directorys,files in os.walk(,path):
    for file in files:
        while(file==filename):
            print(datetime.date)
'''
# print(os.listdir())
for i in os.listdir():
    while(i==filename):
        print(i)
        break
print("1+1=2")