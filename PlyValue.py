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
# This script is built with 3 plies in single region, generating by random module of python, and
# caculating by while sentence.
# -------------------------------------------
