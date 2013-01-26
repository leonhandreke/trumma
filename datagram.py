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
        elif isinstance(message, ByeMessage):
            self.handle_bye_message(message, address[0])
        elif isinstance(message, FileMessage):
            self.handle_file_message(message, address[0])


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
            # prepare a yo, but only if the hi did not come from myself
            if peer.address != settings.OWN_IP:
                yo = YoMessage(peerlist.self_peer.tcp_port,
                    peerlist.self_peer.alias)
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

    def handle_bye_message(self, message, address):
        peer = find_peer_by_address(address)
        peerlist.remove(peer)

    def handle_file_message(self, message, address):
        peerlist.update_with_file_announcement_message(message)

    def send_hi_message_to_multicast_group(self):
        hi = HiMessage(username=settings.ALIAS, port=settings.TCP_PORT)
        self.send_message_to_multicast_group(hi)

    def send_bye_message_to_multicast_group(self):
        self.send_message_to_multicast_group(ByeMessage())

    def send_message_to_multicast_group(self, message):
        data = message.data
        self.sendto(data, (settings.IPV4_MULTICAST_GROUP, settings.UDP_PORT))

