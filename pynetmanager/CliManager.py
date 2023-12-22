from multiprocessing import Queue
from typing import Tuple, Iterable
from socket import socket

from .RawSockManager import RawSockManager

from .NetCallback import NetCallback

class CliManager(RawSockManager):
    def __init__(self, conn:socket, addr:Tuple,
                       connCallbacks:Iterable[NetCallback] = [],
                       recvCallbacks:Iterable[NetCallback] = []):
        super().__init__(True, conn, addr,
                         None, connCallbacks, recvCallbacks)
        self.recvQueue = Queue()
        self._connCallbacks.append(
            NetCallback(self.recv, [self.recvQueue])
        )
    
    def connect(self):
        self._bind_or_connect()
    
    def recv(self, conn:socket, addr:Tuple,
                   data:Iterable, queues:Iterable[Queue]):
        print("Connected to {}...".format(addr))
        while self._running:
            queues[0].put(conn.recv(1))
    
    def close(self, wipeQueue:bool=False):
        self._conn.close()
        if wipeQueue: self.recvQueue.close()