import fins.udp
import time
import binascii

fins_instance = fins.udp.UDPFinsConnection()
fins_instance.connect('192.168.0.2')
fins_instance.dest_node_add = 1
fins_instance.srce_node_add = 25

import socket
import time
import select


# Define socket connection variable
my_socket = socket

ip_address = "127.0.0.1"
port = 10000
id = "2"

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

#mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD, b'\x00\x00\x00')

def message_PLC(received_message):
    
    if (received_message == "sensorsconveyor"):
        time.sleep(3)
        while True:
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD, b'\x00\x00\x00')
            print("READ")
            print(mem_area)

            last_4_bytes = mem_area[-4:]
            integer_value = int.from_bytes(last_4_bytes, byteorder='big', signed=False)
            integer_value= bin(integer_value)[2:]
            print("Binary representation of the last 4 bytes:", integer_value)
            #The bit index 3 is for reading sensor that is outside of the wall
            bit_index = 5
            bitmask = int(integer_value[bit_index])
 
            
            print(bitmask)
           


            if(bitmask == 0):
                time.sleep(1)
                send_command("[3]go")
                break
    elif (received_message == "sensorscarrier"):

        while True:
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD, b'\x00\x00\x00')
            print("READ")
            print(mem_area)

            last_4_bytes = mem_area[-4:]
            integer_value = int.from_bytes(last_4_bytes, byteorder='big', signed=False)
            integer_value= bin(integer_value)[2:]
            print("Binary representation of the last 4 bytes:", integer_value)
            
            bit_index = 1
            bitmask = int(integer_value[bit_index])
 
            
            print(bitmask)
           


            if(bitmask == 1):
                send_command("[3]correct")
                break

    elif (received_message == "sensorsback"):
        time.sleep(3)
        while True:
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD, b'\x00\x00\x00')
            print("READ")
            print(mem_area)

            last_4_bytes = mem_area[-4:]
            integer_value = int.from_bytes(last_4_bytes, byteorder='big', signed=False)
            integer_value= bin(integer_value)[2:]
            print("Binary representation of the last 4 bytes:", integer_value)
            #The bit index 3 is for reading sensor that is outside of the wall
            bit_index = 3
            bitmask = int(integer_value[bit_index])
            
            print(bitmask)


            if(bitmask == 1):
                send_command("[3]finish")
                break

            
    elif (received_message == "sensorsdone"):
        time.sleep(12   )
        while True:
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD, b'\x00\x00\x00')
            print("READ")
            print(mem_area)

            last_4_bytes = mem_area[-4:]
            integer_value = int.from_bytes(last_4_bytes, byteorder='big', signed=False)
            integer_value= bin(integer_value)[2:]
            print("Binary representation of the last 4 bytes:", integer_value)
            bit_index = 4
            bitmask = 1
            bitmask = int(integer_value[bit_index])
            
            print(bitmask)

            if(bitmask == 0):
                #log("DONE")
                send_command("[3]sensorsDONE")
                send_command("[5]done")
                break

    elif (received_message == "turntable"):
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
            print("READ")
            print(mem_area)

            last_4_bytes = mem_area[-4:]
            integer_value = int.from_bytes(last_4_bytes, byteorder='big', signed=False)

            print("Integer representation of the last 4 bytes:", integer_value)
            
            bit_position = 10
            bitmask = (1 << bit_position)

            result_after_and = integer_value | bitmask  
            print("RESULT After End : :")
            print(result_after_and)

            print("Type of integer_variable:", type(result_after_and))
            print("OUTPUT:")
            print(result_after_and)

            bytes_representation = result_after_and.to_bytes(2, byteorder='big')

            print("Bytes representation:", bytes_representation)
            message = bytes_representation
            print(message)

            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00', message, 1)
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
            print(mem_area)

    elif (received_message == "restart"):
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
            print("READ")
            print(mem_area)

            last_4_bytes = mem_area[-4:]
            integer_value = int.from_bytes(last_4_bytes, byteorder='big', signed=False)

            print("Integer representation of the last 4 bytes:", integer_value)
            
            bit_position = 13
            bitmask = ~(1 << bit_position)

            result_after_and = integer_value & bitmask  
            print("RESULT After End : :")
            print(result_after_and)

            print("Type of integer_variable:", type(result_after_and))
            print("OUTPUT:")
            print(result_after_and)

            bytes_representation = result_after_and.to_bytes(2, byteorder='big')

            print("Bytes representation:", bytes_representation)
            message = bytes_representation
            print(message)

            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00', message, 1)
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
            print(mem_area)

    elif (received_message == "start"):
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
            print("READ")
            print(mem_area)

            last_4_bytes = mem_area[-4:]
            integer_value = int.from_bytes(last_4_bytes, byteorder='big', signed=False)

            print("Integer representation of the last 4 bytes:", integer_value)
            
            bit_position = 13
            bitmask = (1 << bit_position)

            result_after_and = integer_value | bitmask  
            print("RESULT After End : :")
            print(result_after_and)

            print("Type of integer_variable:", type(result_after_and))
            print("OUTPUT:")
            print(result_after_and)

            bytes_representation = result_after_and.to_bytes(2, byteorder='big')

            print("Bytes representation:", bytes_representation)
            message = bytes_representation
            print(message)

            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00', message, 1)
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
            print(mem_area)

    elif (received_message == "rotate"):
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
            print("READ")
            print(mem_area)

            last_4_bytes = mem_area[-4:]
            integer_value = int.from_bytes(last_4_bytes, byteorder='big', signed=False)

            print("Integer representation of the last 4 bytes:", integer_value)
            
            bit_position = 11
            bitmask = (1 << bit_position)

            result_after_and = integer_value | bitmask  
            print("RESULT After End : :")
            print(result_after_and)

            print("Type of integer_variable:", type(result_after_and))
            print("OUTPUT:")
            print(result_after_and)

            bytes_representation = result_after_and.to_bytes(2, byteorder='big')

            print("Bytes representation:", bytes_representation)
            message = bytes_representation
            print(message)

            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00', message, 1)
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
            print(mem_area)

    elif (received_message == "ready"):
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
            print("READ")
            print(mem_area)

            last_4_bytes = mem_area[-4:]
            integer_value = int.from_bytes(last_4_bytes, byteorder='big', signed=False)

            print("Integer representation of the last 4 bytes:", integer_value)
            
            bit_position = 14
            bitmask = (1 << bit_position)

            result_after_and = integer_value | bitmask  
            print("RESULT After End : :")
            print(result_after_and)

            print("Type of integer_variable:", type(result_after_and))
            print("OUTPUT:")
            print(result_after_and)

            bytes_representation = result_after_and.to_bytes(2, byteorder='big')

            print("Bytes representation:", bytes_representation)
            message = bytes_representation
            print(message)

            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00', message, 1)
            mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
            print(mem_area)

    elif(received_message == "magnetoff"):

        mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
        print("READ")
        print(mem_area)

        #Encode that messages in binary mode
        binary_previous_message =  ''.join(format(byte, '08b') for byte in mem_area)
        print("BINARY PREVIOUS:" + binary_previous_message)
        binary_previous_16 = binary_previous_message[-16:]
        print("BINARY PREVIOUS 16:" + binary_previous_16)



        bit_position = 11
        # Clearing the bit at the specified position
        bitmask = ~(1 << bit_position)
        print("bitmask :")
        print(bitmask)



        binary_previous_16 = bin(binary_previous_16 & bitmask)
        print("OUTPUT:")                                               
        print(binary_previous_16)

        #FOR CHANGING FROM BINARY TO BYTES

        binary_previous_16= int(binary_previous_16, 2)
        message = binary_previous_16.to_bytes((binary_previous_16.bit_length() + 7) // 8, byteorder='big')
        #message = bytes(int(binary_previous_16[i:i+8], 2) for i in range(0, len((binary_previous_16)), 8))



        print(message)         


        fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00', message, 1)
        mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
        print(mem_area)
        
        

    elif(received_message == "pusheroff"):

        mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
        print("READ")
        print(mem_area)

        last_4_bytes = mem_area[-4:]
        integer_value = int.from_bytes(last_4_bytes, byteorder='big', signed=False)

        print("Integer representation of the last 4 bytes:", integer_value)
        
        bit_position = 6
        bitmask = ~(1 << bit_position)

        result_after_and = integer_value & bitmask  
        print("RESULT After End :")
        print(result_after_and)

        print("Type of integer_variable:", type(result_after_and))
        print("OUTPUT:")
        print(result_after_and)

        bytes_representation = result_after_and.to_bytes(2, byteorder='big')

        print("Bytes representation:", bytes_representation)
        message = bytes_representation
        print(message)

        fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00', message, 1)
        mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
        print(mem_area)

    elif(received_message == "stopconveyor"):

        mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
        print("READ")
        print(mem_area)

        #Encode that messages in binary mode
        binary_previous_message =  ''.join(format(byte, '08b') for byte in mem_area)
        print("BINARY PREVIOUS:" + binary_previous_message)
        binary_previous_16 = binary_previous_message[-16:]
        print("BINARY PREVIOUS 16:" + binary_previous_16)

        bit_position = 12
        # Clearing the bit at the specified position
        bitmask = ~(1 << bit_position)
        binary_previous_16 = int(binary_previous_16) & bitmask

        bit_position = 13
        # Clearing the bit at the specified position
        bitmask = ~(1 << bit_position)
        binary_previous_16 = binary_previous_16 & bitmask

        message = bytes(int(binary_previous_16[i:i+8], 2) for i in range(0, len(str(binary_previous_16)), 8))
        print(message)         


        fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00', message, 1)
        mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
        print(mem_area)

    else:    

        received_message = bytes.fromhex(received_message)
        print(received_message)

        #Previous message
        mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
        print("READ")
        print(mem_area)

        #Encode that messages in binary mode
        binary_previous_message =  ''.join(format(byte, '08b') for byte in mem_area)
        print("BINARY PREVIOUS:" + binary_previous_message)
        binary_previous_16 = binary_previous_message[-16:]
        print("BINARY PREVIOUS 16:" + binary_previous_16)

        binary_received_message = ''.join(format(byte, '08b') for byte in received_message)
        print("BINARY NEW:" + binary_received_message)

        #Make an OR between previous message and received message
        binary_OR =  ''.join('1' if b1 == '1' or b2 == '1' else '0' for b1, b2 in zip(binary_previous_16, binary_received_message))
        print("BINARY OR:" + binary_OR)

        #Encode that message in bytes format. For example: b'\x00\x02'
        message = bytes(int(binary_OR[i:i+8], 2) for i in range(0, len(binary_OR), 8))
        print(message)         


        fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00', message, 1)
        mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, b'\x00\x00\x00')
        print(mem_area)
        # time.sleep(2)


initialize()
#message_PLC("sensorscarrier")

while(True):
    command = wait_for_command()
    if((command == "3" )):
        log("Wrong communication")
    else:
        message_PLC(command)

