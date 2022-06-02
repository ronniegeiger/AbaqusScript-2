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

# Import material property form lib of materials
from material import createMaterialFromDataString
createMaterialFromDataString('Model-1', 'CompositeLaminates', '2019', 
        """{'materialIdentifier': '', 'description': '', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((162000.0, 14900.0, 14900.0, 0.283, 0.283, 0.386, 5.7, 5.7, 5.4),), 'type': ENGINEERING_CONSTANTS}, 'name': 'CompositeLaminates'}""")
createMaterialFromDataString('Model-1', 'AluminumAlloy_6061', '2019',"""{'name': 'AluminumAlloy_6061', 'elastic': {'temperatureDependency': OFF, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'dependencies': 0, 'table': ((70000.0, 0.35),), 'type': ISOTROPIC}, 'density': {'temperatureDependency': OFF, 'table': ((2.7e-06,),), 'dependencies': 0, 'fieldName': '', 'distributionType': UNIFORM}, 'plastic': {'temperatureDependency': OFF, 'strainRangeDependency': OFF, 'rate': OFF, 'dependencies': 0, 'hardening': ISOTROPIC, 'dataType': HALF_CYCLE, 'table': ((200.0, 0.0), (246.0, 0.0235), (294.0, 0.0474), (374.0, 0.0935), (437.0, 0.1377), (480.0, 0.18)), 'numBackstresses': 1}, 'materialIdentifier': '', 'description': ''}""")

myModel.HomogeneousSolidSection(name='Section-1',material='AluminumAlloy_6061', thickness=None)
cell1=PartPlate.cells
regionPlate = regionToolset.Region(cells=cell1)
PartPlate.SectionAssignment(region=regionPlate, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)

# Create Instance
AssemblyPlate=myModel.rootAssembly
InstancePlate=AssemblyPlate.Instance(name=InstanceName, part=PartPlate, dependent=DependentState)
# Create Step
myModel.StaticStep(name=StaticStepName, previous=PreviousStepName, 
        maxNumInc=MaxNumInc, initialInc=InitialInc, minInc=MinInc, maxInc=MaxInc)
#Create Load
FaceFix=[]
FaceTensile=[]
FaceFix.append(InstancePlate.faces.findAt(((0.0,width/2,height_plate/2),),))
SetFixed=AssemblyPlate.Set(faces=FaceFix, name='Set-Fixed')
FaceTensile.append(InstancePlate.faces.findAt(((length,width/2,height_plate/2),),))
SetTensile=AssemblyPlate.Set(faces=FaceTensile, name='Set-Tensile')
region = AssemblyPlate.sets['Set-Fixed']
myModel.XsymmBC(name='BC-Fixed', createStepName='Initial', 
        region=region, localCsys=None)
region = AssemblyPlate.sets['Set-Tensile']
myModel.DisplacementBC(name='BC-Tensile',createStepName='Step-1', region=region, u1=2.68, u2=UNSET, u3=UNSET, 
        ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
# Create Seeds
PartPlate.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
PartPlate.generateMesh()
# Submit Job
mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
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