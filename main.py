import glob
import os
import random

import pybullet as p
import time
import math
import pybullet_data



#cid = p.connect(p.SHARED_MEMORY_GUI)
cid = p.connect(p.GUI)
if (cid < 0):
  p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setPhysicsEngineParameter(numSolverIterations=10)
p.setTimeStep(1. / 120.)
logId = p.startStateLogging(p.STATE_LOGGING_PROFILE_TIMINGS, "visualShapeBench.json")
#useMaximalCoordinates is much faster then the default reduced coordinates (Featherstone)
# p.loadURDF("plane_transparent.urdf", useMaximalCoordinates=True)
#disable rendering during creation.
# p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 0)
# p.configureDebugVisualizer(p.COV_ENABLE_PLANAR_REFLECTION, 1)

# p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
#disable tinyrenderer, software (CPU) renderer, we don't use it here
# p.configureDebugVisualizer(p.COV_ENABLE_TINY_RENDERER, 0)
p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 1)

shift = [0, -0.02, 0]
meshScale = [0.1, 0.1, 0.1]
#the visual shape and collision shape can be re-used by all createMultiBody instances (instancing)
# /home/josyula/Documents/DataAndModels/ufo_trees_labelled/1_l.x3d
"/home/josyula/Documents/DataAndModels/ufo_trees_labelled/1_l.obj"
visualShapeId = p.createVisualShape(shapeType=p.GEOM_MESH,
                                    fileName="/home/josyula/Documents/DataAndModels/ufo_trees_labelled/1_l.obj",
                                    rgbaColor=None)
                                    # specularColor=[0.4, .4, 0],
                                    # visualFramePosition=shift,
                                    # meshScale=meshScale)
collisionShapeId = p.createCollisionShape(shapeType=p.GEOM_MESH,
                                          fileName="/home/josyula/Documents/DataAndModels/ufo_trees_labelled/1_l.obj")
                                          # collisionFramePosition=shift,
                                          # meshScale=meshScale)

multiBodyId = p.createMultiBody(baseMass=1,
                  baseInertialFramePosition=[0, 0, 0],
                  baseCollisionShapeIndex=collisionShapeId,
                  baseVisualShapeIndex=visualShapeId,
                  basePosition=[0,0,0],
                  useMaximalCoordinates=True)

# texture_paths = glob.glob(os.path.join('/home/josyula/Documents/DataAndModels/ufo_trees_labelled/dtd', '**', '*.jpg'), recursive=True)
# random_texture_path = texture_paths[random.randint(0, len(texture_paths) - 1)]
# textureId = p.loadTexture(random_texture_path)
# p.changeVisualShape(multiBodyId, -1, textureUniqueId=textureId)
# rangex = 3
# rangey = 3
# for i in range(rangex):
#   for j in range(rangey):
#     p.createMultiBody(baseMass=1,
#                       baseInertialFramePosition=[0, 0, 0],
#                       baseCollisionShapeIndex=collisionShapeId,
#                       baseVisualShapeIndex=visualShapeId,
#                       basePosition=[((-rangex / 2) + 0) * meshScale[0] * 2,
#                                     (-rangey / 2 + 0) * meshScale[1] * 2, 1],
#                       useMaximalCoordinates=True)
p.stopStateLogging(logId)
p.setGravity(0, 0, 0)
p.setRealTimeSimulation(1)

colors = [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1], [1, 1, 1, 1]]
currentColor = 0
i=0
while (1):
#   p.resetDebugVisualizerCamera(cameraDistance=3, cameraYaw=30, cameraPitch=52, cameraTargetPosition=colors[i%3][:3])
  p.getDebugVisualizerCamera()
#   i=i+1
  # mouseEvents = p.getMouseEvents()
  # for e in mouseEvents:
  #   if ((e[0] == 2) and (e[3] == 0) and (e[4] & p.KEY_WAS_TRIGGERED)):
  #     mouseX = e[1]
  #     mouseY = e[2]
  #     #p.addUserDebugLine(rayFrom,rayTo,[1,0,0],3)
  #   objectUid = hit[0]
  #   if (objectUid >= 1):
  #     #p.removeBody(objectUid)
  #     p.changeVisualShape(objectUid, -1, rgbaColor=colors[currentColor])
  #     currentColor += 1
  #     if (currentColor >= len(colors)):
  #       currentColor = 0