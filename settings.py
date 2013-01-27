import getpass
import socket

UDP_PORT = 4747
TCP_PORT = 4747

OWN_IP = socket.gethostbyname(socket.gethostname())
BIND_INTERFACE_V4 = ''
BIND_INTERFACE_V6 = ''
IPV4_MULTICAST_GROUP = "239.255.0.113"
IPV6_MULTICAST_GROUP = "ff05::7171"

ALIAS = getpass.getuser()
DOWNLOAD_PATH = "/tmp/trumma"
SHARE = ["/tmp/trumma", "/tmp/trumma2"]

DEBUG = False
