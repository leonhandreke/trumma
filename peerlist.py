import hashlib

import settings

"""
class PeerList(list):
    SELF_KEY = 'SELF'

    def _get_self(self):
        return self[self.SELF_KEY]

    def _set_self(self, value):
        self[self.SELF_KEY] = value

    self = property(_get_self, _set_self)

    def __init__(self, *args, **kwargs):
        super(PeerList, self).__init__(*args, **kwargs)
        self[self.SELF_KEY] = []
"""
class Peer(object):
    def __init__(self, address, tcp_port, alias, *args, **kwargs):
        super(Peer, self).__init__(*args, **kwargs)
        self.address = address
        self.tcp_port = tcp_port
        self.alias = alias
        self.files = []

    def __unicode__(self):
        return self.alias + "(" + self.address + ")"


class AvailableFile(object):
    def __init__(self, sha_hash, length, name, ttl=float("inf"), meta=None, *args, **kwargs):
        super(AvailableFile, self).__init__(*args, **kwargs)
        self.sha_hash = sha_hash
        self.length = length
        self.name = name
        self.ttl = ttl
        self.meta = meta

    def get_local_path(self):
        return os.path.join(settings.DOWNLOAD_PATH, self.name)

    def recalculate_sha_hash(self):
        h = hashlib.sha1()
        f = open(self.get_local_path())
        while True:
            data = f.read(4096)
            if not data:
                f.close()
                break
            h.update(data)
        self.sha_hash = h.hexdigest()
