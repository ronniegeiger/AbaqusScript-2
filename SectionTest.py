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

## initial variables
length = 38.0	
width = 12.5
height_plate = 3.0
MidHeight=height_plate/2
spacing_y=0.5
spacing_x = 0.5
num_DatumPlanes_y = int((width /spacing_y) -1.0)
num_DatumPlanes_x = int((length/spacing_x) -1.0)
num_plies = 11 # The quantity of plies
ply=0 
sectionpoint=3
# The describing function of architecture
omega=1.0
Firstphase=1.57
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
e=PartPlate.edges
da=PartPlate.datums
# Create Datum planes
for num_DatumPlane_y in range(num_DatumPlanes_y):
	yOffsetValue = (num_DatumPlane_y + 1) * spacing_y
	pointOnY = (18,yOffsetValue,height_plate/2)
	PartPlate.DatumPlaneByPointNormal(point=pointOnY, normal=e[2])
for num_DatumPlane_x in range(num_DatumPlanes_x):
	xOffsetValue = (num_DatumPlane_x + 1) * spacing_x
	pointOnX = (xOffsetValue,6.25,height_plate/2)
	PartPlate.DatumPlaneByPointNormal(point=pointOnX, normal=e[11])
# Partition Cells
cy=PartPlate.cells
for i in range(len(da)):
	num = i+2
	PartPlate.PartitionCellByDatumPlane(datumPlane=da[num], cells=cy)
# Display the view of PartPlate in Front
session.viewports['Viewport: 1'].setValues(displayedObject = PartPlate)
session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(datumPlanes=OFF)
# Highlight cy[n] to indicate the sequence of cells
#for i in range(len(cy)):
#	highlight(cy[i])
#	time.sleep(0.01)
#	unhighlight(cy[i])
# Import material property form lib of materials
from material import createMaterialFromDataString
createMaterialFromDataString('Model-1', 'CompositeLaminates', '2019', 
        """{'materialIdentifier': '', 'description': '', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((162000.0, 14900.0, 14900.0, 0.283, 0.283, 0.386, 5.7, 5.7, 5.4),), 'type': ENGINEERING_CONSTANTS}, 'name': 'CompositeLaminates'}""")
createMaterialFromDataString('Model-1', 'AluminumAlloy_6061', '2019',"""{'name': 'AluminumAlloy_6061', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((70000.0, 0.35),), 'type': ISOTROPIC}, 'density': {'temperatureDependency': OFF, 'table': ((2.7e-06,),), 'dependencies': 0, 'fieldName': '', 'distributionType': UNIFORM}, 'plastic': {'temperatureDependency': OFF, 'strainRangeDependency': OFF, 'rate': OFF, 'dependencies': 0, 'hardening': ISOTROPIC, 'dataType': HALF_CYCLE, 'table': ((200.0, 0.0), (246.0, 0.0235), (294.0, 0.0474), (374.0, 0.0935), (437.0, 0.1377), (480.0, 0.18)), 'numBackstresses': 1}, 'materialIdentifier': '', 'description': ''}""")
#
layupOrientation = None
#cells1 = PartPlate.cells.findAt(((5.5, 8.3, 1.5),),)
#Assign Material Property
#Region=[]
#for num_x in range(10):
#	for num_y in range(10):
#		region='X{num_X}Y{num_Y}'.format(num_X=num_x,num_Y=num_y)
#		Region.append(region)

#Coordinate computation of x,y and z
zarray=[]
xarray=np.arange(spacing_x/2,length,spacing_x)
yarray=np.arange(spacing_y/2,width,spacing_y)
for i in range(len(xarray)):
	zvalue=(height_plate/2)*sin(omega*xarray[i]+Firstphase) + (height_plate/2)#describing function
	zarray.append(zvalue)
#Combine the tri-axis coordinates
CoordinateLocate=[]
for ycoordinate in range(len(yarray)):
	for xcoordinate in range(len(xarray)):
		for num_ply in range(num_plies):
			if zarray[xcoordinate] > ((height_plate/num_plies)*num_ply) and zarray[xcoordinate] <= ((height_plate/num_plies)*(num_ply + 1)):
				ply= num_ply + 1
			else:
				continue
		CoordinateLocate.append((xarray[xcoordinate],yarray[ycoordinate],zarray[xcoordinate],ply)) 
#CompositeLayup Predefine
compositeLayup = PartPlate.CompositeLayup(name='CompositeLayup-1', description='', elementType=CONTINUUM_SHELL, 
        symmetric=False)
compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON, 
        poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
        useDensity=OFF)
compositeLayup.ReferenceOrientation(orientationType=GLOBAL, localCsys=None, 
        fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0, 
        axis=AXIS_3, stackDirection=STACK_3)
#Project architecture to section layers
'''
for temp_y in range(len(yarray)):
	for temp_x in range(len(xarray)):
		temp_n = (temp_y * len(xarray)) + temp_x
		cells_part=PartPlate.cells.findAt(((CoordinateLocate[temp_n][0], CoordinateLocate[temp_n][1],height_plate/2),),)
		region=regionToolset.Region(cells=cells_part)
		for num_ply in range(num_plies):
			if (num_ply+1) == CoordinateLocate[temp_n][3]:
				compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format((num_plies * temp_n) + num_ply + 1), region=region, material=MatrixMaterial, thicknessType=SPECIFY_THICKNESS, 
				thickness=0.1, orientationType=ANGLE_0, additionalRotationType=ROTATION_NONE, additionalRotationField='', 
				axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
			else:
				compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format((num_plies * temp_n) + num_ply + 1), region=region, material=ReinforceMaterial, thicknessType=SPECIFY_THICKNESS, 
				thickness=0.1, orientationType=ANGLE_0, additionalRotationType=ROTATION_NONE, additionalRotationField='', 
				axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
'''
# '''
a=time.time()
temp_allY=len(yarray)
temp_allX=len(xarray)
for temp_y in range(2):
	for temp_x in range(temp_allX):
		temp_n = (temp_y * temp_allX) + temp_x
		cells_part=PartPlate.cells.findAt(((CoordinateLocate[temp_n][0], CoordinateLocate[temp_n][1],MidHeight),),)
		region=regionToolset.Region(cells=cells_part)
		for num_ply in range(num_plies):
			nam_ply=(num_plies*temp_n)+num_ply+1
			if (num_ply+1) == CoordinateLocate[temp_n][3]:
				compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format(nam_ply), region=region, material=MatrixMaterial,thicknessType=SPECIFY_THICKNESS,thickness=0.1, orientationType=ANGLE_0,axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
			else:
				compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format(nam_ply), region=region, material=ReinforceMaterial,thicknessType=SPECIFY_THICKNESS,thickness=0.1, orientationType=ANGLE_0,axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
print(time.time()-a)
# '''
# 3 rows 733s
# Time after add temporary variable: 5.5s
'''
a=time.time()
for temp_y in range(2):
	for temp_x in range(len(xarray)):
		temp_n = (temp_y * len(xarray)) + temp_x
		cells_part=PartPlate.cells.findAt(((CoordinateLocate[temp_n][0], CoordinateLocate[temp_n][1],height_plate/2),),)
		region=regionToolset.Region(cells=cells_part)
		for num_ply in range(num_plies):
		    nam_ply=(num_plies*temp_n)+num_ply+1
			if (num_ply+1)==CoordinateLocate[temp_n][3]:
			    compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format(nam_ply), region=region, material=MatrixMaterial,thicknessType=SPECIFY_THICKNESS,thickness=0.1, orientationType=ANGLE_0,axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
			else:
			    compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format(nam_ply), region=region, material=ReinforceMaterial,thicknessType=SPECIFY_THICKNESS,thickness=0.1, orientationType=ANGLE_0,axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
print(time.time()-a)
'''

'''
a=time.time()
for temp_y in range(2):
	for temp_x in range(len(xarray)):
		temp_n = (temp_y * len(xarray)) + temp_x
		cells_part=PartPlate.cells.findAt(((CoordinateLocate[temp_n][0], CoordinateLocate[temp_n][1],height_plate/2),),)
		region=regionToolset.Region(cells=cells_part)
		for num_ply in range(num_plies):
			if (num_ply+1) == CoordinateLocate[temp_n][3]:
				compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format((num_plies * temp_n) + num_ply + 1), region=region, material=MatrixMaterial,thicknessType=SPECIFY_THICKNESS,thickness=0.1, orientationType=ANGLE_0,axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
			else:
				compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format((num_plies * temp_n) + num_ply + 1), region=region, material=ReinforceMaterial,thicknessType=SPECIFY_THICKNESS,thickness=0.1, orientationType=ANGLE_0,axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
print(time.time()-a)
# 343s
'''
# The influence of judge is limited.
'''
# This part is for Test the influence of judge sentence
a=time.time()
for temp_y in range(2):
    #assign 2 rows to reduce compute time
	for temp_x in range(len(xarray)):
		temp_n = (temp_y * len(xarray)) + temp_x
		cells_part=PartPlate.cells.findAt(((CoordinateLocate[temp_n][0], CoordinateLocate[temp_n][1],height_plate/2),),)
		region=regionToolset.Region(cells=cells_part)
		for num_ply in range(num_plies):
				compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format((num_plies * temp_n) + num_ply + 1), region=region, material=MatrixMaterial, thicknessType=SPECIFY_THICKNESS, 
				thickness=0.1, orientationType=ANGLE_0, additionalRotationType=ROTATION_NONE, additionalRotationField='', 
				axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
print(time.time()-a)
# 338s
'''
'''
a=time.time()
for temp_y in range(2):
	for temp_x in range(len(xarray)):
		temp_n = (temp_y * len(xarray)) + temp_x
		cells_part=PartPlate.cells.findAt(((CoordinateLocate[temp_n][0], CoordinateLocate[temp_n][1],height_plate/2),),)
		region=regionToolset.Region(cells=cells_part)
		for num_ply in range(num_plies):
			if (num_ply+1) == CoordinateLocate[temp_n][3]:
				compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format((num_plies * temp_n) + num_ply + 1), region=region, material=MatrixMaterial, thicknessType=SPECIFY_THICKNESS, 
				thickness=0.1, orientationType=ANGLE_0, additionalRotationType=ROTATION_NONE, additionalRotationField='', 
				axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
			else:
				compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format((num_plies * temp_n) + num_ply + 1), region=region, material=ReinforceMaterial, thicknessType=SPECIFY_THICKNESS, 
				thickness=0.1, orientationType=ANGLE_0, additionalRotationType=ROTATION_NONE, additionalRotationField='', 
				axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
print(time.time()-a)
# 344s
'''