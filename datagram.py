from datetime import datetime

from gevent.server import DatagramServer
from peerlist import Peer, peerlist, findpeer, find_peer_by_address
from message import create_message, HiMessage, YoMessage, ByeMessage
import settings


class TrummaDatagramServer(DatagramServer):
    def handle(self, data, address):
        message = create_message(data)
        if message is None:
            # discard message
            print "Datagram with unknown message received"
        elif isinstance(message, HiMessage):
            self.handle_hi_message(message, address[0])
        elif isinstance(message, YoMessage):
            self.handle_yo_message(message, address[0])

    def handle_hi_message(self, message, address):
        # insert the new peer into our peerlist
        peer = find_peer_by_address(address)
        if peer not in peerlist:
            new_peer = Peer(address)
            new_peer.tcp_port = message.port
            new_peer.alias = message.username
            peerlist.append(new_peer)
        else:
            peer.last_seen = datetime.now()

        # prepare a yo
        yo = YoMessage(peerlist.self_peer.tcp_port, peerlist.self_peer.alias)
        self.send_message_to_multicast_group(yo)

    def handle_yo_message(self, message, address):
        # insert the new peer into our peerlist
        peer = find_peer_by_address(address)
        if peer not in peerlist:
            new_peer = Peer(address)
            new_peer.tcp_port = message.port
            new_peer.alias = message.username
            peerlist.append(new_peer)
        else:
            peer.last_seen = datetime.now()

    def handle_bye_message(self, message):
        peerlist.remove(message.sender)

    def handle_file_announcement(self, message):
        try:
            f = filter(lambda f: f.sha_hash == message.sha,
                message.sender.files)[0]
        except IndexError:
            f = AvailableFile(message.sha)
            self.sender.files.append(f)
        f.meta = message.meta
        f.length = message.length
        f.ttl = message.ttl
        f.name = message.name

        # if the file was deleted
        if f.ttl == 0:
            sender.files.remove(f)

    def send_hi_message_to_multicast_group(self):
        hi = HiMessage(username=settings.ALIAS, port=settings.TCP_PORT)
        self.send_message_to_multicast_group(hi)

    def send_bye_message_to_multicast_group(self):
        self.send_message_to_multicast_group(ByeMessage())

    def send_message_to_multicast_group(self, message):
        data = message.data
        self.sendto(data, (settings.IPV4_MULTICAST_GROUP, settings.UDP_PORT))

