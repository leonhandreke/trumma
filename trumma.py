# -*- coding: utf8 -*-
import struct
import pdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import gevent
from gevent import socket
from gevent.server import StreamServer, DatagramServer
from gevent import Greenlet

import settings
from datagram import TrummaDatagramServer
from connection import handle_connection
from ui import run_ui
from peerlist import Peer, AvailableFile, share_files_from_folder
from peerlist import decrement_other_peers_files_ttl, peerlist

peerlist.self_peer = Peer(settings.OWN_IP)
peerlist.self_peer.tcp_port = settings.TCP_PORT
peerlist.self_peer.alias = settings.ALIAS
peerlist.append(peerlist.self_peer)


# build own file list
for s in settings.SHARE:
    share_files_from_folder(s)


# decrement the TTL of all other peer's files every second
Greenlet.spawn(decrement_other_peers_files_ttl)


ipv4_connection_server = StreamServer((settings.BIND_INTERFACE_V4,
    settings.TCP_PORT), handle_connection)
ipv4_connection_server.start()

# Set up the v4 UDP server
ipv4_datagram_server = TrummaDatagramServer((settings.BIND_INTERFACE_V4,
    settings.UDP_PORT))

# Modify some private (?) members to make it join the multicast group
ipv4_datagram_server.init_socket()
ipv4_datagram_server.socket.setsockopt(socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(settings.IPV4_MULTICAST_GROUP) +
            struct.pack('=I', socket.INADDR_ANY))
ipv4_datagram_server.start()

## Set up the v6 UDP server
#ipv6_datagram_server = TrummaDatagramServer((settings.BIND_INTERFACE,
    #settings.UDP_PORT))

## Modify some private (?) members to make it join the multicast group
#ipv6_datagram_server.init_socket()
#ipv6_datagram_server.socket.setsockopt(socket.IPPROTO_IP,
        #socket.IP_ADD_MEMBERSHIP,
        #socket.inet_aton(settings.IPV6_MULTICAST_GROUP) +
            #struct.pack('=I', socket.INADDR_ANY))
#ipv6_datagram_server.start()

#Greenlet.spawn(run_ui(ipv4_datagram_server, ipv6_datagram_server)).join()

gevent.sleep(0.2)
ipv4_datagram_server.send_hi_message_to_multicast_group()
Greenlet.spawn(run_ui(ipv4_datagram_server)).join()

ipv4_connection_server.stop()
ipv4_datagram_server.stop()
