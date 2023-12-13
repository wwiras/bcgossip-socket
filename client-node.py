import socket

host=socket.gethostbyname(socket.gethostname())
port = 5050

# host = input('Your target server (IP addr):')
print(f'Initiating gossip from ({host}) ....', flush=True)
msg = input('Type message:')

clientSocket = socket.socket()
try:
    # Connecting to server
    clientSocket.connect((host, port))

    # If successful, send the message
    # Default message is used and can be changed afterward
    # Input = "This is a standard message"
    clientSocket.send(str.encode(msg))

    # Once the socket send the message and no error is displayed
    # It is assumed that a message has been send successfully
    # No need for server response and server will terminate the connection
    print(f'Message is sent and connection is closed by the ({host})', flush=True)

except socket.error as e:
    print(str(e),flush=True)
