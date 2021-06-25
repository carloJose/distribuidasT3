import socket
import struct
import os
from threading import Thread

from delivery import Delivery as dy

class Comunication(Thread):

    def __init__(self, delivery_type, sock, IP = None, PORT = None, msg = None):
        Thread.__init__(self)
        self.delivery_type = delivery_type
        self.sock = sock
        self.IP = IP
        self.PORT = PORT
        self.msg = msg

    
    def run(self):

        if self.delivery_type == dy.RECIEVE:
             
            msg = self.sock.recv(1024)
            self.msg = msg
            print(msg)
        
        elif self.delivery_type == dy.SEND:
            self.sock.sendto(self.msg, (self.IP, self.PORT))
        
        else:
            i = 0
            while i < 5: 
                self.sock.sendto(b'1', ('127.0.0.1', '5002'))
                self._timer()
            
            self.msg = True

    def _timer(self):
        hit = range(100, 350)
        time(hit)
