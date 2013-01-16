import parser

def receive_datagrams(udp_socket):
    while True:
        data, addr = udp_socket.recvfrom(8192)
        print data
        # message = parser.parse(data, sender)
        # do something with the message

def handle_datagram(data, address):
    print data

#class DatagramProcessor(Thread):
#    def __init__(self, datagram_sender, message_receive_queue, *args, **kwargs):
#        super(DatagramProcessor, self).__init__(*args, **kwargs)
#
#    def run(self):
#        while True:
#            message = self.message_receive_queue.get()
            # do something with the message, maybe send a reply
