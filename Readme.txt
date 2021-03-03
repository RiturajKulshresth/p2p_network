Note: node.py and nodeconnection.py have been heavily modified

To create a peer to peer network first run the network.py
Then Run the appk_s.py
Then run the appk.py

appk_s.py is used here for sending the file 
However you can send from any file using node
create a copy of either the appk_s or appk file and put it in the system you want to run with 
remmenber to include the dependencies
node.py
nodeconnection.py
normalNode.py
superNode.py

We are using python 3.6.12, 3.8.3, 3.8.5 
If your system has an incompatible python version such that file paths are not found
please swich to 3.6.12 
or copy the dependencies to the folder 
recievingfile
second_reciever
Super Node
sender_File


The folder Initial structure shows our design of the network and is flawed and was our initial design only

To run 
run p2p.py which will run all the nodes 
you can send/recieve any message from command line 

to send to a particular client use this format
<msg | address>


