# Imports
import socket, time
from threading import Thread
from kubernetes import client, config

class GossipNode:
    # pass the port of the node and the ports of the nodes connected to it
    def __init__(self, port):
        # create a new socket instance
        self.node = socket.socket()
        self.previous_message = ''

        # kubernetes service name
        # this is hard coded initially
        self.service_name = 'bcgossip'

        # set the address, i.e(hostname and port) of the socket
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port

        # bind the address to the socket created (TCP)
        try:
            self.node.bind((self.host, self.port))
        except socket.error as e:
            print(str(e), flush=True)

        # Start listening
        print(f'Server ({self.host}) is listening on the port {port}...', flush=True)
        self.node.listen()

        # set the ports of the nodes connected to it as susceptible nodes
        # empty node as all nodes are not established yet
        self.susceptible_nodes = []

        # call the threads to begin the magic
        self.start_threads()
        # self.start_server()

    def receive_message(self):

        while True:
            client, address = self.node.accept()
            if client:

                # print(f'Connected to: ({address[0]}:{address[1]})', flush=True)
                # Waiting for client message
                data = client.recv(2048)
                message = data.decode('utf-8')

                # if the node has already received the message
                # skip it
                if self.previous_message == message:
                    print(f'Node({self.host}:{self.port}) already received! from({address[0]}:{address[1]}) :{message}', flush=True)
                    client.close()
                    continue

                # getting message from client or other node
                self.previous_message = message

                # Close client connection
                client.close()
                # print(f'Disconnected from: ({address[0]}:{address[1]})', flush=True)

                # Initiating gossip from a node
                if self.host == address[0]:
                    print(f'Node({self.host}:{self.port}) is initiating gossip.. :{message}', flush=True)

                    # Previous node IP is the host itself
                    prev_node = self.host
                # Receiving message other susceptible(connected) nodes 
                else:
                    # Getting previous node IP
                    prev_node = address[0]

                    # Message received acknowledged
                    print(f'Node({self.host}:{self.port}) received message from({address[0]}:{address[1]}) :{message}', flush=True)

                # sleep for 2 seconds in order to show difference in time
                # time.sleep(1)

                # Transmitting message to other susceptible(connected) nodes
                self.transmit_message(message, prev_node)

    def transmit_message(self,msg_to_forward,previous_node=0):

        # Getting all the nodes(pods in k8s) IP addr in the neighbourhood
        self.get_neighbours()
        
        # Get next node to transfer the message
        for i in range(len(self.susceptible_nodes)):
            selected_node = self.susceptible_nodes[i]

            # if the selected node is where the message(s) comes from
            # skip it
            if selected_node == previous_node:
                continue

            nodeSocket = socket.socket()
            try:
                # Connecting to server
                nodeSocket.connect((selected_node, self.port))

                # If successful, send the message
                nodeSocket.send(str.encode(msg_to_forward))

                # Once the socket send the message and no error is displayed
                # It is assume that a message has been send successfully
                # no need for server response and server will terminate the connection
                print(f'Transmitting msg from({self.host}) to({selected_node}) :{msg_to_forward}', flush=True)
            except socket.error as e:
                print(str(e),flush=True)

    def start_threads(self):
        # two threads for entering and getting a message.
        # it will enable each node to be able to
        # enter a message and still be able to receive a message
        #Thread of receiving message
        Thread(target=self.receive_message).start()

    def get_neighbours(self):
        # this function will get list of nodes neighbour
        # from kubernetes API
        config.load_incluster_config()
        v1 = client.CoreV1Api()
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            if (i.metadata.labels):
                for k,v in i.metadata.labels.items():
                    if (k=='run') and (v==self.service_name):
                        if (self.host==i.status.pod_ip):
                            # skip and don't add IPaddr of its own
                            continue
                        else:
                            # add negihbour IPaddr to list
                            self.susceptible_nodes.append(i.status.pod_ip)