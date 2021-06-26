import socket
import struct
import os
import time

from storage import Storage stg
from threading import Thread
from delivery import Delivery as dy
from comunication import Comunication as com


class Postman(Thread):
    

    def __init__(self, threadID, counterEvents, IP, PORT, MCAST_GRP, MCAST_PORT):
        Thread.__init__(self)
        self.threadID = threadID
        self.counterEvents = 0
        self.IP = IP
        self.PORT = PORT
        self.sock_uni = None
        self.sockTop = None
        self.MCAST_GRP = MCAST_GRP 
        self.MCAST_PORT = MCAST_PORT
        self._msgs = None
        self._start = set()
        self.storage = None
    
    def run(self):

        self._config_nodo_mult()
        self._config_nodo_uni()
        
        while True:
            self._recieve()
            go = b'0:GO' in list(self._start)
            print(go)
            print(self._start)
            if len(self._start)>1 or go :
                break

        if self.threadID == 0:
            self._send_mensage('GO')
        print("Vamo dale")

        finish = self.event()
        print(finish)

    def event(self):
            even = com(dy.EVENT, self.sock_uni)
            even.start()

            lis = com(dy.RECIEVE, self.sock_uni)
            lis.start()

            even.join()
            lis.join()
            
            while even.msg is None:
                pass
            
            return True

    def _config_nodo_mult(self):

        MCAST_GRP = self.MCAST_GRP #'224.1.1.1'
        MCAST_PORT = self.MCAST_PORT #5007
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', MCAST_PORT))
        mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.sockTop = sock
        ready_msg = 'OK'
        self._send_mensage(ready_msg)

    def _config_nodo_uni(self):

        MCAST_GRP = self.IP #'224.1.1.1'
        MCAST_PORT = self.PORT #5007
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.bind(('', MCAST_PORT))
        #sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.sock_uni = sock
        

    def _setup(self):
        data_aux = None
        with open('config.txt','r') as file:
            data_aux = file.read_lines()

        self.storage = stg()
        for i in data_aux:
            format_info = i.split(' ')
            self.storage.add_node_info(format_info)
        # TODO set storage to a singleton object


    def _send_mensage(self, msg, IP='224.1.1.1', PORT=5007):
        msg_formated = str(self.threadID) +':' + msg
        msg_byte = bytes(msg_formated, 'utf_8')
        snd = com(dy.SEND, self.sockTop, IP, PORT, msg_byte)
        snd.start()


    def _recieve(self, IP='224.1.1.1', PORT=5007):
        
        recv = com(dy.RECIEVE, self.sockTop, IP, PORT)
        recv.start()
        recv.join()
        if len(self._start)>1:
            print(recv.msg)
        else:
            self._start.add(recv.msg)
