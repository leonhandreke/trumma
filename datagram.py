from datetime import datetime

from gevent.server import DatagramServer
import parser
from message import HiMessage, YoMessage
from peerlist import Peer, peerlist
import settings


class TrummaDatagramServer(DatagramServer):
    def handle(self, data, address):
        message = parser.parse(data, address)
        if message is None:
            # discard message
            print "Datagram with unknown message received"
        elif isinstance(message, HiMessage):
            self.handle_hi_message(message)
        elif isinstance(message, YoMessage):
            self.handle_yo_message(message)

    def handle_hi_message(self, message):
        # insert the new peer into our peerlist
        message.sender = message.tcp_port
        message.sender = message.peer_alias
        peerlist.append(new_peer)

        # prepare a yo
        yo = YoMessage()
        yo.tcp_port = peerlist.self_peer.tcp_port
        yo.peer_alias = peerlist.self_peer.alias

        self.send_message_to_multicast_group(yo)

    def handle_yo_message(self, message):
        if message.sender not in peerlist:
            new_peer = Peer(address[0])
            peerlist.append(new_peer)
        message.sender = message.tcp_port
        message.sender = message.peer_alias

        self.sender.last_seen = datetime.now()

    def handle_bye_message(self, message):
        peerlist.remove(message.sender)

    def handle_file_announcement(self, message):
        try:
            f = filter(lambda f: f.sha_hash == message.sha_hash,
                message.sender.files)[0]
        except IndexError:
            f = AvailableFile(message.sha_hash)
            self.sender.files.append(f)
        f.meta = message.meta
        f.length = message.length
        f.ttl = message.ttl
        f.name = message.name

        # if the file was deleted
        if f.ttl == 0:
            sender.files.remove(f)

    def send_hi_message_to_multicast_group(self):
        self.send_message_to_multicast_group(HiMessage())

    def send_message_to_multicast_group(self, message):
        data = parser.build(message)
        self.sendto(data, (settings.IPV4_MULTICAST_GROUP, settings.UDP_PORT))

