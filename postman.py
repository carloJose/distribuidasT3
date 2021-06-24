import socket
import struct
import os

class Postman:

    @staticmethod
    def send(sock):
         
        MCAST_GRP = '224.1.1.1'
        MCAST_PORT = 5007
        IS_ALL_GROUPS = True
        nome = input("diz teu nome ai: ")
        MESSAGE = bytes('{nome} entrou!'.format(nome=nome),'utf-8')
        # regarding socket.IP_MULTICAST_TTL
        # ---------------------------------
        # for all packets sent, after two hops on the network the packet will not
        # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
        MULTICAST_TTL = 1

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

        while True:
            sock.sendto(MESSAGE, (MCAST_GRP, MCAST_PORT))
            MESSAGE = bytes( "{nome} falou: ".format(nome=nome)+ input(''),'utf-8')
            if MESSAGE == exit:
                sock.close()
                os._exit(0)
        print("mandei a caralha")

    @staticmethod
    def receieve(sock):

        MCAST_GRP = '224.1.1.1'
        MCAST_PORT = 5007
        IS_ALL_GROUPS = True
        # on this port, receives ALL multicast groups
        sock.bind(('', MCAST_PORT))
        #else:
        # on this port, listen ONLY to MCAST_GRP
        #    sock.bind((MCAST_GRP, MCAST_PORT))
        mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            print(sock.recv(1024))