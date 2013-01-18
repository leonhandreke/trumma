class Message(object):
    # sender = Peer Object, should be the same object as in the peerlist.
    # If the sending peer is not yet in the peerlist, a new Peer Object
    pass

class HiMessage(Message):
    # tcp_port = 4747
    # peer_alias = "troll"
    pass

class YoMessage(Message):
    # tcp_port = 4747
    # peer_alias = "troll"
    pass

class FileAnnouncementMessage(Message):
    # sha_hash = hexadecmial string
    # length = length in bytes
    # ttl = ttl in seconds or float("inf")
    # name = "troll.pdf"
    # meta = "Troll everybody effectively!"
    pass
