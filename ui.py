# -*- coding: utf8 -*-
from __future__ import print_function
import readline

from gevent import monkey
from gevent import Greenlet

import settings
from peerlist import peerlist, findpeer
from message import HiMessage
from connection import get_file_list, get_file

monkey.patch_sys()

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
                cmd = "list files " + settings.OWN_IP
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
                print("Peer {alias} has {numfiles} files:".format(
                    alias=peer.alias,
                    numfiles=len(peer.files)
                    ))
                for f in peer.files:
                    print("{name} {length} {sha_hash}".format(
                        name=f.name,
                        length=f.length,
                        sha_hash=f.sha_hash
                        ))
            elif cmd.startswith("get filelist ") and len(scmd) >= 3:
                peer = findpeer(' '.join(scmd[2:]))
                get_filelist_task = Greenlet.spawn(get_file_list, peer)
                get_filelist_task.join()
            elif cmd.startswith("get file ") and len(scmd) == 4:
                peer = findpeer(' '.join(scmd[3:]))
                matching_files = filter(lambda f: scmd[2] in f.sha_hash or scmd[2] in f.name, peer.files)
                if len(matching_files) > 1:
                    raise UserInputException("Multiple matching files")
                elif len(matching_files) == 0:
                    raise UserInputException("No matching file")
                else:
                    download_task = Greenlet.spawn(get_file, peer, matching_files[0])
                    # wait until completion
                    download_task.join()


            elif cmd.startswith("find peers"):
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
