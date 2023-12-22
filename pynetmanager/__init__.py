"""
TODO:
- Network Callback:
  - Variables: Function to run (CONN, ADDR, DATA, QUEUES), Process running, Queues
  - Start Process
  - Force terminate process
- Raw Socket Manager:
  - Variables: Type (ie svr or cli), Locking Socket, Locking Address, Binding Callbacks, Connection Callbacks, Recv Callbacks
  - Bind or connect to given address
- Server Manager:
  - Variables: Own Socket, Own Address, Client Sockets, Client Addresses, Listener Process, Connection Callbacks, Recv Callbacks
  - Bind to given address
  - Listen and allow connection on thread; Preform callbacks on accept
  - Receive messages from client (bound by default as a callback); Perform callbacks on recv
  - Close individual socket
  - Close server
- Client Manager:
  - Variables: Server Address, Server Socket, Connection Callbacks, Recv Callbacks
  - Connect to given address; Preform callbacks on connection
  - Receive messages from server (bound by default as a callback); Perform callbacks on recv
  - Close socket
"""

from pynetmanager.NetCallback import *
from pynetmanager.RawSockManager import *
from pynetmanager.SvrManager import *
from pynetmanager.CliManager import *
