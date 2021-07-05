import socket
import struct
import os
import time
import pdb

from watch import Watch
from storage import Storage as stg
from threading import Thread
from delivery import Delivery as dy
from comunication import Comunication as com

# Organiza o nodo
class Postman(Thread):
    

    def __init__(self, threadID, MCAST_GRP, MCAST_PORT, counterEvents=0, IP=None, PORT=0000):
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
        self.watch_local = Watch()
    
    def run(self):

        self._setup()        
        self._config_nodo_mult()
        self._config_nodo_uni()
        # inicia o relogio vetorial com  zeros com espacos para todos os nodos previstos pelo arquivo de configuracao
        self.watch_local.watch = [0] * len(self.storage.data)
        try:
            while True:
                self._recieve()
                
                # quando nao é o nogo id zero, só inicia quando recebe o GO
                go = b'0:GO' in list(self._start)
                if len(self._start)>len(self.storage.data)-1 or go :
                    break

            if self.threadID == 0:
                # quando for id zero e ver que todos os nodos previstos entraram, envia o GO via multicast
                self._send_mensage('GO')
            print("Vamo dale")
            
            #pdb.set_trace()
            finish = self.event()
            print(finish)
            self.sock_uni.close()
            self.sockTop.close()
            raise Exception("Done")
            
        except:
            self.sock_uni.close()
            self.sockTop.close()
            exit()

    def event(self):
        # dispara os envios e o recebimento unicast
            even = com(dy.EVENT, self.sock_uni, self.threadID)
            even.start()

            lis = com(dy.RECIEVE, self.sock_uni, self.threadID)
            lis.start()
            even.join()
            
            return 'done'

    def _config_nodo_mult(self):
        # configura o socket multicast usando udp e Datagram
        MCAST_GRP = self.MCAST_GRP #'224.1.1.1'
        MCAST_PORT = self.MCAST_PORT #5007
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((MCAST_GRP, MCAST_PORT))
        sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY),
        )

        self.sockTop = sock
        ready_msg = 'OK'
        self._send_mensage(ready_msg)

    def _config_nodo_uni(self):
        # configura socket unicast
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.IP, self.PORT)
        s.bind(server_address)
        
        self.sock_uni = s
        

    def _setup(self):
        # faz o setup do arquivo de configuracao no storage
        data_aux = None
        with open('config.txt','r') as file:
            data_aux = file.readlines()

        self.storage = stg()
        for i in data_aux:
            format_info = i.split(' ')
            self.storage.add_node_info(list(format_info))
        
        IP_aux = self.storage.get_data_by_index(self.threadID)[0]
        PORT_aux = int(self.storage.get_data_by_index(self.threadID)[1])
        N_events_aux= (self.storage.get_data_by_index(self.threadID)[3])
        self.counterEvents = int(N_events_aux)
        self.IP = IP_aux
        self.PORT = int(PORT_aux)
        


    def _send_mensage(self, msg, IP='224.1.1.1', PORT=5007):
        # envia msg. Basicamente usado para multicast
        msg_formated = str(self.threadID) +':' + msg
        msg_byte = bytes(msg_formated, 'utf_8')
        snd = com(dy.SEND, self.sockTop, self.threadID, IP, PORT, msg_byte)
        snd.start()


    def _recieve(self, IP='224.1.1.1', PORT=5007):
        # recebe msg basicamente multicast
        recv = com(dy.RECIEVE, self.sockTop, self.threadID, IP, PORT)
        recv.start()
        recv.join()
        if len(self._start)>1:
            print(recv.msg)
        else:
            self._start.add(recv.msg)
