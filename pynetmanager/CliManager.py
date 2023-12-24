from multiprocessing import Queue
from threading import Thread
from typing import Tuple, Iterable
from socket import socket

from pynetmanager.RawSockManager import RawSockManager

from pynetmanager.NetCallback import NetCallback

class CliManager(RawSockManager):
    '''
    Client Manager object; Capable of connecting to a server, receiving
    from the server, and closing the connection.
    
    Parameters:
     - conn: Socket object of the client
     - addr: Address of the server, usually in (IP, PORT) form
     - connCallbacks: Callbacks to run when the client connects to the server
    '''
    def __init__(self, conn:socket, addr:Tuple,
                       connCallbacks:Iterable[NetCallback] = []):
        super().__init__(True, conn, addr,
                         None, connCallbacks)
        self.recvQueue = Queue()
        self._connCallbacks.append(
            NetCallback(self.recv, [self.recvQueue])
        )
    
    def connect(self):
        '''
        Connect socket object to the given address. Upon connecting, all
        callbacks in `CliManager.connCallbacks` are started in parallel
        processes.
        '''
        self._bind_or_connect()
    
    def recv(self, conn:socket, addr:Tuple,
                   data:Iterable, queues:Iterable[Queue]):
        '''
        Receive bytes from the server. This function is initiated
        automatically for when the client connects to the server.

        Parameters:
         - conn: Socket object of the client
         - addr: Address of the client, usually in (IP, PORT) form
         - data: This parameter is not accessed here; can be ommitted
         - queues: Queues in which the received bytes are put
        '''
        print("Connected to {}...".format(addr))
        while self._running:
            recvData = conn.recv(1)
            queues[0].put(recvData)
    
    def send(self, message:bytes, blocking:bool=True):
        if not blocking:
            self._conn.send(message)
            return None
        else:
            thread = Thread(target=self._conn.send, args=(message,))
            thread.start()
            return thread

    def close(self, wipeRecvQueue:bool=False):
        '''
        Close the connection with the serevr.

        Parameters:
         - wipeRecvQueue: If True, the `recvQueue` is closed, ergo it cannot be written to or read from
        '''
        self._conn.close()
        if wipeRecvQueue: self.recvQueue.close()
