import threading
import socket
import struct

from postman import Postman as pst


def main():

    nodo = pst(
                threadID = 1, 
                counterEvents = 100, 
                IP = '127.0.0.1', 
                PORT = 5000, 
                MCAST_GRP = '224.1.1.1', 
                MCAST_PORT = 5007
                )

    nodo.start()
    nodo.join()

    # MCAST_GRP = '224.1.1.1'
    # MCAST_PORT = 5007
    # IS_ALL_GROUPS = True
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # snd = threading.Thread(target=pst.send, args=(sock,))
    # snd.start()
    # recv = threading.Thread(target=pst.receieve, args=(sock,))
    # recv.start()

    # snd.join()
    # recv.join()

if __name__ == "__main__":
    main()