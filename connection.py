from gevent import Greenlet
import settings


def handle_connection(conn, addr):
    conn.close()


def get_file_list(addr):
    # could we report progress here using yield?
    port = settings.TCP_PORT
    print("If this method was implemented, it would try to get the filelist")
    pass
