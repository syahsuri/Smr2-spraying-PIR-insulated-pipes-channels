from pyzbar.pyzbar import decode
from datetime import datetime
import pandas as pd
import threading
import time
import cv2
import ast
import socket
import select

# Import libraries
import socket
import time
import select


my_socket = socket

ip_address = "127.0.0.1"
port = 10000
id = "4"

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


def wait_for_command(timeout=0.1):
    log("Waiting for command...")

    global my_socket
    ready = select.select([my_socket], [], [], timeout)
    if ready[0]:
        data = my_socket.recv(1024).decode()
        if data:
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







def decode_qr_code(frame):
    decoded_objects = decode(frame)

    decoded_data = None

    for obj in decoded_objects:
        decoded_data = obj.data.decode("utf-8")
        print(f'{decoded_data}')
    
    return decoded_data

def qrCameraInitialization():
    global cam
    cam = cv2.VideoCapture(0)
    cam.set(3, 320)
    cam.set(4, 240)

def qrCodeDetection(show=False):
    success, frame = cam.read()
    qr_code_information = decode_qr_code(frame)                 # Calling The Decode fuction

    if show:
        cv2.imshow("QR Code Scanner", frame)

        # Wait for 3000 MiliSecond to take another picture
        cv2.waitKey(2000)

    if qr_code_information is not None:
        return True, qr_code_information
    else:
        return False, None

def qr_thread():

    while True:        
        available, data = qrCodeDetection(True)
        if available:
            send_command("[3]"+ data)
            #data_list = list(ast.literal_eval(data[1:-1]))
            #print(data_list)
            


    
    

qr_thread = threading.Thread(target=qr_thread)

initialize()

qrCameraInitialization()

time.sleep(0.5)

qr_thread.start()