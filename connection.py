from gevent import Greenlet
import settings
from peerlist import peerlist


def handle_connection(conn, addr):
    conn.close()


def get_file_list(peer):
    # could we report progress here using yield?
    port = settings.TCP_PORT
    print("If this method was implemented, it would try to get the filelist")
    pass


def get_file(peer, f):
    # could we report progress here using yield?
    port = settings.TCP_PORT
    print("If this method was implemented, it would try to get the filelist")
    pass
