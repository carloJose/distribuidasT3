import socket
import struct
import os
import time
import random

from storage import Storage as stg
from threading import Thread
from delivery import Delivery as dy

class Comunication(Thread):

    def __init__(self, delivery_type, sock, thread_id, IP = None, PORT = None, msg = None):
        Thread.__init__(self)
        self.delivery_type = delivery_type
        self.sock = sock
        self.IP = IP
        self.PORT = PORT
        self.msg = msg
        self.thread_id = thread_id
        self.stg = stg()
        

    
    def run(self):

        if self.delivery_type == dy.RECIEVE:
            if self.IP is not None:
                print('Listening Multicast...')
            else:
                print('Listening...')
                
            while True:
                msg = self.sock.recv(4096)
                self.msg = msg
                print(msg)
                if self.IP is not None:
                    break
        
        elif self.delivery_type == dy.SEND:
            self.sock.sendto(self.msg, (self.IP, self.PORT))
        
        else:
            i = 0
            done = int(self.stg.get_data_by_index(self.thread_id)[3])
            print(' Lets send {} msgs'.format(done))
            while i < done:
                
                ip_dest = self.select_destination()[0]
                port_dest = int(self.select_destination()[1])
                origin_ip = self.stg.get_data_by_index(self.thread_id)[0]
                origin_port = int(self.stg.get_data_by_index(self.thread_id)[1])
                
                if ip_dest == origin_ip and port_dest == origin_port:
                    print('igual')
                    
                else:
                    msg_to_send = 'from ip: {} port: {} test: {}'.format(origin_ip, origin_port, i)
                    self.sock.sendto(bytes(msg_to_send, 'utf_8'), (ip_dest, port_dest))
                    
                self._timer()
                i+=1
            
            raise Exception('Done')

    def _timer(self):
        
        min_d = float(self.stg.get_data_by_index(self.thread_id)[4])
        max_d = float(self.stg.get_data_by_index(self.thread_id)[5].replace('\n',''))
        hit = random.randint(min_d, max_d)
        time.sleep(hit*0.001)
    
    def select_destination(self):
        max_chance = None
        hit = random.uniform(0,1)
        
        for i in self.stg.data:
            chance = float(i[2])
            if hit < chance:
                return i[:2]
            
            if max_chance is None or chance > float(max_chance[2]):
                max_chance = i
                    

        return max_chance[:2]
