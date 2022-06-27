from abaqus import *
from abaqusConstants import *
import os
import job
from odbAccess import *	
import string
import visualization
from textRepr import *
import numpy as np
import regionToolset

odbname='Job-1.odb'
odb = openOdb(odbname)
scratchOdb = session.ScratchOdb(odb)

