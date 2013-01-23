# -*- coding: utf-8 -*-

from message import *
from settings import DEBUG

if DEBUG:
    DEBUG_message_separator = u"\\"
    DEBUG_field_separator = u"|"

# ASCII control character 30 (Record Separator, U+001E)
# is used as a message separator.
message_separator = u"\u001e"

# ASCII control caracter 31 (Unit Separator, U+001F)
# is used as a field separator
field_separator = u"\u001f"


""" Message Examples:

# Hi
Hi|{PORT}|{USERNAME}
Hi|123|Kev
Hi|123|

USERNAME can be empty


# Yo
Yo|{PORT}|{USERNAME}
Yo|123|Kev
Yo|123|

USERNAME can be empty


# Bye
Bye


# File
File|{SHA1}|{TTL}|{LENGTH}|{DISPLAY_NAME}|{META_INFORMATION}
File|526b11399df02e253c502a8067eabea17bfae8a8|-1|3|Kev|Kev


# Get Filelist
Get Filelist


# Get File
Get File|{SHA1}|{OFFSET}|{LENGTH}
Get File|526b11399df02e253c502a8067eabea17bfae8a8|0|3


# File Transfer Response
File Transfer Response|{STATUS}|{Expected Transfer Volume}
File Transfer Response|OK|3
"""


def parse(data):
    """
    Return a Message object with the deserialized message.

    If no Message object can be constructed from the given input data,
    None is returned.
    """
    return _parseType(data)


def build(message, separator=field_separator):
    """
    Given a Message object, construct a str Object to be transmitted over the
    network.
    """
    if DEBUG:
        print "built: %s" % __str__(message)

    return separator.join([message.type, ] + message.fields) + message_separator


def __str__(message):
    return DEBUG_field_separator.join([message.type, ] + message.fields)


def __splitFirstField(text):
    result = text.split(field_separator, 1)
    if len(result) == 1:
        return result[0], ""
    else:
        return result


def __splitFields(text):
    return text.split(field_separator)


def _parseType(text):
    type, text = __splitFirstField(text)

    if type == "Hi":
        return _parseHi(text)
    elif type == "Yo":
        return _parseYo(text)
    elif type == "Bye":
        return _parseBye(text)
    elif type == "File":
        return _parseFile(text)
    elif type == "Get Filelist":
        return _parseGetFilelist(text)
    elif type == "Get File":
        return _parseGetFile(text)
    elif type == "File Transfer Response":
        return _parseFileTransferResponse(text)
    else:
        print "Warning: Message nicht parsbar."
        if DEBUG:
            print "type: %s (%s)" % (str(type), typee(type))
            print "text: %s (%s)" % (str(text), typee(text))
        return None


def _parseHi(text):
    # Hi|{PORT}|{USERNAME}
    # USERNAME can be empty
    fields = __splitFields(text)
    if len(fields) != 2:
        return None
    port, username = fields
    return HiMessage(port, username)


def _parseYo(text):
    # Yo|{PORT}|{USERNAME}
    # USERNAME can be empty
    fields = __splitFields(text)

    if len(fields) != 2:
        return NOne

    port, username = fields
    return YoMessage(port, username)


def _parseBye(text):
    # Bye
    return ByeMessage()


def _parseFile(text):
    # File|{SHA1}|{TTL}|{LENGTH}|{DISPLAY_NAME}|{META_INFORMATION}
    fields = __splitFields(text)

    if len(fields) != 5:
        return None

    sha, ttl, length, name, meta = fields
    return FileMessage(sha, ttl, length, name, meta)


def _parseGetFilelist(text):
    # Get Filelist

    return GetFilelistMessage()


def _parseGetFile(text):
    # Get File|{SHA1}|{OFFSET}|{LENGTH}
    fields = __splitFields(text)

    if len(fields) != 3:
        return None

    sha, offset, length = fields
    return GetFileMessage(sha, offset, length)


def _parseFileTransferResponse(text):
    # File Transfer Response|{STATUS}|{Expected Transfer Volume}
    fields = __splitFields(text)

    if len(fields) != 2:
        return None

    status, volume = fields
    return FileTransferResponseMessage(status, volume)
