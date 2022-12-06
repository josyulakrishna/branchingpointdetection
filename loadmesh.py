import pybullet as p
import time

#file to load mesh into pybullet

client = p.connect(p.GUI)
p.setAdditionalSearchPath("/home/josyula/Documents/DataAndModels/ufo_trees_labelled")
p.setGravity(0,0,-10)
p.createVisualShape(shapeType=p.GEOM_MESH, fileName="1_l.obj")
p.createMultiBody(baseMass=1, baseVisualShapeIndex=1, basePosition=[0,0,1])
p.setRealTimeSimulation(1)
