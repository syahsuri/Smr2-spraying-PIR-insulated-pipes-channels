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
    print(F'Initializing RoboDK workspace ...')
    #Add robot to RoboDK
    robot = RDK.Item('Kawasaki FS06L',ITEM_TYPE_ROBOT)
    #if not in frame add robot
    if not robot.Valid(): 
        robot.AddFile(os.path.join(Process_files_dir, "Kawasaki-FS06L.robot"))

    #Add turntable refrence frame
    turntable_static_fr = RDK.AddFrame("Turntable_static",ITEM_TYPE_FRAME)
    turntable_fr = RDK.AddFrame("Turntable",ITEM_TYPE_FRAME)
    turntable_rob_pos     = [-1200,300,100,0,0,0]
    turntable_fr.setPose(xyzrpw_2_matrix(turntable_rob_pos))
    turntable_static_fr.setPose(xyzrpw_2_matrix(turntable_rob_pos))

    #Add product refrence frame
    product_fr = RDK.AddFrame("Product",ITEM_TYPE_FRAME)
    product_fr.setParent(turntable_fr)
    product_turntable_pos = [400,-300,0,0,0,90]
    product_fr.setPose(xyzrpw_2_matrix(product_turntable_pos))

    # Import product
    product = RDK.AddFile(os.path.join(Process_files_dir, "Product.STL"))
    product.setParent(product_fr)

    #Add CFP refrence frame
    CFP_fr = RDK.AddFrame("CFP",ITEM_TYPE_FRAME)
    CFP_fr.setParent(product_fr)
    CFP_fr.setPose(xyzrpw_2_matrix([0,0,0,90,-0,180]))
    print(F'Workspace is setup')

def get_process_traject_paras(RDK):
    product_fr = RDK.Item('Product',ITEM_TYPE_FRAME)
    CFP_fr = RDK.Item('CFP',ITEM_TYPE_FRAME)
    turntable_fr = RDK.Item("Turntable",ITEM_TYPE_FRAME)
    turntable_static_fr = RDK.Item("Turntable_static",ITEM_TYPE_FRAME)

#open part metadata
    with open(os.path.join(Process_files_dir, "Product_metadata.json")) as json_file:
        product_data = json.load(json_file)

#find groundplane based on turntable coordinates
    #get current position of product to turntable
    Position = pose_2_xyzrpw(product_fr.PoseWrt(turntable_static_fr))
    #get untranstlated ground plane
    groundplane = np.array(product_data["face_5"])
    #rotate to turntable frame
    r = R.from_euler('xyz', Position[3:], degrees=True)
    groundplane = r.apply(groundplane)
    #apply translation to part
    groundplane = np.add(groundplane,Position[:3])


    traject_parameters = []
    angle_addition = 90
    angle = 0
    #compute the first 4 sides or less (all side profiles) 
    for i in range(product_data["Nmb_of_faces_to_spray"]):
        traject_para = {"Nmb"           : i,
                        "Angle"         : angle,
                        "Y-length"      : product_data[F"face_{i}"][3][2],
                        "combinations"  : [None]
                        }
        if traject_para["Angle"] == 0 or traject_para["Angle"] == 180:
              traject_para["X-length"] = product_data[F"face_{i}"][3][0]
        else: traject_para["X-length"] = product_data[F"face_{i}"][3][1]

        #find startpoint based on translation angle
        r = R.from_euler('z', traject_para["Angle"], degrees=True)
        trnsl_gnd_plane = r.apply(groundplane)
        #find start point (most left/bottom point)
        startpoint = trnsl_gnd_plane[np.lexsort((trnsl_gnd_plane[:,2],-1*trnsl_gnd_plane[:,1],-1*trnsl_gnd_plane[:,0]))][0]
        traject_para["Startpoint"] = np.round(startpoint,0)

        angle += angle_addition
        traject_parameters.append(traject_para)

    return traject_parameters

def process_traject(RDK,traject_para):
    def generate_surface_pattern_path(part,Reference_frame,settings):
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
    
    def generate_surface_pattern_traject(refrence,settings):
        traject = spg_tools.CreateProgram(refrence, SPEED_OPERATION = 200, ANGLE_TCP_X = 0, ANGLE_TCP_Y = 0)
        return traject 

    product = RDK.Item('Product',ITEM_TYPE_OBJECT)
    CFP_fr = RDK.Item('CFP',ITEM_TYPE_FRAME)
    turntable_fr = RDK.Item("Turntable",ITEM_TYPE_FRAME)
    turntable_static_fr = RDK.Item("Turntable_static",ITEM_TYPE_FRAME)

    print(F"Computing traject: {traject_para['Nmb']}")
    
    #set CFP parent to same parent as turntable (world frame)
    CFP_fr.setParentStatic(turntable_static_fr)

    #turn turntable
    New_pose = pose_2_xyzrpw(turntable_fr.Pose())
    New_pose[5] = traject_para["Angle"]
    turntable_fr.setPose(RDK_math.xyzrpw_2_pose(New_pose))

    print(F"Turntable angle: {traject_para['Angle']}")
    

    SP_settings = {"SIZE_X": traject_para["X-length"],
                   "SIZE_Y": traject_para["Y-length"], 
                   "STEP_X": 80, 
                   "STEP_Y": 4.9999, 
                   "REPEAT_TIMES": 1,
                   "REPEAT_OFFSET": 2, 
                   "cover_all": False,
                   "even_distribution": True,
                   "continuous": False,
                   "angle_triangle_deg": 0.0,
                   "remove_points_not_on_surface": True}

    #set new CFP
    New_pose = pose_2_xyzrpw(CFP_fr.Pose())
    New_pose[:3] = traject_para["Startpoint"] + [100,-(SP_settings["STEP_X"]/2),0]
    CFP_fr.setPose(RDK_math.xyzrpw_2_pose(New_pose))
    CFP_fr.setParentStatic(product)

    print(F'CFP set at: {New_pose}')

    #Compute surface pattern
    path_points = generate_surface_pattern_path(product,CFP_fr,SP_settings)

    #create RDK machining program
    mach_prog = generate_surface_pattern_traject(CFP_fr,None)

    return None


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
    traject_paras = get_process_traject_paras(RDK)

    for traject in traject_paras:
        
        process_traject(RDK,traject)
        input("Press enter to continue with next side")




if __name__ == "__main__":
    main()