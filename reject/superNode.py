from node import Node

class superNode(Node):

    # self.peerList = []
    def __init__(self, host, port):
        super(superNode, self).__init__(host, port, None)
        print("superNode: Started")

        self.peerList = []

    def outbound_node_connected(self, node):
        print("outbound_node_connected: " + node.id)
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: " + node.id)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: " + node.id)

    def node_message(self, node, data):
        print("node_message from " + node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")
    
    def get_peers(self):
        self.peerList =self.nodes_inbound+self.nodes_outbound 
        return self.peerList
 