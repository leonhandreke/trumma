from gevent import Greenlet


def handle_connection(conn, addr):
    conn.close()


def get_file_list(addr, port):
    # could we report progress here using yield?
    pass
