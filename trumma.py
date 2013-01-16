# -*- coding: utf8 -*-
import struct
import os

import gevent
from gevent import socket
from gevent import Greenlet

import settings
from datagram import receive_datagrams
from connection import listen_for_connection
from ui import run_ui
from peerlist import Peer, LocallyAvailableFile

self_peer = Peer("127.0.0.1", settings.TCP_PORT, "trumma on " + socket.gethostname())
peerlist = [self_peer, ]

# build own file list
for f in os.listdir(settings.DOWNLOAD_PATH):
    file_path = os.path.join(settings.DOWNLOAD_PATH, f)
    if os.path.isfile(file_path):
        self_peer.files.append(
                LocallyAvailableFile(file_path,
                    None,
                    os.path.getsize(file_path),
                    f))

for f in self_peer.files:
    f.sha_hash = f.calculate_sha_hash()

# Set up the IPv4 multicast listener socket
ipv4_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
ipv4_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#ipv4_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
ipv4_udp_socket.setsockopt(socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(settings.IPV4_MULTICAST_GROUP) + struct.pack('=I', socket.INADDR_ANY))
ipv4_udp_socket.bind((settings.BIND_INTERFACE, settings.UDP_PORT))

# Set up the IPv4 TCP socket and listener
ipv4_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipv4_tcp_socket.bind((settings.BIND_INTERFACE, settings.TCP_PORT))

ipv4_connection_thread = Greenlet.spawn(listen_for_connection, ipv4_tcp_socket)
ipv4_datagram_thread = Greenlet.spawn(receive_datagrams, ipv4_udp_socket)

Greenlet.spawn(run_ui).join()

ipv4_connection_thread.kill()
ipv4_datagram_thread.kill()
