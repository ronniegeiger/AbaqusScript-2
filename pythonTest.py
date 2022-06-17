'''
import numpy as np
length = 38.0	
width = 12.5
height_plate = 3.0
spacing_y=0.5
spacing_x = 0.5
num_DatumPlanes_y = int((width /spacing_y) -1.0)
num_DatumPlanes_x = int((length/spacing_x) -1.0)
num_plies = 11
zarray=height_plate/2
xarray=np.arange(spacing_x/2,length,spacing_x)
yarray=np.arange(spacing_y/2,width,spacing_y)

T=11*spacing_x
CoordinateLocate=[]
# for ycoordinate in range(len(yarray)):
for xcoordinate in range(len(xarray)):
	print((((xarray[xcoordinate]%T)-0.25)/spacing_x)+1)
		# print(xarray[xcoordinate]%T == Flag_1 or xarray[xcoordinate]%T == Flag_3)
'''
# '''
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
# '''