'''
# copy & deep copy
# create 2 dimension tuple, the different of [0]*n & [0 for _ in range(n)]
n = 4
dp1= [0]*n
dp2=[0 for _ in range(n)]
print(dp2)
# create a 3*4 matrix, replace element (0,2) with 3,provide  approches as follow:
m,n = 3,4
dp2_1=[[0]*n]*m
dp2_2=[[0 for _ in range(n)] for _ in range(m)]
dp2_3=[[0]*n for _ in range(m)]
dp2_1[0][2]=3
dp2_2[0][2]=3
dp2_3[0][2]=3
print('dp2_1:',dp2_1)
print('dp2_2:',dp2_2)
print('dp2_3:',dp2_3)
# Results as follow:
# dp2_1: [[0, 0, 3, 0], [0, 0, 3, 0], [0, 0, 3, 0]]
# dp2_2: [[0, 0, 3, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
# dp2_3: [[0, 0, 3, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
# The results show that row 1(dp2_1) failed, because change one element cause the all rows change.
# The method 2 & 3 all are available.
# Summary: [0] * n is copy(eg.repeat a list n times, is '=' copy); [[0]* n] *m repeat '[0]*n' with n times.
# 		   [0 for _ in range(n)] is createing, "DeepCopy".
'''
'''
import numpy as np
import math
from textRepr import *
length = 38.0	
width = 12.5
height_plate = 3.0
spacing_y=0.5
spacing_x = 0.5
num_plies = 11
omega=1.0
Firstphase_1=1.57
Firstphase_2=3.0
zarray_1=[]
zarray_2=[]
zarray=[]
xarray=np.arange(spacing_x/2,length,spacing_x)
yarray=np.arange(spacing_y/2,width,spacing_y)
for i in range(len(xarray)):
	zvalue1=(height_plate/2)*math.sin(omega*xarray[i]+Firstphase_1) + (height_plate/2)#describing function
	zvalue2=(height_plate/2)*math.sin(omega*xarray[i]+Firstphase_2) + (height_plate/2)#describing function
	zarray_1.append(zvalue1)
	zarray_2.append(zvalue2)
Ply=[[0 for _ in range(num_plies)] for _ in range(len(xarray)*len(yarray))]
CoordinateLocate=[]
for ycoordinate in range(len(yarray)):
	for xcoordinate in range(len(xarray)):
		region_num = (ycoordinate * len(xarray)) + xcoordinate
		for num_ply in range(num_plies):
			if (zarray_1[xcoordinate] > ((height_plate/num_plies)*num_ply) and zarray_1[xcoordinate] <= ((height_plate/num_plies)*(num_ply + 1))) or (zarray_2[xcoordinate] > ((height_plate/num_plies)*num_ply) and zarray_2[xcoordinate] <= ((height_plate/num_plies)*(num_ply + 1))):
				Ply[region_num][num_ply]=1
			else:
				continue
		CoordinateLocate.append((xarray[xcoordinate],yarray[ycoordinate],height_plate/2))
prettyPrint(Ply)
'''
'''
import numpy as np
num_plies = 11
length = 38.0
width = 12.5
height_plate = 3.0
spacing_y=0.5
spacing_x = 0.5
xarray=np.arange(spacing_x/2,length,spacing_x)
yarray=np.arange(spacing_y/2,width,spacing_y)
Ply=[[0 for _ in range(num_plies)] for _ in range(len(xarray)*len(yarray))]
Ply[0][1]=1
Ply[0][2]=1
print(Ply[0])
'''
# '''

# '''