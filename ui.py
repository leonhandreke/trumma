# -*- coding: utf8 -*-
from __future__ import print_function
import readline

from gevent import monkey
import settings
from peerlist import peerlist, findpeer
#from datagram import TrummaDatagramServer
#from trumma import ipv4_datagram_server
from message import HiMessage
from connection import get_file_list, get_file

monkey.patch_sys()

import pdb


#def run_ui(ipv4_datagram_server, ipv6_datagram_server):
    #ipv6_datagram_server = ipv6_datagram_server
    #ipv4_datagram_server = ipv4_datagram_server
def run_ui(ipv4_datagram_server):
    ipv4_datagram_server = ipv4_datagram_server

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
                peer = findpeer(' '.join(scmd[2:]))
                if peer:
                    print("Peer " + peer.alias + " has "
                        + str(len(peer.files)) + " files:")
                    for f in peer.files:
                        print(f.name + "  " + str(f.length)
                            + "  " + str(f.sha_hash))
            elif cmd.startswith("get filelist ") and len(scmd) >= 3:
                peer = findpeer(' '.join(scmd[2:]))
                if peer:
                    get_file_list(peer)
            elif cmd.startswith("get file ") and len(scmd) == 4:
                peer = findpeer(' '.join(scmd[3:]))
                if peer:
                    get_file(peer, scmd[2])
            elif cmd.startswith("find peers"):
                #pdb.set_trace()
                ipv4_datagram_server.send_hi_message_to_multicast_group()
                #ipv6_datagram_server.send_hi_message_to_multicast_group()
                print("finding peers … please check peerlist to " +
                    "see if somebody answered")
            elif cmd == "exit" or cmd == "quit" or cmd == "q":
                ipv4_datagram_server.send_bye_message_to_multicast_group()
                break
            elif cmd == "help" or cmd == "h":
                #todo: implement
                print("there should be some help here…")
            else:
                print("No such command - type help to get a list of commands")
        except EOFError:
            break
