"""
RoboDK API program for Brago PIR spraying project
---------------------------------------------------------------
Project: Automatically spraying polyester on 4/5 sides of airducts
         Input of the whole system is a CAD file (STL)

---------------------------------------------------------------
Program functions: - Setup workspace in roboDK
                   - Import Product (proecessed STL)
                   - Compute some trajectory parameters from preprocessed STL file
                   - Generate Surface pattern on part
                   - Generate Robot program (RoboDK)
                   - Generate Kawasaki program
                   - send and execute program on physical robot
---------------------------------------------------------------
Author: Tiemen van Rijswijk
---------------------------------------------------------------
Final revision date: 19-12-2023
---------------------------------------------------------------

"""
"""
Librarys
"""
#RoboDK:
from robolink           import * 
from robodk             import *      
from robodk.robolink    import * 
import robodk.robomath  as RDK_math

#General:
import numpy as np
from scipy.spatial.transform import Rotation as R
import os
import json

#Local modules:
import SurfacePatternGenerator._spgtools as spg_tools
import kawapai.robot as kawa_connection




"""
Kawasaki connection functions
"""

def create_kawa_program(Robo_link,Program_name,Directory):
    #Get first program object
    program = Robo_link.Item(Program_name,ITEM_TYPE_PROGRAM)
    #Create robot specific program
    program.MakeProgram(Directory,RUNMODE_MAKE_ROBOTPROG)

def upload_kawa_code(robot,program_directory):
    #stop current running program
    robot.AS_command(F"HOLD")
    robot.AS_command(F"ABORT")
    #turn robot off
    robot.motor_power_off()
    time.sleep(0.2) #time to let the off switch switch
    #delete current config
    robot.delete_eveything_in_robot_memory()
    #upload new file
    robot.load_as_file(program_directory)

def run_code(robot,program_name):
    #turn the robot on
    robot.motor_power_on()
    #wait for switch to switch
    time.sleep(0.2)
    #run robot program
    robot.AS_command(F"EXECUTE {program_name}")


Process_files_dir = "C:/Users/tieme/Documents/School/Semester_7 (Minor)/SMR2/Code/RoboDK_python/Process_files/"



"""
General robot programs
"""
def Home_program(RDK,folder):
    if not RDK.Item('Home',ITEM_TYPE_PROGRAM).Valid():
        program = RDK.AddProgram('Home')

        program.MoveJ([-90.311605, -18.164237, -127.540950, 180.939124, -19.379123, -220])
        # xyzrpw_2_matrix([802, 112, 928, -68.4, -85.5, 68.6])
    else: program = RDK.Item('Home',ITEM_TYPE_PROGRAM)

    if folder.Valid():
        program.setParent(folder)
    
    return program

def Retract_program(RDK,folder):
    if not RDK.Item('Retract',ITEM_TYPE_PROGRAM).Valid():
        program = RDK.AddProgram('Retract')
        program.MoveJ([-96.691770, 21.122946, -135.131844, 187.304247, -66.426389,-229])
        # xyzrpw_2_matrix([506, 1, 450, 0, -90, 0])
    else: program = RDK.Item('Retract',ITEM_TYPE_PROGRAM)

    if folder.Valid():
        program.setParent(folder)

    return program

def approach_program(RDK,folder):
    if not RDK.Item('Approach',ITEM_TYPE_PROGRAM).Valid():
        program = RDK.AddProgram('Approach')
        program.MoveJ([-86.177112, 49.573354, -127.966713, 176.173596, -87.545544, -210])
        # xyzrpw_2_matrix([453, 190, 100, 0, -90, 0])
    else: program = RDK.Item('Approach',ITEM_TYPE_PROGRAM)

    if folder.Valid():
        program.setParent(folder)

    return program

def Turn_EOAT_ON(RDK,folder):
    if not RDK.Item('EOAT_ON',ITEM_TYPE_PROGRAM).Valid():
        program = RDK.AddProgram('EOAT_ON')
        program.setAO(22,1)
    else: program = RDK.Item('EOAT_ON',ITEM_TYPE_PROGRAM)

    if folder.Valid():
        program.setParent(folder)
    return program

def Turn_EOAT_OFF(RDK,folder):
    if not RDK.Item('EOAT_OFF',ITEM_TYPE_PROGRAM).Valid():
        program = RDK.AddProgram('EOAT_OFF')
        program.setAO(22,0)
    else: program = RDK.Item('EOAT_OFF',ITEM_TYPE_PROGRAM)

    if folder.Valid():
        program.setParent(folder)
    return program


"""
Functions
"""
def xyzrpw_2_matrix(pose):
    matrix = RDK_math.xyzrpw_2_pose(pose)
    return matrix

def initiate_RDK_workspace(RDK):
    print(F'Initializing RoboDK workspace ...')
    #Add robot to RoboDK
    robot = RDK.Item('Kawasaki FS06L',ITEM_TYPE_ROBOT)
    #if not in frame add robot
    if not robot.Valid(): 
        robot.AddFile(os.path.join(Process_files_dir, "Kawasaki-FS06L.robot"))
        robot = RDK.Item('Kawasaki FS06L',ITEM_TYPE_ROBOT)

    #Add EOAT
    EOAT = RDK.AddFile(os.path.join(Process_files_dir, "EOAT.stl"))
    EOAT.setParent(robot)
    EOAT.setParam("Convert","Tool")
    
    EOAT.setGeometryPose(xyzrpw_2_matrix([0, 0, 0, 90, 0, -135]))
    EOAT.setPoseTool(xyzrpw_2_matrix([5, -5, 200, 0, 0, 0]))

    #Add turntable refrence frame
    turntable_static_fr = RDK.AddFrame("Turntable_static",ITEM_TYPE_FRAME)
    turntable_fr = RDK.AddFrame("Turntable",ITEM_TYPE_FRAME)
    turntable_rob_pos     = [-1373.4,-114.6,106,0,0,0]
    turntable_fr.setPose(xyzrpw_2_matrix(turntable_rob_pos))
    turntable_static_fr.setPose(xyzrpw_2_matrix(turntable_rob_pos))

    #Add product refrence frame
    product_fr = RDK.AddFrame("Product",ITEM_TYPE_FRAME)
    product_fr.setParent(turntable_fr)
    product_turntable_pos = [249.5,243.5,51,0,0,180]
                            # [209.5,203.5,51,0,0,180]
    product_fr.setPose(xyzrpw_2_matrix(product_turntable_pos))

    # Import product
    product = RDK.AddFile(os.path.join(Process_files_dir, "Product.STL"))
    product.setParent(product_fr)

    #Add CFP refrence frame
    CFP_fr = RDK.AddFrame("CFP",ITEM_TYPE_FRAME)
    CFP_fr.setParent(product_fr)
    CFP_fr.setPose(xyzrpw_2_matrix([-200,0,20,90,0,90]))
    
    #Add some default movement trajects
    folder_id = RDK.Command("AddFolder", "Programs")
    program_folder = Item(RDK, folder_id)
    
    Home_program(RDK,program_folder)
    Retract_program(RDK,program_folder)
    approach_program(RDK,program_folder)
    Turn_EOAT_ON(RDK,program_folder)
    Turn_EOAT_OFF(RDK,program_folder)
    
    print(F'Workspace is setup')

def def_process_traject_paras(RDK):
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

def process_traject(RDK,traject_paras,i):
    #Objects
    product = RDK.Item('Product',ITEM_TYPE_OBJECT)
    CFP_fr = RDK.Item('CFP',ITEM_TYPE_FRAME)
    turntable_fr = RDK.Item("Turntable",ITEM_TYPE_FRAME)
    turntable_static_fr = RDK.Item("Turntable_static",ITEM_TYPE_FRAME)

    traject_para = traject_paras[i]

    #settings:
    SP_settings = {"SIZE_X": traject_para["X-length"],
                   "SIZE_Y": traject_para["Y-length"] - 60, 
                   "STEP_X": 50, 
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
                        "SpeedOperation": 400,
                        "SpeedRapid": 1000,
                        "TrackActive": 0,
                        "TrackOffset": 0,
                        "TrackVector_X": -2,
                        "TrackVector_Y": -2,
                        "TrackVector_Z": -2,
                        "TurntableActive": 1,
                        "TurntableOffset": 0,
                        "TurntableRZcomp": 1,
                        "VisibleNormals": 0,
                        }

    MachiningProgEvents = {
                        "CallAction": "onPoint",
                        "CallActionOn": 0,
                        "CallApproach": "onApproach",
                        "CallApproachOn": 0,
                        "CallPathFinish": "EOAT_OFF",
                        "CallPathFinishOn": 1,
                        "CallPathStart": "EOAT_ON",
                        "CallPathStartOn": 1,
                        "CallProgFinish": "onFinish",
                        "CallProgFinishOn": 0,
                        "CallProgStart": "ChangeTool(%TOOL%)",
                        "CallProgStartOn": 0,
                        "CallRetract": "onRetract",
                        "CallRetractOn": 0,
                        "Extruder": "Extruder(%1)",
                        "IO_Off": "default",
                        "IO_OffMotion": "OutOffMov(%1)",
                        "IO_On": "default",
                        "IO_OnMotion": "OutOnMov(%1)",
                        "Mcode": "M_RunCode(%1)",
                        "RapidSpeed": 1000,  # rapid speed to move to/from the path
                        "Rounding": 25,  # blending radius
                        "RoundingOn": 1,
                        "SpindleCCW": "",
                        "SpindleCW": "",
                        "SpindleRPM": "SetRPM(%1)",
                        "ToolChange": "SetTool(%1)"
                    }

    MachiningSettings2 = {"Start_joints":[-96.7, 21.2, -135, 187.3, -66.4, -92.9],
                          "Tool_offset" : xyzrpw_2_matrix([0,0,0,0,0,-135])}

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
    
    def generate_machining_traject(refrence,settings,setting2,Progevents):
        prog = spg_tools.CreateProgram(refrence,settings,setting2,Progevents)
        # if prog is not None and prog.Valid():
        #     spg_tools.CreateMainProgram(product, [prog.Name])
        return prog 

    #Delete (if existing) previous items
    RDK.Delete(RDK.Item('Main',ITEM_TYPE_PROGRAM))
    RDK.Delete(RDK.Item('CFP',ITEM_TYPE_PROGRAM))
    RDK.Delete(RDK.Item('CFP',ITEM_TYPE_MACHINING))
    RDK.Delete(RDK.Item('CFP',ITEM_TYPE_OBJECT))
    
    print(F"Computing traject: {traject_para['Nmb']}")
    
    #set CFP parent to same parent as turntable (world frame)
    CFP_fr.setParentStatic(turntable_static_fr)

    #turn turntable
    New_pose = pose_2_xyzrpw(turntable_fr.Pose())
    New_pose[5] = traject_para["Angle"]
    turntable_fr.setPose(RDK_math.xyzrpw_2_pose(New_pose))

    print(F"\nTurntable angle: {traject_para['Angle']}")

    #set new CFP
    New_pose = pose_2_xyzrpw(CFP_fr.Pose())
    New_pose[:3] = traject_para["Startpoint"] + [100,-25,40]
    CFP_fr.setPose(RDK_math.xyzrpw_2_pose(New_pose))
    CFP_fr.setParentStatic(product)

    print(F'\nCFP set at: {New_pose}')

    #Compute surface pattern
    path_points = generate_surface_pattern_path(product,CFP_fr,SP_settings)
    print(F'\nSurface pattern generated')

    #create RDK machining program
    mach_prog = generate_machining_traject(CFP_fr,MachiningSettings,MachiningSettings2,MachiningProgEvents)
    print(F'\nMachining program generated')

    #create Main Calling program
    
    prog = RDK.AddProgram('Main')
    
    if traject_para["Nmb"] == 0:
        prog.RunInstruction('Home',INSTRUCTION_CALL_PROGRAM)
        homing = True
    else: homing = False

    prog.RunInstruction('Approach',INSTRUCTION_CALL_PROGRAM)
    approach = True
    prog.RunInstruction('CFP',INSTRUCTION_CALL_PROGRAM)
    CFP = True
    
    if len(traject_paras)-1 != traject_para["Nmb"]:
          prog.RunInstruction('Retract',INSTRUCTION_CALL_PROGRAM)
          retract = True
          homing2 = False
    else: 
        prog.RunInstruction('Home',INSTRUCTION_CALL_PROGRAM)
        retract = False
        homing2 = True
    
    print(F'\nGenerated main program:')
    print(F'homing    | {homing}')
    print(F'approach  | {approach}')
    print(F'CFP       | {CFP}')
    print(F'retract   | {retract}')
    print(F'homing    | {homing2}')

    return prog




"""
MAIN
"""

def main():

    # Start the RoboDK API:
    if robolink.RoboDKInstallFound():
        RDK = Robolink()
        
    else: raise Exception("RoboDK not installed")

    #Empty frame (for testing purpose)
    RDK.Delete(RDK.ItemList())

    #initiate workspace 
    initiate_RDK_workspace(RDK)

    #start connection with kawasaki
    Kawasaki = kawa_connection.KawaBot("192.168.0.5",23)

    #compute process parameters
    traject_paras = def_process_traject_paras(RDK)

    for i in range(4):
        
        input(F"\nPress enter to continue with next side: {i}")

        #create program
        program = process_traject(RDK,traject_paras,i)
        
        
        if True:
            input(F"\nPress enter to send to robot")
            #create kawasaki program
            create_kawa_program(RDK,program.Name(),Process_files_dir)
            #upload kawasaki program
            upload_kawa_code(Kawasaki,os.path.join(Process_files_dir, program.Name() + ".pg"))
            #run kawasaki program
            run_code(Kawasaki,program.Name())
            


"""
Program if modules is run as main
"""

if __name__ == "__main__":
    main()