import readline
from threading import Thread

class UserInterface(Thread):
    def __init__(self, peerlist, *args, **kwargs):
        super(UserInterface, self).__init__(*args, **kwargs)
        self._peerlist = peerlist

    def run(self):
        while True:
            try:
                cmd = input("> ")
                if cmd == "listpeers"
            except EOFError:
                break

