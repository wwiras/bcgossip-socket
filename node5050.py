# import the GossipNode class
from GNode import GossipNode

# communication ports for this node
# for received messages
port = 5050

# Initialize node creation with empty list of neighbours    
# send port number 
node = GossipNode(port)