# Import libraries
import socket
import sys
import time
import select

import sys

import STL_preprocessor_V12

import RoboDK_python.RoboDK_API as RDKP
from robolink           import * 
from robodk             import *      
from robodk.robolink    import * 
import robodk.robomath  as RDK_math
import kawapai.robot as kawa_connection



#Which files do I have to put in the folder?
#Where do I send rotating command to PLC?
#Do I have to implement more libraries here?


# Define socket connection variable
my_socket = socket

ip_address = "127.0.0.1"
port = 10000
id = "5"

# Initialize socket connection
def initialize():
    global my_socket
    log("Initializing...")

    my_socket = connect_to_server()
    if not is_connected():
        log("Failed")
        return

    log("Ready")

# Connect to socket server
def connect_to_server():
    log("Connecting to server...")
    global my_socket, ip_address, port
    server_address = (ip_address, port)

    while True:
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            my_socket.connect(server_address)
            send_command(id)
            return my_socket
        except ConnectionRefusedError:
            log("Connection attempt failed. Retrying...")
            time.sleep(5)

# Send data over socket
def send_command(message):

    global my_socket
    my_socket.send(message.encode())
    log(f"Data sent: {message}")


def wait_for_command():
    

    global my_socket
    
    log("Waiting for command...")
    ready = select.select([my_socket], [], [])
    if ready[0]:
        data = my_socket.recv(1024).decode()
        if  data:
                log(f"Command received: {data}")
                return data
        else:
            log("No command received within the timeout")
            return None
    

# Check if the socket is connected to the server
def is_connected():
    global my_socket
    if my_socket is not None:
        try:
            # Try to get the peer name, which will raise an exception if not connected
            peername = my_socket.getpeername()
            return True
        except OSError:
            pass
    return False

# Close socket connection
def close():

    global my_socket
    my_socket.close()
    log("Connection closed")

# Check if ready
def is_ready():
    if(is_connected()):
        return True
    return False

# Log messages in console
def log(message):
    print(f"Brago_Socket: {message}")

#----------------------------------------------MAIN CODE--------------------------------------------------------

initialize()
time.sleep(1.5) 

#start connection with kawasaki
Kawasaki = kawa_connection.KawaBot("192.168.0.5",23)
time.sleep(0.2)

RDKP.Kawa_Home(Kawasaki)

send_command("[2]turntable") 
#First, we should make the login and start the program correctly from the interface.
while(True):
    while(True):
        time.sleep(5)    
        #send_command("[2]turntable") 
        send_command("[2]restart") 
        command = wait_for_command()
        if((command == "start" )):
            #Message to plc to start            
            log("Login received")
            break    
        else:
            log("Wrong communication")

    #Now, the interface is going to open the camera and you have to scan the code.
    #After that, it will search the name in the database and confirm is a duct registered.        

    #Wait for command file from the QR Reader.

    stl_name_file = wait_for_command()
    stl_name_file = "D:\\" + stl_name_file
    save_dir = "D:/De Haagse Hogeschool/Brago_PirProject_groups - Documenten/Code/Comms/RoboDK_python/Process_files/"
    image = STL_preprocessor_V12.process_STL(stl_name_file,True,True,True,save_dir)
    send_command("[2]sensorscarrier")

    while(True):
        command = wait_for_command()
        if(command == "ok"):                
                send_command("[2]start")                #Buttons activated
                time.sleep(2)
                send_command("[2]sensorsconveyor")
                break
        else:
            log("Not ready")
    time.sleep(2)
    send_command("[2]sensorsdone")
    command = wait_for_command()                            #Waiting for starting all the process after having QR scanned
    if(command == "done"):
            

            

            #----------------------ROBODK PROCESS-------------------------------------------



            #folder directory were the process files are located/stored
            # Process_files_dir = "C:/Users/tieme/Documents/School/Semester_7 (Minor)/SMR2/Code/RoboDK_python/Process_files/"
            Process_files_dir = "D:/De Haagse Hogeschool/Brago_PirProject_groups - Documenten/Code/Comms/RoboDK_python/Process_files/"

            # Start the RoboDK API:
            if robolink.RoboDKInstallFound():
                RDK = Robolink()
                
            else: raise Exception("RoboDK not installed")

            #Empty frame (for testing purpose)
            RDK.Delete(RDK.ItemList())

            #initiate workspace 
            RDKP.initiate_RDK_workspace(RDK,Process_files_dir)

            #compute process parameters
            traject_paras = RDKP.def_process_traject_paras(RDK,Process_files_dir)

            for i in range(4):

                #create program
                program = RDKP.process_traject(RDK,traject_paras,i)
  
                start_t = time.time()
                print(F'\n______________________________________________________________________________________________')
                print(F'Sending traject:')
                #create kawasaki program
                print(F"Creating kawasaki program       |" ,end="")
                start_t = time.time()
                RDKP.create_kawa_program(RDK,program.Name(),Process_files_dir)
                print(F"{round((time.time()-start_t),3)} s")

                #upload kawasaki program
                print(F"Uploading kawasaki program      |" ,end="")
                start_t = time.time()
                RDKP.upload_kawa_code(Kawasaki,os.path.join(Process_files_dir, program.Name() + ".pg"))
                print(F"{round((time.time()-start_t),3)} s")

                #run kawasaki program
                repeat_speed = 40
                print(F"Run speed                  |{repeat_speed} %")  
                print(F"Run kawasaki code          |" ,end="")
                RDKP.run_code(Kawasaki, program.Name(),repeat_speed)
                start_t = time.time()
                #Wait for kawasaki program to finish on the robot
                RDKP.wait_for_kawa(Kawasaki) 
                print(F"{round((time.time()-start_t),3)} s")
                print(F'______________________________________________________________________________________________\n\n')


                send_command("[3]sidedone")                    #Send this signal to the interface to update progress bar
                
                send_command("[2]rotate")                        #Rotate turntable
                time.sleep(1.5)     


    else:
        log("Error loading images")

    
    command = wait_for_command()
    if(command == "end"):                                       #Once you receive the end from the interface, restart the process
        send_command("[2]ready")                                 #Disable stepper
        send_command("[2]sensorsback")
        log("FINISHED PRODUCT")
    else:
        log("Error in the process")

                    

    
    