import numpy as np
import math
'''
a=[1,8,3]
print(a)
a.sort()
print(a)

A=[2,4,5,6,7]
if 4 in A:
    print('4 is in')
if 3 not in A:
    print('3 is not in')
'''
# '''
length = 38.0
width = 12.5
height_plate = 3.0
length_plate=length*2
spacing_y=0.5
spacing_x = 0.5
num_DatumPlanes_y = int((width /spacing_y) -1.0)
num_DatumPlanes_x = int((length/spacing_x) -1.0)
num_plies = 10
ply=0
sectionpoint=3
#Describe function 
omega1=1.0
omega2=1.0
omega3=1.0
Firstphase1=1.57
Firstphase2=3.57
Firstphase3=5.57
# 
zarray1=[]
zarray2=[]
zarray3=[]
xarray=np.arange(spacing_x/2,length,spacing_x)
yarray=np.arange(spacing_y/2,width,spacing_y)
for i in range(len(xarray)):
	zvalue1=(height_plate/2)*math.sin(omega1*xarray[i]+Firstphase1) + (height_plate/2) #describing function
	zarray1.append(zvalue1)
	zvalue2=(height_plate/2)*math.sin(omega2*xarray[i]+Firstphase2) + (height_plate/2) #describing function
	zarray2.append(zvalue2)
	zvalue3=(height_plate/2)*math.sin(omega3*xarray[i]+Firstphase3) + (height_plate/2) #describing function
	zarray3.append(zvalue3)

# 
CoordinateLocate=[]
for ycoordinate in range(len(yarray)):
	for xcoordinate in range(len(xarray)):
		matrixplyarray=[]
		for num_ply in range(num_plies):
			if zarray1[xcoordinate] > ((height_plate/num_plies)*num_ply) and zarray1[xcoordinate] <= ((height_plate/num_plies)*(num_ply + 1)):
				matrixplyarray.append(num_ply+1)
			if zarray2[xcoordinate] > ((height_plate/num_plies)*num_ply) and zarray2[xcoordinate] <= ((height_plate/num_plies)*(num_ply + 1)):
				matrixplyarray.append(num_ply+1)
			if zarray3[xcoordinate] > ((height_plate/num_plies)*num_ply) and zarray3[xcoordinate] <= ((height_plate/num_plies)*(num_ply + 1)):
				matrixplyarray.append(num_ply+1)
		matrixplyarray=list(set(matrixplyarray)) # Remove duplicate elements from a list
		matrixplyarray.sort()
		CoordinateLocate.append((xarray[xcoordinate],yarray[ycoordinate],height_plate/2,matrixplyarray))
volumnfraction=0
Allvolumn=num_plies* len(CoordinateLocate)
for CoordinateLocatesequnce in range(len(CoordinateLocate)):
	volumnfraction=volumnfraction+len(CoordinateLocate[CoordinateLocatesequnce][3])
print(volumnfraction/Allvolumn)
# '''