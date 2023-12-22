from typing import Tuple, Iterable
from socket import socket

from .NetCallback import NetCallback

class RawSockManager:
    def __init__(self, isSvr:bool, conn:socket, addr:Tuple,
                       bindCallbacks:Iterable[NetCallback] = [],
                       connCallbacks:Iterable[NetCallback] = [],
                       recvCallbacks:Iterable[NetCallback] = []):
        self.__isSvr = isSvr
        self._conn = conn
        self._addr = addr
        self._bindCallbacks = bindCallbacks
        self._connCallbacks = connCallbacks
        self._recvCallbacks = recvCallbacks
        self._running = False

    def _bind_or_connect(self):
        self._running = True
        if self.__isSvr:
            self._conn.bind(self._addr)
            for bindCallback in self._bindCallbacks:
                bindCallback.start(self._conn, self._addr, [])
        else:
            self._conn.connect(self._addr)
            for connCallback in self._connCallbacks:
                connCallback.start(self._conn, self._addr, [])

            
