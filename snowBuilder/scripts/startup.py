import maya.cmds as cmds
import os

print "// Loading SnowBuilder Setups //"

# Updating template search path to access SnowBuilder template.
Current_location = os.path.dirname(__file__)
Current_location = os.path.join(os.path.split(Current_location)[0], "templates")
cmds.containerTemplate(e=True, searchPath=Current_location)
