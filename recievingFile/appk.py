import sys
import time
import os
import tqdm
import os.path
# sys.path.append()


sys.path.append("../Structure") # Adds higher directory to python modules path.

sys.path.insert(0,'/home/netrunner/Desktop/sem 6/CN project/pep_sth/Structure/') # Import the files where the modules are located

from normalNode import normalNode
from superNode import superNode

node_6 = normalNode("127.3.0.1", 8006)
node_7 = normalNode("127.0.4.1", 8007)
node_8 = normalNode("127.0.5.1", 8008)

# time.sleep(1)

node_6.start()
node_7.start()
node_8.start()

# time.sleep(1)

# node_1.connect_with_node('127.0.0.1', 8002)
node_6.connect_with_node('127.0.0.1', 8001)
node_7.connect_with_node('127.0.0.1', 8001)
node_7.connect_with_node('127.0.0.1', 8003)
node_7.connect_with_node('127.0.0.1', 8006)
node_8.connect_with_node('127.0.0.1', 8002)
node_8.connect_with_node('127.0.0.1', 8007)
node_8.connect_with_node('127.0.0.1', 8001)

# print("Current peer list for normalnode 6 ",node_6.all_nodes())
# print("Current peer list for normalnode 7 ",node_7.all_nodes())
# print("Current peer list for normalnode 8 ",node_8.all_nodes())




# node_1.get_peers()


# time.sleep(2)
# node_6.send_to_nodes("message: Hi there!")
# print(node_6.get_peers())
# time.sleep(5)


# progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
# with open(filename, "wb") as f:
#     while True:
#         # read 1024 bytes from the socket (receive)
#         bytes_read = client_socket.recv(BUFFER_SIZE)
#         if not bytes_read:    
#             # nothing is received
#             # file transmitting is done
#             break
#         # write to the file the bytes we just received
#         f.write(bytes_read)
#         # update the progress bar
#         progress.update(len(bytes_read))

# close the client socket
# client_socket.close()
# close the server socket
# s.close()





# node_1.stop()
# node_2.stop()
# node_3.stop()
print('end test')
# sys.exit(0)
# time.sleep(20)