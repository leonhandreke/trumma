# -*- coding: utf8 -*-
from __future__ import print_function
import readline

from gevent import monkey

from peerlist import peerlist
monkey.patch_sys()


def run_ui():
    while True:
        try:
            cmd = raw_input("> ")

            # split command
            if cmd != "":
                scmd = cmd.split()
            # some alias commands first:
            if cmd == "list my files":
                cmd = "list files 127.0.0.1"
            elif cmd == "listpeers":
                cmd = "list peers"
            elif ((scmd[0] == "refresh" or scmd[0] == "update") and
                scmd[1] == "filelist" and len(scmd) == 3):
                cmd = "get filelist " + scmd[2]
            # split again, we may have changed cmd

            if cmd != "":
                scmd = cmd.split()

            if cmd == "list peers":
                print(*peerlist, sep="\n")
            elif cmd == "self":
                print(peerlist.self_peer)
            elif cmd.startswith("list files ") and len(scmd) >= 3:
                matchingpeers = []
                query = ' '.join(scmd[2:])
                for peer in peerlist:
                    if peer.alias == query or peer.address == scmd[2]:
                        matchingpeers.append(peer)

                if len(matchingpeers) > 1:
                    print("The following peers match your search, please " +
                            "specify the peer whose files you want to see " +
                            "by typing \"list peers $ip\"")
                elif len(matchingpeers) == 0:
                    print('No peer "' + query + '" found.')
                else:
                    for peer in matchingpeers:
                        print(filter(
                            lambda s: s.address == peer.address, peerlist))
            elif cmd.startswith("get filelist ") and len(scmd) == 3:
                print("get filelist " + scmd[2])
            elif cmd.startswith("get file ") and len(scmd) == 4:
                print("get file " + scmd[2] + " " + scmd[3])
            elif cmd.startswith("find peers"):
                print("find peers")
            elif cmd == "exit" or cmd == "quit" or cmd == "q":
                break
            elif cmd == "help" or cmd == "h":
                print("there should be some help here…")
            else:
                print("No such command - type help to get a list of commands")
        except EOFError:
            break
