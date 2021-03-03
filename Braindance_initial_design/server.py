import socket
import threading
import utils
import sys

HEADER = 1024
SERVER = '127.0.0.1'
PORT = 5001
FORMAT = 'utf-8'
PEER_BYTE_DIFFERENTIATOR = b'\x11'


class Server:

    def __init__(self):
        # try:
        self.so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.conns = []
        self.peers = []

        self.so.bind((SERVER, PORT))
        self.so.listen()

        print("Server Listening...")
        self.start()

        # except Exception as e:
        #     print("ERROR: Cannot start server")
        #     sys.exit(0)

    def handleClient(self, conn, addr):
        try:
            while True:
                print("Receiving...")
                data = conn.recv(HEADER)

                for conn in self.conns:

                    if data and data.decode(FORMAT) == '!DIS':
                        self.disconnect(conn, addr)
                        return
                    elif data and data.decode(FORMAT) == '!SP':
                        peerList = ""
                        for peer in self.peers:
                            peerList = peerList + str(peer) + ","
                        conn.send(peerList.encode(FORMAT))
                    elif "|" in data.decode(FORMAT):
                        print("in here")
                        addrToSend = data.decode(FORMAT).split("|")[1]
                        msgToSend = data.decode(FORMAT).split("|")[0]
                        msgToSend = msgToSend.encode(FORMAT)
                        if str(conn.getpeername()) == addrToSend:
                            print("Sending....")
                            conn.send(msgToSend)
                        print("Message sent")
                    else:
                        print("Sending....")
                        conn.send(data)
                        print("Response sent")

        except Exception as e:
            print("ERROR in handling")
            sys.exit(0)

    def disconnect(self, conn, addr):
        conn.close()
        self.conns.remove(conn)
        self.peers.remove(addr)
        print(addr, " disconnected")
        print("Now, Current peers: ", self.peers)

    def sendPeers(self):
        peerList = ""
        print("Start sendpeers")
        for peer in self.peers:
            peerList = peerList + str(peer) + ","
            print("peer done")
            print(peerList)
        for conn in self.conns:
            print("connection started")
            data = PEER_BYTE_DIFFERENTIATOR + bytes(peerList, FORMAT)
            conn.send(PEER_BYTE_DIFFERENTIATOR +
                      bytes(peerList, FORMAT))

    def start(self):
        while True:
            conn, addr = self.so.accept()

            self.peers.append(addr)
            print("Current peers: ", self.peers)
            cthread = threading.Thread(
                target=self.handleClient, args=(conn, addr))
            cthread.daemon = True
            cthread.start()
            self.conns.append(conn)
            print(addr, " connected")
            print("Active connections: ", threading.activeCount() - 1)
