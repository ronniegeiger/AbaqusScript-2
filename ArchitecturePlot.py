import matplotlib.pyplot as plt
import matplotlib.patches as pat
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
fig,ax =plt.subplots()
ax.plot()
ax.add_patch(pat.Rectangle((0,0),spacing_x,height_plate/num_plies,edgecolor='blue',facecolor='red',fill=True))
ax.add_patch(pat.Rectangle((spacing_x,0),spacing_x,height_plate/num_plies,edgecolor='blue',facecolor='red',fill=True))
plt.show()