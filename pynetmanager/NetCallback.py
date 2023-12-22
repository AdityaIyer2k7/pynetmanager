from threading import Thread
from multiprocessing import Queue
from typing import Callable, Iterable, Tuple
from socket import socket

class NetCallback:
    def __init__(self, func:Callable, queues:Iterable[Queue]):
        self.func = func
        self.process = None
        self.queues = queues
    
    def start(self, conn:socket, addr:Tuple, data:Iterable):
        self.process = Thread(target=self.func, args=(conn, addr, data, self.queues))
        self.process.start()
    
    def stop(self):
        self.process.close()
    
    def forcestop(self):
        self.process.kill()
        self.process.close()
