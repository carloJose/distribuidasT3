import socket
import struct
import os
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
      self.sockTop = None
      self.MCAST_GRP = MCAST_GRP 
      self.MCAST_PORT = MCAST_PORT
      self._msgs = None
      self._start = set()

    def run(self):

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
        
        while True:
            self._recieve()
            go = b'0:GO' in list(self._start)
            print(go)
            print(self._start)
            if len(self._start)>2 or go :
                break

        if self.threadID == 0:
            self._send_mensage('GO')
        print("feito")
    
    def event(self):
        pass

    def _send_mensage(self, msg, IP='224.1.1.1', PORT=5007):
        msg_formated = str(self.threadID) +':' + msg
        msg_byte = bytes(msg_formated, 'utf_8')
        snd = com(dy.SEND, self.sockTop, IP, PORT, msg_byte)
        snd.start()


    def _recieve(self, IP='224.1.1.1', PORT=5007):
        
        recv = com(dy.RECIEVE, self.sockTop, IP, PORT)
        recv.start()
        recv.join()
        self._start.add(recv.msg)
