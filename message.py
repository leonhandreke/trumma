#/usr/bin/python2
# -*- coding: utf-8 -*-
"""
>>> import message
>>> o = message.HiMessage(123, "Kev")
>>> print o
HI|123|Kev
>>> i = message.create_message(o.data)
>>> print i
HI|123|Kev
>>> i.username
u'Kev'
>>> i.port
123

"""
import settings


def create_message(data):
    if isinstance(data, Message):
        raise TypeError("data is already a Message object!")

    import parser
    return parser.parse(data)


class Message(object):
    def __init__(self):
        pass

    def __str__(self):
        import parser
        return parser.__str__(self)

    @property
    def data(self):
        import parser
        return parser.build(self)

    @property
    def fields(self):
        return []


class HiMessage(Message):
    """
    port = valid port number
    username = string, can be empty
    """
    typ = "HI"

    def __init__(self, port, username=""):
        super(HiMessage, self).__init__()
        self.port = port
        self.username = username

    @property
    def fields(self):
        return [self.port, self.username]


class YoMessage(Message):
    """
    port = valid port number
    username = string, can be empty
    """
    typ = "YO"

    def __init__(self, port, username=""):
        super(YoMessage, self).__init__()
        self.port = port
        self.username = username

    @property
    def fields(self):
        return [self.port, self.username]


class ByeMessage(Message):
    tcp_port = settings.UDP_PORT
    typ = "BYE"

    def __init__(self):
        super(ByeMessage, self).__init__()


class FileMessage(Message):
    """
    sha = hexadecmial string (sha1 hash of file)
    ttl = ttl in seconds or float("inf")
    length = length in bytes
    name = "filename.pdf"
    meta = "Some additional things good to know"
    """
    typ = "FILE"

    def __init__(self, sha, ttl, length, name, meta):
        super(FileMessage, self).__init__()
        self.sha = sha
        self.ttl = ttl
        self.length = length
        self.name = name
        self.meta = meta

    @property
    def fields(self):
        return [self.sha, self.ttl, self.length, self.name, self.meta]


class GetFilelistMessage(Message):
    typ = "GET FILELIST"

    def __init__(self):
        super(GetFilelistMessage, self).__init__()


class GetFileMessage(Message):
    """
    sha = hexadecmial string (sha1 hash of file)
    offset = start at offset (octet)
    length = length in bytes (octet)
    """
    typ = "GET FILE"

    def __init__(self, sha, offset, length):
        super(GetFileMessage, self).__init__()
        self.sha = sha
        self.offset = offset
        self.length = length

    @property
    def fields(self):
        return [self.sha, self.offset, self.length]


class FileTransferResponseMessage(Message):
    """
    status = one of three status responses (see below)
    volume = number of octets of the file that the peer expects to send.
    """

    OK_STATUS = "OK"
    TRY_AGAIN_LATER_STATUS = "Try Again Later"
    NEVER_TRY_AGAIN_STATUS = "Never Try Again"

    typ = "FILE TRANSFER RESPONSE"

    def __init__(self, status, volume):
        super(FileTransferResponseMessage, self).__init__()
        self.status = status
        self.volume = volume

    @property
    def fields(self):
        return [self.status, self.volume]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
