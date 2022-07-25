import numpy as np
import matplotlib.pyplot as plt
import math
# fig = plt.figure(1)
# ax1 = plt.subplot(2,1,1)
# plt.plot([1,2,3])
# plt.show()
#
length = 38.0
width = 12.5
height_plate = 3.0
spacing_x=0.5
num_plies = 11
omega1=1.0
omega2=0.5
omega3=0.1
Firstphase1=1.57
Firstphase2=1.57
Firstphase3=1.57
# architecture
zarray1=[]
zarray2=[]
zarray3=[]
xarray=np.arange(spacing_x/2,length,0.01)
for i in range(len(xarray)):
	zvalue1=(height_plate/2)*math.sin(omega1*xarray[i]+Firstphase1) + (height_plate/2) #describing function
	zarray1.append(zvalue1)
	zvalue2=(height_plate/2)*math.sin(omega2*xarray[i]+Firstphase2) + (height_plate/2) #describing function
	zarray2.append(zvalue2)
	zvalue3=(height_plate/2)*math.sin(omega3*xarray[i]+Firstphase3) + (height_plate/2) #describing function
	zarray3.append(zvalue3)
plt.plot(xarray,zarray1)
plt.plot(xarray,zarray2)
plt.plot(xarray,zarray3)
'''
fig,ax =plt.subplots()
ax.plot()
ax.add_patch(pat.Rectangle((0,0),spacing_x,height_plate/num_plies,edgecolor='blue',facecolor='red',fill=True))
ax.add_patch(pat.Rectangle((spacing_x,0),spacing_x,height_plate/num_plies,edgecolor='blue',facecolor='red',fill=True))
'''
plt.show()