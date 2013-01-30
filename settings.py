import getpass
import socket

UDP_PORT = 4747
TCP_PORT = 4747

LOOPBACK_IP_ADDRESS = "127.0.0.1"
# make sure, OWN_IP_ADDRESSES contains your ip addesses,
# otherwise your client will be listed multiple times
OWN_IP_ADDRESSES = [socket.gethostbyname(socket.gethostname()),
                 '2001:7c0:409:8001:221:ccff:fec4:25f0']
IPV4_BIND_INTERFACE = ''
IPV6_BIND_INTERFACE = ''
IPV4_MULTICAST_GROUP = "239.255.0.113"
IPV6_MULTICAST_GROUP = "ff05::7171"

ALIAS = getpass.getuser()
DOWNLOAD_PATH = "/tmp/trumma"
SHARE = ["/tmp/trumma", "/tmp/trumma2"]

DEBUG = False
