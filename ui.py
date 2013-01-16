# -*- coding: utf8 -*-
from __future__ import print_function
import readline

from gevent import monkey

def run_ui():
    while True:
        try:
            cmd = raw_input("> ")

            # split command
            scmd = cmd.split();

            # some alias commands first:
            if cmd == "list my files": cmd = "list files 127.0.0.1"
            elif cmd == "listpeers": cmd = "list peers"
            elif (scmd[0] == "refresh" or scmd[0] == "update") and scmd[1] == "filelist" and len(scmd) == 3: cmd = "get filelist " + scmd[2]
            # split again, we may have changed cmd
            scmd = cmd.split();

            if (cmd == "list peers"):
                print(*self._peerlist, sep="\n")
            elif cmd.startswith("list files ") and len(scmd) == 3:  
                print(filter(lambda s: s.address==scmd[2], self._peerlist))
            elif cmd.startswith("get filelist ") and len(scmd) == 3:
                print("get filelist " + scmd[2])
            elif cmd.startswith("get file ") and len(scmd) == 4:
                print("get file " + scmd[2] + " " + scmd[3])
            elif cmd.startswith("find peers"):
                print("find peers")
            elif cmd == "exit" or cmd == "quit" or cmd =="q":
                break
            elif cmd == "help" or cmd == "h":
                print("there should be some help here…") 
            else:
                print("No such command - type help to get a list of commands")
        except EOFError:
            pass
