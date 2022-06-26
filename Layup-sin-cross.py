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
num_DatumPlanes_y = int((width /spacing_y) -1.0)
num_DatumPlanes_x = int((length/spacing_x) -1.0)
num_plies = 11
ply=0
sectionpoint=3
#Architecture Description Function
omega=1.0
Firstphase_1=1.57
Firstphase_2=3.0
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

for i in range(len(da)):
	num = i+2
	PartPlate.PartitionCellByDatumPlane(datumPlane=da[num], cells=cy)
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
#cells1 = PartPlate.cells.findAt(((5.5, 8.3, 1.5),),)
#Assign Material Property
#Region=[]
#for num_x in range(10):
#	for num_y in range(10):
#		region='X{num_X}Y{num_Y}'.format(num_X=num_x,num_Y=num_y)
#		Region.append(region)

#Coordinate computation of x,y and z
zarray_1=[]
zarray_2=[]
zarray=[]
xarray=np.arange(spacing_x/2,length,spacing_x)
yarray=np.arange(spacing_y/2,width,spacing_y)
for i in range(len(xarray)):
	zvalue1=(height_plate/2)*sin(omega*xarray[i]+Firstphase_1) + (height_plate/2)#describing function
	zvalue2=(height_plate/2)*sin(omega*xarray[i]+Firstphase_2) + (height_plate/2)#describing function
	zarray_1.append(zvalue1)
	zarray_2.append(zvalue2)
Ply=[[0 for _ in range(num_plies)] for _ in range(len(xarray)*len(yarray))]

#Combine the tri-axis coordinates
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
#CompositeLayup Predefine
compositeLayup = PartPlate.CompositeLayup(name='CompositeLayup-1', description='', elementType=SOLID, 
        symmetric=False)
compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON, 
        poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
        useDensity=OFF)
compositeLayup.ReferenceOrientation(orientationType=GLOBAL, localCsys=None, 
        fieldName='', additionalRotationType=ROTATION_NONE, angle=0.0, 
        axis=AXIS_3, stackDirection=STACK_3)
#Project architecture to section layers
#'''
for temp_y in range(len(yarray)):
	for temp_x in range(len(xarray)):
		temp_n = (temp_y * len(xarray)) + temp_x
		cells_part=PartPlate.cells.findAt(((CoordinateLocate[temp_n][0], CoordinateLocate[temp_n][1],height_plate/2),),)
		region=regionToolset.Region(cells=cells_part)
		for num_ply in range(num_plies):
			if Ply[temp_n][num_ply] == 1:
				compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format((num_plies * temp_n) + num_ply + 1), region=region, material=MatrixMaterial, thicknessType=SPECIFY_THICKNESS, 
				thickness=0.1, orientationType=ANGLE_0, additionalRotationType=ROTATION_NONE, additionalRotationField='', 
				axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
			else:
				compositeLayup.CompositePly(suppressed=False, plyName='Ply-{}'.format((num_plies * temp_n) + num_ply + 1), region=region, material=ReinforceMaterial, thicknessType=SPECIFY_THICKNESS, 
				thickness=0.1, orientationType=ANGLE_0, additionalRotationType=ROTATION_NONE, additionalRotationField='', 
				axis=AXIS_3, angle=0.0, numIntPoints=sectionpoint)
#'''

# Create Instance
AssemblyPlate=myModel.rootAssembly
InstancePlate=AssemblyPlate.Instance(name=InstanceName, part=PartPlate, dependent=DependentState)
# Create Step
myModel.StaticStep(name=StaticStepName, previous=PreviousStepName,maxNumInc=MaxNumInc, initialInc=InitialInc, minInc=MinInc, maxInc=MaxInc)
# myModel.FieldOutputRequest(name='F-Output-2',createStepName='Step-1', variables=('LE', 'S'), layupNames=('Part-plate-1.CompositeLayup-1', ), layupLocationMethod=ALL_LOCATIONS,rebar=EXCLUDE)

#Create Load
FaceFix=[]
FaceTensile=[]
for y in np.arange(spacing_y/2,width,spacing_y):
	FaceFix.append(InstancePlate.faces.findAt(((0.0,y,height_plate/2),),))
SetFixed=AssemblyPlate.Set(faces=FaceFix, name='Set-Fixed')
for y in np.arange(spacing_y/2,width,spacing_y):
	FaceTensile.append(InstancePlate.faces.findAt(((length,y,height_plate/2),),))
SetTensile=AssemblyPlate.Set(faces=FaceTensile, name='Set-Tensile')
region = AssemblyPlate.sets['Set-Fixed']
myModel.XsymmBC(name='BC-Fixed', createStepName='Initial', 
        region=region, localCsys=None)
region = AssemblyPlate.sets['Set-Tensile']
mdb.models['Model-1'].DisplacementBC(name='BC-Tensile', 
        createStepName='Step-1', region=region, u1=xDis, u2=UNSET, u3=0, 
        ur1=0, ur2=0, ur3=0, amplitude=UNSET, fixed=OFF, 
        distributionType=UNIFORM, fieldName='', localCsys=None)

# Create Seed Control
#find horizontally Line
for y in np.arange(0.0,width+spacing_y,spacing_y):
	for x in np.arange(spacing_x/2,length,spacing_x):
		edge_seed =  PartPlate.edges.findAt(((x,y,height_plate),),)
		PartPlate.seedEdgeByNumber(edges=edge_seed, number=seedNumber, constraint=seedConstraint)
#find perpendicular Line
for y in np.arange(spacing_y/2,width,spacing_y):
	for x in np.arange(0.0,length+spacing_x,spacing_x):
		edge_seed =  PartPlate.edges.findAt(((x,y,height_plate),),)
		PartPlate.seedEdgeByNumber(edges=edge_seed, number=seedNumber, constraint=seedConstraint)
#find vertically Line
yarraylimit=[0.0,width]#boundary of y
xarraylimit=[0.0,length]#boundary of x
for y in yarraylimit:
	for x in np.arange(0.0,length+spacing_x,spacing_x):
		edge_seed =  PartPlate.edges.findAt(((x,y,height_plate/2),),)
		PartPlate.seedEdgeByNumber(edges=edge_seed, number=seedNumber, constraint=seedConstraint)
for x in xarraylimit:
	for y in np.arange(spacing_y,width,spacing_y):
		edge_seed =  PartPlate.edges.findAt(((x,y,height_plate/2),),)
		PartPlate.seedEdgeByNumber(edges=edge_seed, number=seedNumber, constraint=seedConstraint)
# Mesh
# Mesh Control
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
elemType1 = mesh.ElemType(elemCode=SC8R, elemLibrary=STANDARD, 
        secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=SC6R, elemLibrary=STANDARD, 
        secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
elemType3 = mesh.ElemType(elemCode=UNKNOWN_TET, elemLibrary=STANDARD, 
        secondOrderAccuracy=OFF, hourglassControl=DEFAULT)
set_cy=PartPlate.Set(cells=cy, name='Set-cells')
PartPlate.setElementType(regions=set_cy, elemTypes=(elemType1,elemType2,elemType3))

# Submit Job
mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,numGPUs=0)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
mdb.jobs['Job-1'].waitForCompletion()


#Postprocessing
## Two methods of opening odb file
# 1; require "import odbAccess"
#odb = odbAccess.openOdb(path=odbfilename)
# 2; require "import visualization"
odb = session.openOdb(name='myodb',path=odbfilename,readOnly=True)
Frames = odb.steps['Step-1'].frames
#
FOPSet=odb.rootAssembly.nodeSets['SET-TENSILE']
xydata=[]
for Frame in range(len(Frames)):
	RFarray=[]#create array and clear the array
	Uarray =[]#create array and clear the array
	RF=Frames[Frame].fieldOutputs['RF']
	U =Frames[Frame].fieldOutputs['U']
	RFsubset=RF.getSubset(region=FOPSet).values
	Usubset = U.getSubset(region=FOPSet).values
	for RFvalue in range(len(RFsubset)): 
		RFarray.append(RFsubset[RFvalue].data[0]) #data[0] means RF1
	for Uvalue in range(len(Usubset)): 
		Uarray.append(Usubset[Uvalue].data[0])    #data[0] means U1
	stress=np.mean(RFarray)/CrossSectionalArea
	strain=np.mean(Uarray)/(length*2)
	xydata.append((strain,stress))
##Create XYplot
if session.xyPlots.has_key('Curve'):
	xyplot = session.XYPlot('Curve-2')

chartName = xyplot.charts.keys()[0]
chart = xyplot.charts[chartName]
xQuantity = visualization.QuantityType(type = STRAIN)
yQuantity = visualization.QuantityType(type = STRESS)
xy_data = session.XYData(data=xydata, name ='StreesStrainCurves', axis1QuantityType = xQuantity, axis2QuantityType =yQuantity)
xy1 = session.xyDataObjects['StreesStrainCurves']
c1 = session.Curve(xyData=xy1)
chart.setValues(curvesToPlot=(c1, ), )
session.viewports['Viewport: 1'].setValues(displayedObject=xyplot)
session.printToFile(fileName='./StressStrainCurve', format=PNG, 
        canvasObjects=(session.viewports['Viewport: 1'], ))
mdb.saveAs(pathName='./Job1')