import socket
import sys
import time
import threading
import random
import hashlib
import json
import os
import tqdm

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

class NodeConnection(threading.Thread):
    """The class NodeConnection is used by the class Node and represent the TCP/IP socket connection with another node. 
       Both inbound (nodes that connect with the server) and outbound (nodes that are connected to) are represented by
       this class. The class contains the client socket and hold the id information of the connecting node. Communication
       is done by this class. When a connecting node sends a message, the message is relayed to the main node (that created
       this NodeConnection in the first place).
       
       Instantiates a new NodeConnection. Do not forget to start the thread. All TCP/IP communication is handled by this 
       connection.
        main_node: The Node class that received a connection.
        sock: The socket that is assiociated with the client connection.
        id: The id of the connected node (at the other side of the TCP/IP connection).
        host: The host/ip of the main node.
        port: The port of the server of the main node."""

    def __init__(self, main_node, sock, id, host, port):
        """Instantiates a new NodeConnection. Do not forget to start the thread. All TCP/IP communication is handled by this connection.
            main_node: The Node class that received a connection.
            sock: The socket that is assiociated with the client connection.
            id: The id of the connected node (at the other side of the TCP/IP connection).
            host: The host/ip of the main node.
            port: The port of the server of the main node."""

        super(NodeConnection, self).__init__()
        self.filenamee=''
        self.host = host
        self.port = port
        self.main_node = main_node
        self.sock = sock
        self.terminate_flag = threading.Event()

        # The id of the connected node
        self.id = id

        # End of transmission character for the network streaming messages.
        self.EOT_CHAR = 0x04.to_bytes(1, 'big')

        # Datastore to store additional information concerning the node.
        self.info = {}

        self.main_node.debug_print("NodeConnection.send: Started with client (" + self.id + ") '" + self.host + ":" + str(self.port) + "'")

    def send(self, data, encoding_type='utf-8'):
        """Send the data to the connected node. The data can be pure text (str), dict object (send as json) and bytes object.
           When sending bytes object, it will be using standard socket communication. A end of transmission character 0x04 
           utf-8/ascii will be used to decode the packets ate the other node."""
        if isinstance(data, str):
            self.sock.sendall( data.encode(encoding_type) + self.EOT_CHAR )

        elif isinstance(data, dict):
            try:
                json_data = json.dumps(data)
                json_data = json_data.encode(encoding_type) + self.EOT_CHAR
                self.sock.sendall(json_data)

            except TypeError as type_error:
                self.main_node.debug_print('This dict is invalid')
                self.main_node.debug_print(type_error)

            except Exception as e:
                print('Unexpected Error in send message')
                print(e)

        elif isinstance(data, bytes):
            bin_data = data + self.EOT_CHAR
            self.sock.sendall(bin_data)

        else:
            self.main_node.debug_print('datatype used is not valid plese use str, dict (will be send as json) or bytes')

    # This method should be implemented by yourself! We do not know when the message is
    # correct.
    # def check_message(self, data):
    #         return True

    # Stop the node client. Please make sure you join the thread.
    def stop(self):
        """Terminates the connection and the thread is stopped."""
        self.terminate_flag.set()

    def parse_packet(self, packet):
        """Parse the packet and determines wheter it has been send in str, json or byte format. It returns
           the according data."""
        try:
            packet_decoded = packet.decode('utf-8')

            try:
                return json.loads(packet_decoded)

            except json.decoder.JSONDecodeError:
                return packet_decoded

        except UnicodeDecodeError:
            return packet

    # Required to implement the Thread. This is the main loop of the node client.
    def run(self):
        """The main loop of the thread to handle the connection with the node. Within the
           main loop the thread waits to receive data from the node. If data is received 
           the method node_message will be invoked of the main node to be processed."""
        self.sock.settimeout(10.0)          
        buffer = b'' # Hold the stream that comes in!

        while not self.terminate_flag.is_set():
            chunk = b''

            try:

                # file=open("recv.txt","wb")
                """Changed CHunk herer"""
                chunk = self.sock.recv(4096) 
                # while chunk:
                #     file.write(chunk)
                #     chunk=self.sock.recv(4096)

               

                # if (self.main_node.message_count_recv==0|self.main_node.message_count_recv==1):
                #     print()
                #     print("First!!!! ", len(chunk) ,chunk)


                # print(chunk)
               # print (chunk)
                # print (self.main_node.message_count_recv)
                # print
                # if (self.main_node.message_count_recv==0):

                #     chunk2 = chunk.decode()
                #     filename, filesizer = chunk2.split(SEPARATOR)
                #     print(filename,filesizer)
                #     filename= os.path.basename(filename)
                #     print("scaat")
                #     try:
                #         filesizee= int(filesizer)
                #         print("caat")
                #     except Exception as e:
                #         print(e)


                # else:
                #     with open(filename, "wb") as f:
                #         while True:
                #             # read 1024 bytes from the socket (receive)
                #             bytes_read = self.sock.recv(BUFFER_SIZE)
                #             if not bytes_read:    
                #                 # nothing is received
                #                 # file transmitting is done
                #                 break
                #             # write to the file the bytes we just received
                #             f.write(bytes_read)
                #             # update the progress bar
                #             # progress.update(len(bytes_read))
                # self.main_node.message_count_recv += 1


            except socket.timeout:
                self.main_node.debug_print("NodeConnection: timeout")

            except Exception as e:
                self.terminate_flag.set()
                self.main_node.debug_print('Unexpected error')
                self.main_node.debug_print(e)

            # BUG: possible buffer overflow when no EOT_CHAR is found => Fix by max buffer count or so?
            if chunk != b'':
                buffer += chunk
                eot_pos = buffer.find(self.EOT_CHAR)
                # print("           EOTPOS          ",eot_pos)
                # # if (self.main_node.message_count_recv==0|self.main_node.message_count_recv==1):
                # #         print()
                # #         print("second!!!! ", len(chunk) ,chunk)
                temp_chunk=chunk.decode()
                if not (temp_chunk.endswith("\x04")): 
                    temp_chunk=temp_chunk+"\x04"
                    chunk=temp_chunk.encode()

                while (eot_pos > 0) :
                    # if (self.main_node.message_count_recv==0|self.main_node.message_count_recv==1):
                    #     print()
                    #     print("third!!!!", len(chunk) ,chunk)

                    packet = buffer[:eot_pos]
                    buffer = buffer[eot_pos + 1:]
                    # chunk=chunk[:eot_pos]
                    # print(chunk)
                    

                    # print(len(chunk))

                    # if (self.main_node.message_count_recv==0):

                    #     chunk2 =chunk.decode()
                    #     filename, filesizer = chunk2.split(SEPARATOR)
                    #     # print(filename,filesizer)
                    #     filename= os.path.basename(filename)
                    #     # print("scaat")
                    #     try:
                    #         filesizee= int(filesizer)
                    #         # print("caat")
                    #     except Exception as e:
                    #         print(e)
                    # else:
                    #     progress = tqdm.tqdm(range(filesizee), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024,)
                    #     with open(filename, "ab") as f:
                    #         f.write(chunk)
                    #         # progress.update(len(chunk))
                    #         # while True:
                    #             # read 1024 bytes from the socket (receive)
                    #             # bytes_read = self.sock.recv(BUFFER_SIZE)
                    #             # if not bytes_read:    
                    #             #     # nothing is received
                    #             #     # file transmitting is done
                    #             #     break
                    #             # write to the file the bytes we just received
                    #             # update the progress bar
                    #             # progress.update(len(bytes_read))
                    #     # progress.refresh()

                    self.reciever_f(chunk, self.main_node.message_count_recv, eot_pos)
                    # print("sent to the reciever f")
                    # print(self.main_node.message_count_recv)

                    self.main_node.message_count_recv += 1
                    # self.main_node.node_message( self, self.parse_packet(packet) )
                    # print (packet)
                    eot_pos = buffer.find(self.EOT_CHAR)
                
            # time.sleep(0.01)
            # self.sock.close()
        # IDEA: Invoke (event) a method in main_node so the user is able to send a bye message to the node before it is closed?

        self.sock.settimeout(None)
        self.sock.close()
        self.main_node.debug_print("NodeConnection: Stopped")

    def set_info(self, key, value):
        self.info[key] = value

    def get_info(self, key):
        return self.info[key]

    def __str__(self):
        return 'NodeConnection: {}:{} <-> {}:{} ({})'.format(self.main_node.host, self.main_node.port, self.host, self.port, self.id)

    def __repr__(self):
        return '<NodeConnection: Node {}:{} <-> Connection {}:{}>'.format(self.main_node.host, self.main_node.port, self.host, self.port)


    def reciever_f(self, chunk, mess_c, eot_pos):
        # print("mess_c",mess_c)
        # print(chunk)
        if (mess_c==0):
            chunky=chunk[:eot_pos]
            # print("chunky",chunky)
            chunk2 =chunky.decode()
            filename, filesizer = chunk2.split(SEPARATOR)
            # print("filename", filenamee)
            self.filenamee= os.path.basename(filename)
            mess_c+=1
            # print(type(filesizer),int(filesizer))
            # filesizee= int(filesizer)

            try:
                filesizee= int(filesizer.strip("\x04"))
            except Exception as e:
                print("ct")
                print("cat",e)
        else:
            # progress = tqdm.tqdm(range(filesizee), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            chunky=chunk[:eot_pos]
            chunk2 =chunky.decode()
            print(os.getcwd())
            with open(self.filenamee+"cat", "wb") as f:
                f.write(chunky)
                # progress.update(len(chunk))
                    # progress.update(len(bytes_read))
            # progress.refresh()