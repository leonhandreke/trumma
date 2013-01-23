# -*- coding: utf-8 -*-

from message import HiMessage, YoMessage, ByeMessage, FileMessage,\
GetFilelistMessage, GetFileMessage, FileTransferResponseMessage
from settings import DEBUG

print_message_seperator = u"\\"
print_field_seperator = u"|"

# ASCII control character 30 (Record Separator, U+001E)
# is used as a message separator.
message_seperator = u"\u001e"

# ASCII control caracter 31 (Unit Separator, U+001F)
# is used as a field separator
field_seperator = u"\u001f"


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


def build(message, seperator=field_seperator):
    """
    Given a Message object, construct a str Object to be transmitted over the
    network.
    """
    if DEBUG:
        print "built: %s" % __str__(message)
    return seperator.join([message.typ, ] +
    list(str(x) for x in message.fields))


def __str__(message):
    return print_field_seperator.join([message.typ, ] +
    list(str(x) for x in message.fields))


def __splitFirstField(text):
    result = text.split(field_seperator, 1)
    if len(result) == 1:
        return result[0], ""
    else:
        return result


def __splitFields(text):
    return text.split(field_seperator)


def _parseType(text):
    typ, text = __splitFirstField(text)

    if typ == "Hi":
        return _parseHi(text)
    elif typ == "Yo":
        return _parseYo(text)
    elif typ == "Bye":
        return _parseBye(text)
    elif typ == "File":
        return _parseFile(text)
    elif typ == "Get Filelist":
        return _parseGetFilelist(text)
    elif typ == "Get File":
        return _parseGetFile(text)
    elif typ == "File Transfer Response":
        return _parseFileTransferResponse(text)
    else:
        print "Warning: Message nicht parsbar."
        if DEBUG:
            print "typ: %s (%s)" % (str(typ), type(typ))
            print "text: %s (%s)" % (str(text), type(text))
        return None


def _parseHi(text):
    # Hi|{PORT}|{USERNAME}
    # USERNAME can be empty
    fields = __splitFields(text)
    if len(fields) != 2:
        return None
    port, username = fields
    port = int(port)

    return HiMessage(port, username)


def _parseYo(text):
    # Yo|{PORT}|{USERNAME}
    # USERNAME can be empty
    fields = __splitFields(text)

    if len(fields) != 2:
        return None

    port, username = fields
    port = int(port)

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
    ttl = int(ttl)
    length = int(length)

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

    offset = int(offset)
    length = int(length)

    return GetFileMessage(sha, offset, length)


def _parseFileTransferResponse(text):
    # File Transfer Response|{STATUS}|{Expected Transfer Volume}
    fields = __splitFields(text)

    if len(fields) != 2:
        return None

    status, volume = fields

    volume = int(volume)

    return FileTransferResponseMessage(status, volume)
