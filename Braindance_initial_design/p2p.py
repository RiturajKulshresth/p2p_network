from client import Client
from server import Server
import utils
import time
import random
import sys


class p2p:
    peers = ['127.0.0.1']


def main():

    while True:
        try:
            print("Trying to connect...")
            time.sleep(random.randint(1, 5))
            for peer in p2p.peers:
                try:
                    print("Trying client...")
                    client = Client(peer)
                except KeyboardInterrupt:
                    print("exiting client...")
                    sys.exit(0)
                except:
                    print("Pass client...")
                    pass

                try:
                    print("Trying server...")
                    server = Server()
                except KeyboardInterrupt:
                    print("exiting server...")
                    sys.exit(0)
                except:
                    print("Passing server...")
                    pass

        except KeyboardInterrupt as e:
            print("exiting app...")
            sys.exit(0)


if __name__ == "__main__":
    main()
