# -*- coding: utf8 -*-
from __future__ import print_function
import readline

from gevent import monkey

monkey.patch_sys()

def run_ui():
    while True:
        try:
            cmd = raw_input("> ")
        # commands needed:
        # * list peers
        # * list files $peer 
        # * get filelist $peer
        # * get file $SHA (tab completion?) $path (put in ~ if $path not given)
        # * find peers


        # $peer identified by nick if unique, else ip

        # alias commands:
        # list my files --> list files 127.0.0.1 
        # refresh filelist $peer --> get filelist $peer
        # update filelist §peer --> get filelist $peer
            if (cmd == "listpeers") or (cmd == "list peers"):
            #    print ("listpeers")
                print(*self._peerlist, sep="\n")
            elif cmd.startswith("list files "):
                peer = cmd.split()[2]
                print("list files " + peer)
            elif cmd.startswith("get filelist "):
                peer = cmd.split()[2]
                print("get filelist " + peer)
            elif cmd.startswith("get file "):
                fileid = cmd.split()[2]
                path = cmd.split()[3]
                print("get file " + fileid + " " + path)
            elif cmd.startswith("find peers "):
                print("get filelist")
            elif cmd == "exit" or cmd == "quit" or cmd =="q":
                break
            else:
                print("No such command")
        except EOFError:
            break

