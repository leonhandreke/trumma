# -*- coding: utf8 -*-
import struct
import os

import gevent
from gevent import socket
from gevent.server import StreamServer, DatagramServer
from gevent import Greenlet

import settings
from datagram import handle_datagram
from connection import handle_connection
from ui import run_ui
from peerlist import Peer, LocallyAvailableFile, peerlist

peerlist.self_peer = Peer("127.0.0.1", settings.TCP_PORT, "trumma on " + socket.gethostname())
peerlist.append(peerlist.self_peer)

# build own file list
for f in os.listdir(settings.DOWNLOAD_PATH):
    file_path = os.path.join(settings.DOWNLOAD_PATH, f)
    if os.path.isfile(file_path):
        peerlist.self_peer.files.append(
                LocallyAvailableFile(file_path,
                    None,
                    os.path.getsize(file_path),
                    f))

for f in peerlist.self_peer.files:
    f.sha_hash = f.calculate_sha_hash()

# Set up the TCP server
ipv4_connection_server = StreamServer((settings.BIND_INTERFACE, settings.TCP_PORT), handle_connection)
ipv4_connection_server.start()

# Set up the UDP server
ipv4_datagram_server = DatagramServer((settings.BIND_INTERFACE, settings.UDP_PORT), handle_datagram)

# Modify some private (?) members to make it join the multicast group
ipv4_datagram_server.init_socket()
ipv4_datagram_server.socket.setsockopt(socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(settings.IPV4_MULTICAST_GROUP) + struct.pack('=I', socket.INADDR_ANY))
ipv4_datagram_server.start()

Greenlet.spawn(run_ui).join()

ipv4_connection_server.stop()
ipv4_datagram_server.stop()
