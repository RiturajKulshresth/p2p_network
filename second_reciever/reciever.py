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

node_10 = normalNode("127.3.0.1", 8010)

node_10.start()
with open("cattat.csv", "ab") as f:
    f.write(b'cat')


node_10.connect_with_node('127.0.0.1', 8001)
node_10.connect_with_node('127.0.0.1', 8002)