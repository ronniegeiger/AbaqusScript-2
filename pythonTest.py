import numpy as np
length = 38.0	
width = 12.5
height_plate = 3.0
spacing_y=0.5
spacing_x = 0.5
zarray=height_plate/2
xarray=np.arange(spacing_x/2,length,spacing_x)
yarray=np.arange(spacing_y/2,width,spacing_y)
Flag_1=spacing_x/2
Flag_2=spacing_x+spacing_x/2
Flag_3=2*spacing_x+spacing_x/2
Flag_4=3*spacing_x+spacing_x/2
T=4*spacing_x
CoordinateLocate=[]
for ycoordinate in range(len(yarray)):
	for xcoordinate in range(len(xarray)):
	    # print(xarray[xcoordinate]%T)
		# print(xarray[xcoordinate]%T == Flag_1 or xarray[xcoordinate]%T == Flag_3)
		if(xarray[xcoordinate]%T == Flag_1 or xarray[xcoordinate]%T == Flag_3):
			flag='Full'
		elif(xarray[xcoordinate]%T == Flag_2):
			flag='Bottom'
		elif(xarray[xcoordinate]%T == Flag_4):
			flag='Top'
		CoordinateLocate.append((xarray[xcoordinate],yarray[ycoordinate],zarray,flag))
for rr in range(len(xarray)):
    print(CoordinateLocate[rr])