import hashlib
import datetime
import os

import gevent

import settings


class PeerList(list):
    self_peer = None

    def update_with_file_announcement_message(self, message, sender_peer):
        try:
            f = filter(lambda f: f.sha_hash == message.sha,
                sender_peer.files)[0]
        except IndexError:
            f = AvailableFile(message.sha)
            sender_peer.files.append(f)
        f.meta = message.meta
        f.length = message.length
        f.ttl = message.ttl
        f.name = message.name

        # if the file was deleted
        if f.ttl == 0:
            sender.files.remove(f)


peerlist = PeerList()


class Peer(object):
    alias = None
    tcp_port = None

    def __init__(self, address, *args, **kwargs):
        super(Peer, self).__init__(*args, **kwargs)
        self.address = address
        self.last_seen = datetime.datetime.now()
        self.files = []

    def __str__(self):
        return self.alias + " (" + self.address + ")"


def decrement_other_peers_files_ttl():
    while True:
        for peer in peerlist:
            if peer is not peerlist.self_peer:
                for f in peer.files:
                    f.ttl -= 1
        gevent.sleep(1)


class AvailableFile(object):
    length = None
    name = None
    ttl = None
    meta = None
    local_path = None

    def __init__(self, sha_hash, *args, **kwargs):
        super(AvailableFile, self).__init__(*args, **kwargs)
        self.sha_hash = sha_hash

    def calculate_sha_hash(self):
        if not self.local_path:
            raise ValueError("Cannot calculate SHA for non-local file.")
        h = hashlib.sha1()
        # open the file in binary mode
        f = open(self.local_path, "rb")
        while True:
            data = f.read(4096)
            if not data:
                f.close()
                break
            h.update(data)
        return h.hexdigest()


def findpeer(query):
    peer = find_peer_by_name(query)
    if peer:
        return peer
    else:
        return find_peer_by_address(query)


def find_peer_by_name(query):
    peers = []
    for peer in peerlist:
        if peer.alias == query:
            peers.append(peer)
    if len(peers) > 1:
        raise NameError("More than one peer in the peerlist with the alias given!")
    elif len(peers) == 0:
        raise NameError("No peer in the peerlist with the alias given!")
    else:
        return(peers[0])


def find_peer_by_address(query):
    peers = []
    for peer in peerlist:
        if peer.address == query:
            peers.append(peer)
    if len(peers) > 1:
        NameError("More than one peer in the peerlist with the address given!")
    elif len(peers) == 0:
        NameError("No peer in the peerlist with the address given!")
    else:
        return(peers[0])


def share_files_from_folder(folder):
    shared = []
    for f in os.listdir(folder):
        file_path = os.path.join(folder, f)
        shared += share_file(file_path)
    return shared


def share_file(f):
    shared = []
    if os.path.isfile(f):
        new_file = AvailableFile(None)
        new_file.length = os.path.getsize(f)
        new_file.ttl = -1
        new_file.name = f
        new_file.local_path = f
        new_file.sha_hash = new_file.calculate_sha_hash()
        shared_already = False
        for s in peerlist.self_peer.files:
            if s.sha_hash == new_file.sha_hash:
                shared_already = True
        if not shared_already:
            peerlist.self_peer.files.append(new_file)
            shared.append(new_file)
        return shared
    elif os.path.isdir(f):
        return share_files_from_folder(f)
    else:
        raise EOFError('No such file or directory')
