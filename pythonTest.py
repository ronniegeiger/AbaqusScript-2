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
