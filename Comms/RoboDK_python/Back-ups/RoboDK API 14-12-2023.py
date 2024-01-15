from robolink           import * 
from robodk             import *      
from robodk.robolink    import * 
import robodk.robomath  as RDK_math

import numpy as np
from scipy.spatial.transform import Rotation as R
import os
import json

import SurfacePatternGenerator._spgtools as spg_tools
Process_files_dir = "C:/Users/tieme/Documents/School/Semester_7 (Minor)/SMR2/Code/RoboDK_python/Process_files/"





def xyzrpw_2_matrix(pose):
    matrix = RDK_math.xyzrpw_2_pose(pose)
    return matrix


class product():
    def __init__(self):
        STL = os.path.join(Process_files_dir, "Product.STL")
        
    def open_meta_data():


        return None

def initiate_RDK_workspace(RDK):
    #Add robot to RoboDK
    robot = RDK.Item('Kawasaki FS06L',ITEM_TYPE_ROBOT)
    #if not in frame add robot
    if not robot.Valid(): 
        robot.AddFile(os.path.join(Process_files_dir, "Kawasaki-FS06L.robot"))

    #Add turntable refrence frame
    turntable_fr = RDK.AddFrame("Turntable",ITEM_TYPE_FRAME)
    turntable_ros_pos     = [-1200,300,100,0,0,0]
    turntable_fr.setPose(xyzrpw_2_matrix(turntable_ros_pos))

    #Add product refrence frame
    product_fr = RDK.AddFrame("Product",ITEM_TYPE_FRAME)
    product_fr.setParent(turntable_fr)
    product_turntable_pos = [400,-250,0,0,0,90]
    product_fr.setPose(xyzrpw_2_matrix(product_turntable_pos))

    # Import product
    product = RDK.AddFile(os.path.join(Process_files_dir, "Product.STL"))
    product.setParent(product_fr)

    #Add CFP refrence frame
    CFP_fr = RDK.AddFrame("CFP",ITEM_TYPE_FRAME)
    CFP_fr.setParent(product_fr)
    CFP_fr.setPose(xyzrpw_2_matrix([10,-100,0,0,-90,-90]))

def generate_surface_pattern_points(part,Reference_frame,settings):
    pattern_points = spg_tools.CreatePaths(Reference_frame, part,
                          settings["SIZE_X"],
                          settings["SIZE_Y"],
                          settings["STEP_X"],
                          settings["STEP_Y"],
                          settings["REPEAT_TIMES"],
                          settings["REPEAT_OFFSET"],
                          settings["cover_all"],
                          settings["even_distribution"],
                          settings["continuous"],
                          settings["angle_triangle_deg"],
                          settings["remove_points_not_on_surface"])
    return pattern_points

def turn_part(RDK):

    return None

def get_process_traject_paras():
    #open part metadata
    with open(os.path.join(Process_files_dir, "Product_metadata.json")) as json_file:
        product_data = json.load(json_file)
    
    traject_parameters = []

    angle_addition = 90
    angle = 0
    X_Y = 0

    #compute the first 4 sides or less (all side profiles) 
    for i in range(product_data["Nmb_of_faces_to_spray"]):
        traject_para = {"Nmb"           : i,
                        "Angle"         : angle,
                        "Startpoint"    : [0,0,0],
                        "Y-length"      : product_data[F"face_{i}"][3][2],
                        "combinations"  : [None]
                        }
        if traject_para["Angle"] == 0 or traject_para["Angle"] == 180:
              traject_para["X-length"] = product_data[F"face_{i}"][3][0]
        else: traject_para["X-length"] = product_data[F"face_{i}"][3][1]

        angle += angle_addition
        traject_parameters.append(traject_para)

    return traject_parameters




def main():

    # Start the RoboDK API:
    if robolink.RoboDKInstallFound():
        RDK = Robolink()
        
    else: raise Exception("RoboDK not installed")

    #Empty frame (for testing purpose)
    RDK.Delete(RDK.ItemList())

    #initiate workspace 
    initiate_RDK_workspace(RDK)
    
    #compute process parameters
    traject_paras = get_process_traject_paras()

    #Generate surface pattern
    SP_settings = {"SIZE_X": 500,
                   "SIZE_Y": 500, 
                   "STEP_X": 80, 
                   "STEP_Y": 5, 
                   "REPEAT_TIMES": 1,
                   "REPEAT_OFFSET": 2, 
                   "cover_all": False,
                   "even_distribution": False,
                   "continuous": False,
                   "angle_triangle_deg": 0.0,
                   "remove_points_not_on_surface": True}
    
    product = RDK.Item('Product',ITEM_TYPE_OBJECT)
    CFP_fr = RDK.Item('CFP',ITEM_TYPE_FRAME)
    path_points = generate_surface_pattern_points(product,CFP_fr,SP_settings)

#generate program



if __name__ == "__main__":
    main()