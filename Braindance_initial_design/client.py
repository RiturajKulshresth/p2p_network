import socket
import threading
import utils
import sys
import os
import signal

HEADER = 1024
SERVER = '127.0.0.1'
PORT = 5001
FORMAT = 'utf-8'
PEER_BYTE_DIFFERENTIATOR = b'\x11'


class Client:

    def __init__(self, addr):

        self.so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.so.connect((addr, PORT))

        self.peers = []

        self.prevData = None

        self.handleops()

    def handleops(self):
        try:
            ithread = threading.Thread(target=self.sendMessage)
            ithread.daemon = True
            ithread.start()

            while True:
                data = self.recvMessage()
                if not data:
                    print("Server Failed...")
                    break

                self.handleops()

        except KeyboardInterrupt:
            self.sendDisconnectMsg()

    def updatePeers(self, peers):
        self.peers = peers

    def recvMessage(self):
        try:
            print("Receiving...")
            data = self.so.recv(HEADER)
            print("Message received: ", data.decode(FORMAT))

            return data

        except KeyboardInterrupt:
            self.sendDisconnectMsg()

        # if self.prevData != data:
        #     utils.createFile(data)
        #     self.prevData = data

    def sendMessage(self):
        try:
            sendMsg = input()
            sendMsg = sendMsg.encode(FORMAT)
            self.so.send(sendMsg)

        except KeyboardInterrupt:
            self.sendDisconnectMsg()
            return
        except EOFError as e:
            self.sendDisconnectMsg()

    def sendDisconnectMsg(self):
        disMsg = '!DIS'
        self.so.send(disMsg.encode(FORMAT))
        print("Disconnected from server")
        os.kill(os.getppid(), signal.SIGHUP)
        sys.exit()
