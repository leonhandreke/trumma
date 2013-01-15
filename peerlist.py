import hashlib
import datetime

import settings

class Peer(object):
    def __init__(self, address, tcp_port, alias, *args, **kwargs):
        super(Peer, self).__init__(*args, **kwargs)
        self.address = address
        self.tcp_port = tcp_port
        self.alias = alias
        self.last_seen = datetime.datetime.now()
        self.files = []

    def __str__(self):
        return self.alias + " (" + self.address + ")"


class AvailableFile(object):
    def __init__(self, sha_hash, length, name, ttl=float("inf"), meta=None, *args, **kwargs):
        super(AvailableFile, self).__init__(*args, **kwargs)
        self.sha_hash = sha_hash
        self.length = length
        self.name = name
        self.ttl = ttl
        self.meta = meta


class LocallyAvailableFile(AvailableFile):
    def __init__(self, local_path, *args, **kwargs):
        super(LocallyAvailableFile, self).__init__(*args, **kwargs)
        self.local_path = local_path

    def calculate_sha_hash(self):
        h = hashlib.sha1()
        f = open(self.get_local_path())
        while True:
            data = f.read(4096)
            if not data:
                f.close()
                break
            h.update(data)
        self.sha_hash = h.hexdigest()
