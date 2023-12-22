from multiprocessing import Queue
from typing import Tuple, Iterable
from socket import socket

from .RawSockManager import RawSockManager

from .NetCallback import NetCallback

class SvrManager(RawSockManager):
    def __init__(self, conn:socket, addr:Tuple,
                       bindCallbacks:Iterable[NetCallback] = [],
                       connCallbacks:Iterable[NetCallback] = [],
                       recvCallbacks:Iterable[NetCallback] = []):
        super().__init__(True, conn, addr,
                         bindCallbacks, connCallbacks, recvCallbacks)
        self.recvQueues = {}
        self.clients = []
        self._bindCallbacks.append(
            NetCallback(self.listen_and_accept, [])
        )
        self._connCallbacks.append(
            NetCallback(self.recv_from, self.recvQueues)
        )
    
    def bind(self):
        self._bind_or_connect()
    
    def listen_and_accept(self, conn:socket, addr:Tuple,
                                data:Iterable, queues:Iterable[Queue]):
        print("Listening...")
        conn.listen()
        while self._running:
            print("Running...")
            cliConn, cliAddr = conn.accept()
            self.clients.append((cliConn, cliAddr))
            self.recvQueues[(cliConn, cliAddr)] = Queue()
            for connCallback in self._connCallbacks:
                connCallback.start(cliConn, cliAddr, [])

    def recv_from(self, conn:socket, addr:Tuple,
                        data:Iterable, queues:Iterable[Queue]):
        print("Accepted {}...".format(addr))
        while self._running:
            queues[(conn, addr)].put(conn.recv(1))
    
    def close_cli(self, conn:socket, addr:Tuple, wipeQueue:bool=False):
        conn.close()
        self.clients.remove((conn, addr))
        if wipeQueue: self.recvQueues[(conn, addr)].close()
    
    def close_svr(self, wipeQueues:bool=False):
        for client in self.clients:
            self.close_cli(*client, wipeQueues)
        self._conn.close()
