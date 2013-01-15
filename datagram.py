from queue import Queue
import socket
from threading import Thread

import parser


class DatagramReceiver(Thread):
    def __init__(self, socket, message_queue, *args, **kwargs):
        super(DatagramReceiver, self).__init__(*args, **kwargs)
        self._socket = socket
        self._message_queue = message_queue
        # give the thread an opportunity to quit every second
        self._socket.settimeout(1)
        self.should_terminate = False

    def run(self):
        while not self.should_terminate:
            try:
                data, addr = self._socket.recvfrom(8192)
                message = parser.parse(data, sender)
                # If no valid buschtrommel message could be recovered, don't push it to the queue
                if message:
                    self._message_queue.put(message)
            except socket.timeout:
                pass
        print("DatagramReceiver shutting down")

class DatagramSender(object):
    """
    Write a message to multiple output sockets.
    """
    def __init__(self, sockets, *args, **kwargs):
        pass

    def sendto(self, data, address):
        # call sendto on all sockets
        # make sure this is thread-safe!
        pass

class DatagramProcessor(Thread):
    def __init__(self, datagram_sender, message_receive_queue, *args, **kwargs):
        super(DatagramProcessor, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            message = self.message_receive_queue.get()
            # do something with the message, maybe send a reply
