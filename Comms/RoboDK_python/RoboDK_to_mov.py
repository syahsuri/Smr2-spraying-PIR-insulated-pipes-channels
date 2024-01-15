from robolink           import * 
from robodk             import *      
from robodk.robolink    import * 
import os

import kawapai.robot as kawa_connection

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



def main():

    Directory = "C:/Users/tieme/Documents/School/Semester_7 (Minor)/SMR2/Code/RoboDK_python/Process_files/"
    Program_name = "Prog1"

    # Start the RoboDK API:
    if robolink.RoboDKInstallFound():
        RDK = Robolink()
    else: raise Exception("RoboDK not installed")
    #start robot connection
    robot = kawa_connection.KawaBot("192.168.0.5",23)

    #create,upload and run program
    create_kawa_program(RDK,Program_name,Directory)
    upload_kawa_code(robot,os.path.join(Directory, Program_name + ".pg"))
    run_code(robot,Program_name)

    robot.disconnect()

if __name__ == "__main__":
    main()
