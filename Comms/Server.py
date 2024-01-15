import asyncio
import socket
import re

# Define the server address and port
ip_address = ""
port = 10000

# Define a list to keep track of connected clients
clients = {}

# Start server
def start_server():
    print("Initializing...")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen(5)

    print("Server is online")
    return server_socket

async def broadcast(message, not_to_client=None):
    print(f"Server to All: {message}")
    for client in clients:
        if not client == not_to_client:
            await send_message(client, message)

async def send_message(client, message):
    print(f"Server to Client [{clients[client]}]: {message}")
    client.send((f"{message}").encode())

async def incoming_message(client, message):
    message = message.decode()
    print(f"Client [{clients[client]}] to Server: {message}")

    if await is_command(message, client):
        return

    target_id, message = discover_id(message)
    if target_id is None:
        await broadcast(message, client)
        return

    for client_socket, client_id in clients.items():
        if client_id == target_id:
            await send_message(client_socket, message)
            break

def discover_id(message):
    message = message.strip()
    match = re.match(r'\[(\d+)\]', message)
    if match:
        message_without_id = re.sub(r'\[\d+\]', '', message).strip()
        return match.group(1), message_without_id
    else:
        return None, message

async def client_connected(client):
    client_id = (await loop.sock_recv(client, 1024)).decode().strip()
    clients[client] = client_id
    print(f"Client [{client_id}] connected")

async def console_log(message):
    for client_socket, client_id in clients.items():
        if client_id == "3":
            await send_message(client_socket, message)
            break

def client_disconnected(client):
    client.close()
    if client in clients:
        client_id = clients[client]
        del clients[client]
        print(f"Client [{client_id}] disconnected")

async def handle_client(client):
    try:
        await client_connected(client)
        while True:
            try:
                data = await loop.sock_recv(client, 1024)
                if not data:
                    break
                await incoming_message(client, data)
            except ConnectionResetError:
                break
    except asyncio.CancelledError:
        pass
    finally:
        client_disconnected(client)

async def is_command(response, client):
    target_id, response = discover_id(response)
    if response == "status":
        if target_id is None:
            return False

        for client_socket, client_id in clients.items():
            if client_id == target_id:
                await send_message(client, f"status({target_id}):true")
                return True
        await send_message(client, f"status({target_id}):false")
        return True

    return False

async def main():
    server_socket = start_server()
    print("Waiting for clients...")

    while True:
        client, address = await loop.sock_accept(server_socket)
        asyncio.create_task(handle_client(client))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
