import os

import settings

class PeerList(dict):
    SELF_KEY = 'SELF'

    def _get_self(self):
        return self[self.SELF_KEY]
    
    def _set_self(self, value):
        self[self.SELF_KEY] = value

    self = property(_get_self, _set_self)

    def __init__(self, *args, **kwargs):
        super(PeerList, self).__init__(*args, **kwargs)
        self[self.SELF_KEY] = []

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
