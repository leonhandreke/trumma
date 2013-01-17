import hashlib
import datetime

import settings

class PeerList(list):
    self_peer = None

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


class AvailableFile(object):
    length = None
    name = None
    ttl = None
    meta = None

    def __init__(self, sha_hash, *args, **kwargs):
        super(AvailableFile, self).__init__(*args, **kwargs)
        self.sha_hash = sha_hash


class LocallyAvailableFile(AvailableFile):
    local_path = None

    def calculate_sha_hash(self):
        h = hashlib.sha1()
        # open the file in binary mode
        f = open(self.local_path, "rb")
        while True:
            data = f.read(4096)
            if not data:
                f.close()
                break
            h.update(data)
        self.sha_hash = h.hexdigest()
