import threading
import socket
import struct
import sys

from postman import Postman as pst


def main(id):

    nodo = pst(
                threadID = id,
                MCAST_GRP = '224.1.1.1', 
                MCAST_PORT = 5007
                )

    nodo.start()
    nodo.join()

if __name__ == "__main__":
    main(int(sys.argv[1]))
