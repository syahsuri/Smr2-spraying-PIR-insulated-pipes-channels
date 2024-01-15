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


# class product():
#     def __init__(self):
#         STL = os.path.join(Process_files_dir, "Product.STL")
        
#     def open_meta_data():


#         return None

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
    turntable_rob_pos     = [-1373.4,-114.6,106,0,0,0]
    turntable_fr.setPose(xyzrpw_2_matrix(turntable_rob_pos))
    turntable_static_fr.setPose(xyzrpw_2_matrix(turntable_rob_pos))

    #Add product refrence frame
    product_fr = RDK.AddFrame("Product",ITEM_TYPE_FRAME)
    product_fr.setParent(turntable_fr)
    product_turntable_pos = [209.5,203.5,51,0,0,180]

    product_fr.setPose(xyzrpw_2_matrix(product_turntable_pos))

    # Import product
    product = RDK.AddFile(os.path.join(Process_files_dir, "Product.STL"))
    product.setParent(product_fr)

    #Add CFP refrence frame
    CFP_fr = RDK.AddFrame("CFP",ITEM_TYPE_FRAME)
    CFP_fr.setParent(product_fr)
    CFP_fr.setPose(xyzrpw_2_matrix([-200,0,0,90,0,90]))
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
              traject_para["X-length"] = product_data[F"face_{i}"][3][1]
        else: traject_para["X-length"] = product_data[F"face_{i}"][3][0]

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
    #Objects
    product = RDK.Item('Product',ITEM_TYPE_OBJECT)
    CFP_fr = RDK.Item('CFP',ITEM_TYPE_FRAME)
    turntable_fr = RDK.Item("Turntable",ITEM_TYPE_FRAME)
    turntable_static_fr = RDK.Item("Turntable_static",ITEM_TYPE_FRAME)

    #settings:
    SP_settings = {"SIZE_X": traject_para["X-length"],
                   "SIZE_Y": traject_para["Y-length"], 
                   "STEP_X": 80, 
                   "STEP_Y": 4.95, 
                   "REPEAT_TIMES": 1,
                   "REPEAT_OFFSET": 2, 
                   "cover_all": False,
                   "even_distribution": True,
                   "continuous": True,
                   "angle_triangle_deg": 0.0,
                   "remove_points_not_on_surface": True}
    
    MachiningSettings = {
                        "Algorithm": 1,  # 0: minimum tool orientation change, 1: tool orientation follows path
                        "ApproachRetractAll": 0,
                        "AutoUpdate": 0,
                        "AvoidCollisions": 0,
                        "FollowAngle": 45,
                        "FollowAngleOn": 1,
                        "FollowRealign": 10,
                        "FollowRealignOn": 0,
                        "FollowStep": 90,
                        "FollowStepOn": 0,
                        "JoinCurvesTol": 0.5,
                        "OrientXaxis2_X": -2,
                        "OrientXaxis2_Y": 0,
                        "OrientXaxis2_Z": 2,
                        "OrientXaxis_X": 0,
                        "OrientXaxis_Y": 0,
                        "OrientXaxis_Z": 1,
                        "PointApproach": 20,
                        "RapidApproachRetract": 1,
                        "RotZ_Range": 180,
                        "RotZ_Step": 20,
                        "SpeedOperation": 50,
                        "SpeedRapid": 1000,
                        "TrackActive": 0,
                        "TrackOffset": 0,
                        "TrackVector_X": -2,
                        "TrackVector_Y": -2,
                        "TrackVector_Z": -2,
                        "TurntableActive": 1,
                        "TurntableOffset": 0,
                        "TurntableRZcomp": 1,
                        "VisibleNormals": 0
                        }

    MachiningProgEvents = {
                        "CallAction": "onPoint",
                        "CallActionOn": 0,
                        "CallApproach": "onApproach",
                        "CallApproachOn": 0,
                        "CallPathFinish": "SpindleOff",
                        "CallPathFinishOn": 1,
                        "CallPathStart": "SpindleOn",
                        "CallPathStartOn": 1,
                        "CallProgFinish": "onFinish",
                        "CallProgFinishOn": 0,
                        "CallProgStart": "ChangeTool(%TOOL%)",
                        "CallProgStartOn": 1,
                        "CallRetract": "onRetract",
                        "CallRetractOn": 0,
                        "Extruder": "Extruder(%1)",
                        "IO_Off": "default",
                        "IO_OffMotion": "OutOffMov(%1)",
                        "IO_On": "default",
                        "IO_OnMotion": "OutOnMov(%1)",
                        "Mcode": "M_RunCode(%1)",
                        "RapidSpeed": 1000,  # rapid speed to move to/from the path
                        "Rounding": 1,  # blending radius
                        "RoundingOn": 0,
                        "SpindleCCW": "",
                        "SpindleCW": "",
                        "SpindleRPM": "SetRPM(%1)",
                        "ToolChange": "SetTool(%1)"
                    }



    #Functions
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
    
    def generate_machining_traject(refrence,settings,Progevents):
        prog = spg_tools.CreateProgram(refrence,settings,Progevents)
        # if prog is not None and prog.Valid():
        #     spg_tools.CreateMainProgram(product, [prog.Name])
        return prog 

    
    print(F"Computing traject: {traject_para['Nmb']}")
    
    #set CFP parent to same parent as turntable (world frame)
    CFP_fr.setParentStatic(turntable_static_fr)

    #turn turntable
    New_pose = pose_2_xyzrpw(turntable_fr.Pose())
    New_pose[5] = traject_para["Angle"]
    turntable_fr.setPose(RDK_math.xyzrpw_2_pose(New_pose))

    print(F"Turntable angle: {traject_para['Angle']}")

    #set new CFP
    New_pose = pose_2_xyzrpw(CFP_fr.Pose())
    New_pose[:3] = traject_para["Startpoint"] + [100,-(SP_settings["STEP_X"]/2),0]
    CFP_fr.setPose(RDK_math.xyzrpw_2_pose(New_pose))
    CFP_fr.setParentStatic(product)

    print(F'CFP set at: {New_pose}')

    #Compute surface pattern
    path_points = generate_surface_pattern_path(product,CFP_fr,SP_settings)
    print(F'Surface pattern generated')

    #create RDK machining program
    mach_prog = generate_machining_traject(CFP_fr,MachiningSettings,MachiningProgEvents)
    print(F'Machining program generated')

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
        
        input(F"Press enter to continue with next side: {traject['Nmb']}")
        process_traject(RDK,traject)
        




if __name__ == "__main__":
    main()