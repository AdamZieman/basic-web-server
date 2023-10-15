from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket
serverSocket.bind(('127.0.0.1', 6789))
serverSocket.listen(1)

while True:
    # Establish a connection with a client
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        # Receive the HTTP request message from the client and decode it
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]

        # Open the requested file for reading
        f = open(filename[1:])                        
        outputdata = f.read()

        # Send an HTTP header to the client indicating a successful response (200 OK)
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(response.encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

    except IOError:
        # Handle the case where the requested file is not found
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(response.encode())

    finally:
        connectionSocket.close() # Close the client socket to end communication with the current client
        serverSocket.close() # Close the server socket to release the network resources
        sys.exit() # Terminate the program after handling the current request and cleaning up resources                                  