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
import random
# -------------------------------------------
# This Model is built with 3 plies in single region, generating by random module of python, and
# caculating by while sentence.
# -------------------------------------------
## initial variables
length = 38.0# Half of actual plate length
length_plate=length*2
width = 12.5
height_plate = 3.0
spacing_y=0.5
spacing_x = 0.5
num_DatumPlanes_y = int((width /spacing_y) -1.0)
num_DatumPlanes_x = int((length/spacing_x) -1.0)
num_plies = 10
ply=0
matrixplies=3#Matrix plies number in single region
sectionpoint=3
VolumnFraction=0.03 #30%

#Declare material
ReinforceMaterial = 'CompositeLaminates'
MatrixMaterial = 'AluminumAlloy_6061'
#Assembly
DependentState=ON
InstanceName='Part-plate-1'
#Step
StaticStepName='Step-1'
PreviousStepName='Initial'
MaxNumInc=10000
InitialInc=0.01
MinInc=1e-09
MaxInc=0.1
#Seed Control
seedNumber=1
seedConstraint=FIXED
#postprocessing
odbfilename = 'Job-1.odb'
CrossSectionalArea= width * height_plate
# Load
# The engineering strain is required to be 3%
xDis=0.03 * length
# Create model
if mdb.models.has_key("Model-1"):
    myModel = mdb.models["Model-1"]
else:
    myModel = mdb.Model(name="Model-1",modelType=STANDARD_EXPLICIT)
# create sketch 1
SketchPlate = myModel.ConstrainedSketch(name='sketch-plate',sheetSize=200)
SketchPlate.rectangle(point1=(0,0), point2=(length, width))
PartPlate = myModel.Part(name = "Part-plate", dimensionality=THREE_D, type=DEFORMABLE_BODY)
PartPlate.BaseSolidExtrude(sketch=SketchPlate, depth=height_plate)
# The actual index number of part
cy=PartPlate.cells
edge=PartPlate.edges
vertice=PartPlate.vertices
face=PartPlate.faces
da=PartPlate.datums
# Create Datum planes
for num_DatumPlane_y in range(num_DatumPlanes_y):
	yOffsetValue = (num_DatumPlane_y + 1) * spacing_y
	pointOnY = (18,yOffsetValue,height_plate/2)
	PartPlate.DatumPlaneByPointNormal(point=pointOnY, normal=edge[2])
for num_DatumPlane_x in range(num_DatumPlanes_x):
	xOffsetValue = (num_DatumPlane_x + 1) * spacing_x
	pointOnX = (xOffsetValue,6.25,height_plate/2)
	PartPlate.DatumPlaneByPointNormal(point=pointOnX, normal=edge[11])
# Partition Cells
'''
for i in range(len(da)):
	num = i+2
	PartPlate.PartitionCellByDatumPlane(datumPlane=da[num], cells=cy)
# 
'''
RegionNumber=len(cy) # 1900
V_Plate=width*height_plate*length
V_singleA=matrixplies*spacing_x*spacing_y*(height_plate/num_plies) #Matrix plies volumn in single region
V_a=VolumnFraction*V_Plate
HoleNumber=V_a/V_singleA# a means architecture
# print(HoleNumber)
# Import material property form lib of materials
from material import createMaterialFromDataString
createMaterialFromDataString('Model-1', 'CompositeLaminates', '2019', 
        """{'materialIdentifier': '', 'description': '', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((162000.0, 14900.0, 14900.0, 0.283, 0.283, 0.386, 5.7, 5.7, 5.4),), 'type': ENGINEERING_CONSTANTS}, 'name': 'CompositeLaminates'}""")
createMaterialFromDataString('Model-1', 'AluminumAlloy_6061', '2019',"""{'name': 'AluminumAlloy_6061', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((70000.0, 0.35),), 'type': ISOTROPIC}, 'density': {'temperatureDependency': OFF, 'table': ((2.7e-06,),), 'dependencies': 0, 'fieldName': '', 'distributionType': UNIFORM}, 'materialIdentifier': '', 'description': ''}""")
# Create Datum csys
v_origin = (0.0, 0.0, 0.0)
v_xaxis = (length, 0.0, 0.0)
v_yaxis = (length, width, 0.0)
PartPlate.DatumCsysByThreePoints(origin=v_origin, point1=v_xaxis, point2=v_yaxis,name='Datum csys-2', coordSysType=CARTESIAN)
#
layupOrientation = None
#Coordinate computation of x,y and z
zarray=[]
xarray=np.arange(spacing_x/2,length,spacing_x)
yarray=np.arange(spacing_y/2,width,spacing_y)
#Combine the tri-axis coordinates
CoordinateLocate=[]
for ycoordinate in range(len(yarray)):
	for xcoordinate in range(len(xarray)):
		CoordinateLocate.append([xarray[xcoordinate],yarray[ycoordinate],0])
CoordinateNumber=list(range(len(CoordinateLocate)))
HoleRegions=random.sample(CoordinateNumber,int(HoleNumber))
HoleRegions.sort() #Sort the list
for holeregion in HoleRegions:
	CoordinateLocate[holeregion][2]=1
# for Coordinatelocation in CoordinateLocate:
# 	prettyPrint(Coordinatelocation)

#CompositeLayup Predefine
compositeLayup = PartPlate.CompositeLayup(name='CompositeLayup-1', description='', elementType=SOLID,
        symmetric=False)
compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON,
        poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT,
        useDensity=OFF)
compositeLayup.ReferenceOrientation(orientationType=GLOBAL, localCsys=None,
        fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0,
        axis=AXIS_3, stackDirection=STACK_3)
