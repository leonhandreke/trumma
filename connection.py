import socket
from threading import Thread

class ConnectionServer(Thread):
    def __init__(self, conn, addr, *args, **kwargs):
        super(ConnectionServer, self).__init__(*args, **kwargs)

    def run(self):
        # receive from the connection, reply, close
        pass

class ConnectionListener(Thread):
    def __init__(self, socket, *args, **kwargs):
        super(ConnectionListener, self).__init__(*args, **kwargs)
        self._socket = socket
        # give the thread an opportunity to quit every second
        self._socket.settimeout(1)
        self.should_terminate = False

    def run(self):
        self._socket.listen(3)
        while not self.should_terminate:
            try:
                conn, addr = self._socket.accept()
                ConnectionServer(conn, addr).start()
            except socket.timeout:
                pass
        print("ConnectionListener shutting down")

class GetFilelistConnectionClient(Thread):
    def __init__(self, addr, port, callback, *args, **kwargs):
        super(GetFilelistConnectionClient, self).__init__(*args, **kwargs)

    def run(self):
        # open connection, build filelist, callback(filelist)
        pass

class GetFileConnectionClient(Thread):
    TRY_AGAIN_LATER_ERROR = "Try Again Later"
    NEVER_TRY_AGAIN_ERROR = "Never Try Again"
    OTHER_ERROR = "Other Error"

    def __init__(self,
            addr, port,
            file_to_get,
            progress_callback, # progress_callback(self, bytes_received, bytes_total)
            error_callback, # error_callback(self, self.__class__.TRY_AGAIN_LATER_ERROR)
            success_callback, # success_callback(self)
            *args, **kwargs):
        super(GetFileConnectionClient, self).__init__(*args, **kwargs)

    def run(self):
        # establish connection, download, call callbacks as appropriate, close connection
        pass
