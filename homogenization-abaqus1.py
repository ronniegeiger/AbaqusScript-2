from abaqus import *
from abaqusConstants import *
import os
import job
from odbAccess import *	
import string
import visualization
for irves in range(1):

    if irves==0:
        odbname='Job-1.odb'
        filename='HomogenizedStrain.txt'
        filename1='HomogenizedStress.txt'        
        
    odb = openOdb(odbname)
    scratchOdb = session.ScratchOdb(odb)   
    datum=scratchOdb.rootAssembly.DatumCsysByThreePoints(name='CSYS-1', coordSysType=CARTESIAN,
            origin=(0.0, 0.0, 0.0), point1=(0.0, 0.0, 1.0), point2=(0.0, 1.0, 0.0))
    S=[[0.0 for col in range(6)] for row in range (6)]
    E=[[0.0 for col in range(6)] for row in range (6)]

    VRVE=[0.0 for row in range (6)]


    for j in range(6):
  
	for i in range(len(odb.rootAssembly.instances)-1):
    
      
	    Stepname = 'Step-' + str(j+1)  
	    if i==0:
	        InstanceName='PART-M-1'
	    if i==1:
	        InstanceName='PART-F-1'
	    if i==2:
	        InstanceName='PART-IN-1'
        
	    

	    Instance = odb.rootAssembly.instances[InstanceName]
    
	    stressField1 = odb.steps[Stepname].frames[-1].fieldOutputs['S']
  
	    stressField=stressField1.getTransformedField(datumCsys=datum)
        
	    field1 = stressField.getSubset(region=Instance, position=INTEGRATION_POINT)
	    field1Values = field1.values

	    strainField1 = odb.steps[Stepname].frames[-1].fieldOutputs['EE']
	    strainField=strainField1.getTransformedField(datumCsys=datum)
	    field2 = strainField.getSubset(region=Instance, position=INTEGRATION_POINT)
	    field2Values = field2.values

	    ivolField = odb.steps[Stepname].frames[-1].fieldOutputs['IVOL']
	    field3 = ivolField.getSubset(region=Instance, position=INTEGRATION_POINT)
	    field3Values = field3.values

	    evolField = odb.steps[Stepname].frames[-1].fieldOutputs['EVOL']
	    field4 = evolField.getSubset(region=Instance, position=WHOLE_ELEMENT)
	    field4Values = field4.values



	    for v in range(len(field1Values)): 
  
		S[j][0]=S[j][0]+field1Values[v].data[0]*field3Values[v].data
		S[j][1]=S[j][1]+field1Values[v].data[1]*field3Values[v].data
		S[j][2]=S[j][2]+field1Values[v].data[2]*field3Values[v].data 
		S[j][3]=S[j][3]+field1Values[v].data[3]*field3Values[v].data  
		S[j][4]=S[j][4]+field1Values[v].data[4]*field3Values[v].data
		S[j][5]=S[j][5]+field1Values[v].data[5]*field3Values[v].data  
   
		E[j][0]=E[j][0]+field2Values[v].data[0]*field3Values[v].data
		E[j][1]=E[j][1]+field2Values[v].data[1]*field3Values[v].data  
		E[j][2]=E[j][2]+field2Values[v].data[2]*field3Values[v].data  
		E[j][3]=E[j][3]+field2Values[v].data[3]*field3Values[v].data 
		E[j][4]=E[j][4]+field2Values[v].data[4]*field3Values[v].data
		E[j][5]=E[j][5]+field2Values[v].data[5]*field3Values[v].data    	

	    for v in range(len(field4Values)): 
  
		VRVE[j]=VRVE[j]+field4Values[v].data


	S[j][0]=S[j][0]/VRVE[j]
	E[j][0]=E[j][0]/VRVE[j]
	
	S[j][1]=S[j][1]/VRVE[j]
	E[j][1]=E[j][1]/VRVE[j]
    
	S[j][2]=S[j][2]/VRVE[j]
	E[j][2]=E[j][2]/VRVE[j]
    
	S[j][3]=S[j][3]/VRVE[j]
	E[j][3]=E[j][3]/VRVE[j]
    
	S[j][4]=S[j][4]/VRVE[j]
	E[j][4]=E[j][4]/VRVE[j]
    
	S[j][5]=S[j][5]/VRVE[j]
	E[j][5]=E[j][5]/VRVE[j]
    '''
    for j in range(6):
	S1=S[j][0]
	S2=S[j][1]
	S3=S[j][2]
	S4=S[j][5]
	S5=S[j][4]
	S6=S[j][3]
    
    E1=E[j][0]
	E2=E[j][1]
	E3=E[j][2]
	E4=E[j][5]
	E5=E[j][4]
	E6=E[j][3]
    '''
  
    f=open(filename, 'w')
    f.write(str(E))
    '''
	f.write('\n')
	f.write(str(E2))
	f.write('\n')
	f.write(str(E3))
	f.write('\n')
	f.write(str(E4))
	f.write('\n')
	f.write(str(E5))
	f.write('\n')
	f.write(str(E6))
    '''
    f.close()
    
    '''
    for j in range(6):
	S1=S[j][0]
	S2=S[j][1]
	S3=S[j][2]
	S4=S[j][5]
	S5=S[j][4]
	S6=S[j][3]
    '''

    f=open(filename1, 'w')
    f.write(str(S))
    '''
	f.write('\n')
	f.write(str(S2))
	f.write('\n')
	f.write(str(S3))
	f.write('\n')
	f.write(str(S4))
	f.write('\n')
	f.write(str(S5))
	f.write('\n')
	f.write(str(S6))
    '''
    
    f.close()

    odb.close()    


