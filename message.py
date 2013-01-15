class Message(object):
    def __init__(self, sender, *args, **kwargs):
        self.sender = sender

class HiMessage(Message):
    def __init__(self, tcp_port, peer_alias, *args, **kwargs):
        self.tcp_port = tcp_port
        self.peer_alias = peer_alias
