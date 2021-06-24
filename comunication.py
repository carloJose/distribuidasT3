import socket
import struct
import os
from threading import Thread

from delivery import Delivery as dy

class Comunication(Thread):

    def __init__(self, delivery_type, sock, IP, PORT, msg = None):
        Thread.__init__(self)
        self.delivery_type = delivery_type
        self.sock = sock
        self.IP = IP
        self.PORT = PORT
        self.msg = msg

    
    def run(self):

        if self.delivery_type == dy.RECIEVE:
             
            msg = self.sock.recv(1024 * 6)
            print(msg)
            self.msg = msg

        else:
            self.sock.sendto(self.msg, (self.IP, self.PORT))
