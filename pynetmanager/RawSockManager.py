from typing import Tuple, Iterable
from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, SOCK_RAW

from pynetmanager.NetCallback import NetCallback

def deafult_socket_inet_stream(): return socket(AF_INET, SOCK_STREAM)
def deafult_socket_inet6_stream(): return socket(AF_INET6, SOCK_STREAM)
def deafult_socket_inet_raw(): return socket(AF_INET, SOCK_RAW)
def deafult_socket_inet6_raw(): return socket(AF_INET6, SOCK_RAW)

class RawSockManager:
    def __init__(self, isSvr:bool, conn:socket, addr:Tuple,
                       bindCallbacks:Iterable[NetCallback] = [],
                       connCallbacks:Iterable[NetCallback] = []):
        self.__isSvr = isSvr
        self._conn = conn
        self._addr = addr
        self._bindCallbacks = bindCallbacks
        self._connCallbacks = connCallbacks
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

            
