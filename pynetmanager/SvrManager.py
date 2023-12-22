from multiprocessing import Queue
from typing import Tuple, Iterable
from socket import socket

from pynetmanager.RawSockManager import RawSockManager

from pynetmanager.NetCallback import NetCallback

class SvrManager(RawSockManager):
    '''
    Server Manager object; Capable of binding to an address, listening for
    clients, receiving from clients, and closing the connections.
    
    Parameters:
     - conn: Socket object of the server
     - addr: Address of the server, usually in (IP, PORT) form
     - bindCallbacks: Callbacks to run when server binds to the given address
     - connCallbacks: Callbacks to run when a client connects to the server
    '''
    def __init__(self, conn:socket, addr:Tuple,
                       bindCallbacks:Iterable[NetCallback] = [],
                       connCallbacks:Iterable[NetCallback] = []):
        super().__init__(True, conn, addr,
                         bindCallbacks, connCallbacks)
        self.recvQueues = {}
        self.clients = []
        self._connCallbacks.append(
            NetCallback(self.recv_from, self.recvQueues)
        )
    
    def bind(self, listenByDefault=True):
        '''
        Bind socket object to the given address.

        Parameters:
         - listenByDefault: If True, the server starts listening for
         client connections as soon as it binds. If False, `listen_and_accept`
         must be called manually
        '''
        if listenByDefault:
            self._bindCallbacks.append(
                NetCallback(self.listen_and_accept, [])
            )
        self._bind_or_connect()
    
    def listen_and_accept(self, conn:socket, addr:Tuple,
                                data:Iterable, queues:Iterable[Queue]):
        '''
        Listen for and accept clients. By default, this function is initiated
        automatically upon running `SvrManager.bind`, although this feature can
        be toggled. Upon accepting a client, all callbacks in
        `SvrManager.connCallbacks` are started in parallel processes.

        Parameters:
         - conn: This parameter is not accessed here; can be ommitted
         - addr: This parameter is not accessed here; can be ommitted
         - data: This parameter is not accessed here; can be ommitted
         - queues: This parameter is not accessed here; can be ommitted
        '''
        print("Listening...")
        self._conn.listen()
        while self._running:
            print("Running...")
            cliConn, cliAddr = self._conn.accept()
            self.clients.append((cliConn, cliAddr))
            self.recvQueues[(cliConn, cliAddr)] = Queue()
            for connCallback in self._connCallbacks:
                connCallback.start(cliConn, cliAddr, [])

    def recv_from(self, conn:socket, addr:Tuple,
                        data:Iterable, queues:Iterable[Queue]):
        '''
        Receive bytes from a client. This function is initiated
        automatically for any client connects to the server.

        Parameters:
         - conn: Socket object of the client
         - addr: Address of the client, usually in (IP, PORT) form
         - data: This parameter is not accessed here; can be ommitted
         - queues: Queues in which the received bytes are put
        '''
        print("Accepted {}...".format(addr))
        while self._running:
            recvData = conn.recv(1024)
            if recvData: queues[(conn, addr)].put(recvData)
    
    def close_cli(self, conn:socket, addr:Tuple, wipeRecvQueue:bool=False):
        '''
        Close a connection with a client.

        Parameters:
         - conn: Socket object of the client
         - addr: Address of the client, usually in (IP, PORT) form
         - wipeRecvQueue: If True, the client's associated `recvQueue` is closed, ergo it cannot be written to or read from
        '''
        conn.close()
        self.clients.remove((conn, addr))
        if wipeRecvQueue: self.recvQueues[(conn, addr)].close()
    
    def close_svr(self, wipeRecvQueues:bool=False):
        '''
        Close down the server. All client connections are terminated using
        `SvrManager.close_cli` before the server is closed.
        
        Parameters:
         - wipeRecvQueues: If True, all queues in `SvrManager.recvQueues` are closed, ergo they cannot be written to or read from
        '''
        for client in self.clients:
            self.close_cli(*client, wipeRecvQueues)
        self._conn.close()
