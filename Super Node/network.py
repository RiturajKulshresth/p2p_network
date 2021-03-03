import sys
import time
import os
import tqdm

BUFFER_SIZE = 4096 # send 4096 bytes each time step
SEPARATOR = "<SEPARATOR>"

sys.path.append("../Structure") # Adds higher directory to python modules path.

sys.path.insert(0,'/home/netrunner/Desktop/sem 6/CN project/pep_sth/Structure/') # Import the files where the modules are located

from normalNode import normalNode
from superNode import superNode


node_1 = superNode("192.168.1.104", 8001)
# node_2 = normalNode("127.0.0.1", 8002)
# node_3 = normalNode("127.0.0.1", 8003)
# node_4 = normalNode("127.0.0.1", 8004)

# time.sleep(1)

node_1.start()
# node_2.start()
# node_3.start()
# node_4.start()
# time.sleep(1)

# node_1.connect_with_node('127.0.0.1', 8002)
# node_2.connect_with_node('127.0.0.1', 8001)
# # node_2.connect_with_node('127.0.0.1', 8003)
# # node_3.connect_with_node('127.0.0.1', 8002)
# node_3.connect_with_node('127.0.0.1', 8001)
# node_4.connect_with_node('127.0.0.1', 8001)

# node_1.get_peers()



# time.sleep(2)
# node_1.send_to_nodes("message: Hi there!")
print("Current peer list for supernode 1 ",node_1.get_peers())
# time.sleep(5)

# node_1.stop()
# node_2.stop()
# node_3.stop()
print('end test')
# sys.exit(0)
time.sleep(80)
print("Current peer list for supN",node_1.get_peers())
# node_1.send_to_nodes("message: Hi there!")

filename = "dataaa.csv"
filesize = os.path.getsize(filename)
node_1.send_to_nodes(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024, miniters=1, smoothing=1)
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        # we use sendall to assure transimission in 
        # busy networks
        progress.update(len(bytes_read))
        node_1.send_to_nodes(bytes_read)
        # update the progress bar
        # close the socket
progress.refresh()
print("File recieved")



print("Current peer list for supN",node_1.get_peers())
