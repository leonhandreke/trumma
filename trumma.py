from queue import Queue
import socket
import struct
import threading
import os

from datagram import DatagramReceiver
from connection import ConnectionListener
from ui import UserInterface
from peerlist import Peer, LocallyAvailableFile
import settings

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

# Instantiate the Queue to hold all received messages
message_receive_queue = Queue()

# Set up the IPv4 multicast listener socket
ipv4_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
ipv4_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#ipv4_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
ipv4_udp_socket.setsockopt(socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(settings.IPV4_MULTICAST_GROUP) + struct.pack('=I', socket.INADDR_ANY))
ipv4_udp_socket.bind((settings.BIND_INTERFACE, settings.UDP_PORT))

# Set up the IPv4 datagram receiver thread
ipv4_datagram_receiver = DatagramReceiver(ipv4_udp_socket, message_receive_queue)
ipv4_datagram_receiver.start()

# Set up the IPv4 TCP socket and listener
ipv4_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipv4_tcp_socket.bind((settings.BIND_INTERFACE, settings.TCP_PORT))
ipv4_connection_listener = ConnectionListener(ipv4_tcp_socket)
ipv4_connection_listener.start()

ui = UserInterface(peerlist)
ui.start()

# wait for the UI to quit
ui.join()
ipv4_connection_listener.should_terminate = True
ipv4_datagram_receiver.should_terminate = True
