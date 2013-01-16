from gevent import Greenlet

def serve_connection(conn, addr):
    print "Serve connection from " + addr

def listen_for_connection(tcp_socket):
    tcp_socket.listen(3)
    while True:
        conn, addr = tcp_socket.accept()
        Greenlet.spawn(serve_connection, conn, addr)

def get_file_list(addr, port):
    # could we report progress here using yield?
    pass
