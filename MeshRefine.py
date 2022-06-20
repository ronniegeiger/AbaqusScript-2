#!/user/bin/python
# -* - coding:UTF-8 -*-
from abaqus import *
from abaqusConstants import *
from textRepr import *
import mesh
import time
import odbAccess
from odbAccess import *
import visualization
import regionToolset
import numpy as np
import os
## initial variables
length = 38.0
width = 12.5
height_plate = 3.0
spacing_y=0.5
spacing_x = 0.5

PartPlate=mdb.models['Model-1'].parts['Part-plate']
# 
cy=PartPlate.cells
edge=PartPlate.edges
vertice=PartPlate.vertices
face=PartPlate.faces
da=PartPlate.datums
# 
Meshxarray=np.arange(spacing_x/2,length,spacing_x)
Meshyarray=np.arange(spacing_y/2,width,spacing_y)
MeshCoordinateLocate=[]
for ycoordinate in range(len(Meshyarray)):
	for xcoordinate in range(len(Meshxarray)):
		MeshCoordinateLocate.append((Meshxarray[xcoordinate],Meshyarray[ycoordinate],height_plate/2))
for temp_y in range(len(Meshyarray)):
	for temp_x in range(len(Meshxarray)):
		temp_n = (temp_y * len(Meshxarray)) + temp_x
		cells_part=PartPlate.cells.findAt(((MeshCoordinateLocate[temp_n][0], MeshCoordinateLocate[temp_n][1],height_plate/2),),)
		face_part=PartPlate.faces.findAt(((MeshCoordinateLocate[temp_n][0], MeshCoordinateLocate[temp_n][1],height_plate),),)
		edge_part=PartPlate.edges.findAt(((MeshCoordinateLocate[temp_n][0]-spacing_x/2,MeshCoordinateLocate[temp_n][1]-spacing_y/2,height_plate/2),),)
		region=regionToolset.Region(cells=cells_part)
		PartPlate.setMeshControls(regions=cy, technique=STRUCTURED, algorithm=ADVANCING_FRONT)
		for FaceNum in cy[temp_n].getFaces():
			FaceZvalue=face[FaceNum].pointOn[0][2]
			if FaceZvalue == height_plate:
				PartPlate.assignStackDirection(referenceRegion=face[FaceNum], cells=cells_part)
				continue
		# for EdgeNum in cy[temp_n].getEdges():
		# 	EdgeZvalue=edge[EdgeNum].pointOn[0][2]
		# 	if EdgeZvalue < height_plate and EdgeZvalue > 0.0:
		# 		PartPlate.setSweepPath(region=cy[temp_n], edge=edge[EdgeNum], sense=FORWARD)
		# 		continue
PartPlate.generateMesh()