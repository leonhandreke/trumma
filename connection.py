import os

from gevent import socket

import settings
from peerlist import peerlist
from message import GetFilelistMessage, GetFileMessage, FileMessage
import parser


def handle_connection(conn, addr):
    message_data = ""
    while True:
        new_data = conn.recv(1)
        message_data += new_data
        if new_data == parser.message_separator:
            break

    message = parser.parse(message_data)
    if message == None:
        print "Unknown message received in connection to " + addr[0]
        conn.close()
        return
    if isinstance(message, GetFilelistMessage):
        for f in peerlist.self_peer.files:
            m = FileMessage(f.sha_hash,
                    -1 if f.ttl == float("inf") else f.ttl,
                    f.length,
                    f.name,
                    f.meta)
            conn.sendall(parser.build(m))
        conn.close()
        return
    elif isinstance(message, GetFileMessage):
        pass

def get_file_list(peer):
    sock = socket.create_connection((peer.address, peer.tcp_port))
    sock.sendall(parser.build(GetFilelistMessage()))

    message_data = ""
    while True:
        new_data = sock.recv(1)
        if not new_data:
            break

        message_data += new_data
        if new_data == parser.message_separator:
            message = parser.parse(message_data)
            if message:
                peerlist.update_with_file_announcement_message(message)
            message_data = ""

    sock.close()

def get_file(peer, f):
    f.local_path = os.path.join(settings.DOWNLOAD_PATH, f.name)
    if os.path.exists(f.local_path):
        print("File {filename} already exists.".format(filename=f.name))
        return

    sock = socket.create_connection((peer.address, peer.tcp_port))
    sock.sendall(parser.build(GetFileMessage(f.sha_hash, 0, f.length)))

    message_data = ""
    while True:
        new_data = sock.recv(1)
        message_data += new_data
        if new_data == parser.message_separator:
            message = parser.parse(message_data)
            if message.status != FileTransferResponseMessage.OK_STATUS:
                print("File Request denied by peer.")
                return
            else:
                break

    fd = file(f.local_path, "wb")
    while True:
        new_data = sock.recv(1024)
        if new_data:
            fd.write(new_data)
        else:
            break

    fd.close()
    sock.close()
