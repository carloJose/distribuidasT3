import threading
import socket
import struct
import sys

from postman import Postman as pst


def main(id):

    nodo = pst(
                threadID = id,
                counterEvents = 100, 
                IP = '127.0.0.1', 
                PORT = 5000, 
                MCAST_GRP = '224.1.1.1', 
                MCAST_PORT = 5007
                )

    nodo.start()
    nodo.join()

if __name__ == "__main__":
    main(int(sys.argv[1]))