const net = require('net');
const WebSocket = require('ws');

const pythonServerAddress = '127.0.0.1';
const pythonServerPort = 10000;

let client;  // Declare the client variable

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  console.log('WebSocket connection established');
  
  ws.on('message', (message) => {
    console.log('Received message from interface:', message);

    // Connect to the Python server if not already connected
    if (!client || client.destroyed) {
      client = new net.Socket();
      client.connect(pythonServerPort, pythonServerAddress, () => {
        console.log('Connected to Python server');
        
      });

      client.on('data', (data) => {
        console.log('Received from Python server:', data.toString());
        // Process the received data from the Python server as needed
        // Send the received data to the connected clients
        wss.clients.forEach((client) => {
          if (client.readyState === WebSocket.OPEN) {
            client.send(data.toString());
          }
        });
      });

      client.on('close', () => {
        console.log('Connection to Python server closed');
      });
    }
    // Send the message to the Python server
    client.write(message);
  });

  ws.on('close', () => {
    console.log('WebSocket connection closed');
  });
});
