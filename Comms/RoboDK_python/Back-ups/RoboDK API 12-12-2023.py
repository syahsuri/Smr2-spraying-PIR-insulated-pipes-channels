from robolink           import * 
from robodk             import *      
from robodk.robolink    import * 
import robodk.robomath  as RDK_math

import numpy as np
from scipy.spatial.transform import Rotation as R


def xyzrpw_2_matrix(pose):
    matrix = RDK_math.xyzrpw_2_pose(pose)
    return matrix


orientated_product = "RoboDK_python\TEMP_FILES\Product.STL"



turntable_position = [100,100,100,0,0,0]



# Start the RoboDK API:
if robolink.RoboDKInstallFound():
    RDK = Robolink()
else: raise Exception("RoboDK not installed")


#Empty frame (for testing purpose)
RDK.Delete(RDK.ItemList())



#Add robot to RoboDK
robot = RDK.Item('Kawasaki FS06L',ITEM_TYPE_ROBOT)
#if not in frame add robot
if not robot.Valid(): 
    robot.AddFile("RoboDK/Kawasaki-FS06L.robot")

#Add turntable refrence frame
turntable_fr = RDK.AddFrame("Turntable",ITEM_TYPE_FRAME)
turntable_fr.setPose(xyzrpw_2_matrix(turntable_position))

#Add product refrence frame
product_fr = RDK.AddFrame("Product",ITEM_TYPE_FRAME)
product_fr.setParent(turntable_fr)

# Import product
product = RDK.AddFile(orientated_product)
product.setParent(product_fr)
print("test")

#Generate surface pattern


#generate program
