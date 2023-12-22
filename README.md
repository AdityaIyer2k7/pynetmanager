# pynetmanager
A FOSS library to simplify writing and handling sockets in Python. Includes INET and INET6 support, `bind`, `listen`, `accept`, `connect` API.

## Description
This repositiory contains the source code for the `pynetmanager` library. This is my second and (hopefully) better networking wrapper library, the first being [pyNetSocket](https://github.com/AdityaIyer2k7/pyNetSocket).

Improvements over `pyNetSocket`:
- Direct IPv6 support (through `AF_INET6`)
- Direct `SOCK_RAW` support
- Support functions to generate socket objects
- Use of threading to avoid blocking
- PEP8 compliance

## Installation
Install directly from `pip` using
```
pip install pynetmanager
```

or download the library from the [GitHub repo](https://github.com/AdityaIyer2k7/pynetmanager) using
```
git clone https://github.com/AdityaIyer2k7/pynetmanager
```

## Usage - Scripting

### Creating a Network Event Callback
Defining the function:
```py
def some_func(conn, addr, data, queues):
    '''
    This function will be called when a network event (binding or connection) occurs
    Parameters:
     - conn: The socket object linked to the event
     - addr: The other side's address
     - data: The miscellaneous data being passed to the function, either Iterable or None
     - queues: An iterable (list or dict) of queues between processes
    '''
    print(f"Address {addr} has connected")
```

Creating the callback:
```py
from pynetmanager import NetCallback
from multiprocessing import Queue

myQueues = [Queue(), Queue()]
callback = NetCallback(func=some_func, queues=myQueues)
```

Running the callback (using `someConn` and `someAddr`):
```py
callback.start(conn=someConn, addr=someAddr, data=None)
```
---

### Running a generic Server (AF_INET, SOCK_STREAM)
Setup the server:
```py
from pynetmanager import SvrManager, deafult_socket_inet_stream

server_socket = deafult_socket_inet_stream()
server_address = ("127.0.0.1", 5500)
server = SvrManager(server_socket, server_address)
```

Assign callbacks:
```py
# Bind Callbacks are called when the server binds to its address
myBindCallbacks = [bindCallback1, bindCallback2]

# Conn Callbacks are called when a client connects to the server
myConnCallbacks = [connCallback1, connCallback2, connCallback3]

# Always use '+=' to add two lists
# do NOT replace any server.xxxxCallbacks unless you know what you're doing
server.bindCallbacks += myBindCallbacks
server.connCallbacks += myConnCallbacks
```

Bind the server:
```py
# If `listenByDeault` is True, the server starts listening for and 
# accepting clients as soon as it binds to its address
server.bind(listenByDefault=False)
```

Listen for clients (Skip if you set `listenByDefault` as True):
```py
# This function does not require parameters
server.listen_and_accept(None, None, None, None)
```

To list connected clients:
```py
server.clients
# OUTPUT:
# [
#   (<socket.socket ...>, ('127.0.0.1', 65028)),
#   (<socket.socket ...>, ('127.0.0.1', 62157)),
#   ...
#   (conn, addr)
# ]
```

To access open queues
```py
server.recvQueues
# OUTPUT:
# {
#   (<socket.socket ...>, ('127.0.0.1', 65028)): <multiprocessing.queues.Queue ...>,
#   (<socket.socket ...>, ('127.0.0.1', 62157)): <multiprocessing.queues.Queue ...>,
#   ...
#   (conn, addr): <multiprocessing.queues.Queue ...>,
# }
```
---

### Running a generic Client (AF_INET, SOCK_STREAM)
Setup the client:
```py
from pynetmanager import CliManager, deafult_socket_inet_stream

client_socket = deafult_socket_inet_stream()
server_address = ("127.0.0.1", 5500) # Note that we use the server's address here since that is what we are connecting to
client = CliManager(client_socket, server_address)
```

Assign callbacks:
```py
# Conn Callbacks are called when the client connects to the server
myConnCallbacks = [connCallback1, connCallback2, connCallback3]

# Always use '+=' to add two lists
# do NOT replace any client.xxxxCallbacks unless you know what you're doing
client.connCallbacks += myConnCallbacks
```

Connect the client:
```py
client.bind()
```

To access the queue of received messages
```py
client.recvQueue
# OUTPUT:
# <multiprocessing.queues.Queue object at ...>
```
