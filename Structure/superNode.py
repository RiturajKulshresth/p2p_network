from node import Node

class superNode(Node):

    # self.peerList = []
    def __init__(self, host, port):
        super(superNode, self).__init__(host, port, None)
        print("superNode: Started")

        self.peerList = []
        self.nodeList=[]
        self.portList=[]

    def outbound_node_connected(self, node):
        print("outbound_node_connected: " + str(node.host) + ":" + str(node.port))
        self.nodeList.append(str(node.host))
        self.portList.append(str(node.port))
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: " + str(node.host) + ":" + str(node.port))
        self.nodeList.append(str(node.host))
        self.portList.append(str(node.port))
    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: " + str(node.host) + ":" + str(node.port))

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: " + str(node.host) + ":" + str(node.port))

    def node_message(self, node, data):
        print("node_message from " + str(node.host) + ":" + str(node.port) + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: " + str(node.host) + ":" + str(node.port))
        
    def node_request_to_stop(self):
        print("node is requested to stop!")
    
    def get_peers(self):
        self.peerList =self.nodes_inbound+self.nodes_outbound 

        return self.peerList
    
    def send_peers_to(self, node):
        li=self.get_peers()
        self.send_to_node(node,li)
        # return self.connected_peers
    
    def get_deets(self):
        print(self.nodeList)
        print(self.portList)

    