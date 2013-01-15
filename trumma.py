from queue import Queue
from socket import *
import struct
import threading

from datagram import DatagramReceiver
from connection import ConnectionListener
from ui import UserInterface
from peerlist import PeerList
import settings

peerlist = PeerList()

# Instantiate the Queue to hold all received messages
message_receive_queue = Queue()

# Set up the IPv4 multicast listener socket
ipv4_udp_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
ipv4_udp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
ipv4_udp_socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
ipv4_udp_socket.setsockopt(IPPROTO_IP,
        IP_ADD_MEMBERSHIP,
        inet_aton(settings.IPV4_MULTICAST_GROUP) + struct.pack('=I', INADDR_ANY))
ipv4_udp_socket.bind((settings.BIND_INTERFACE, settings.UDP_PORT))

# Set up the IPv4 datagram receiver thread
ipv4_datagram_receiver = DatagramReceiver(ipv4_udp_socket, message_receive_queue)
ipv4_datagram_receiver.start()

# Set up the IPv4 TCP socket and listener
ipv4_tcp_socket = socket(AF_INET, SOCK_STREAM)
ipv4_tcp_socket.bind((settings.BIND_INTERFACE, settings.TCP_PORT))
ipv4_connection_listener = ConnectionListener(ipv4_tcp_socket)
ipv4_connection_listener.start()

ui = UserInterface(peerlist)
ui.start()

# wait for the UI to quit
ui.join()
ipv4_connection_listener.should_terminate = True
ipv4_datagram_receiver.should_terminate = True
