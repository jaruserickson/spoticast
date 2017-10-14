#!/usr/bin/python3
''' main cli for spotipy rooms '''
from __future__ import absolute_import, unicode_literals
import sys
import time
import argparse
from multiprocessing import Process
from Crypto.Cipher import AES

from app.mac_scripts import MacScripts
from app.sockets import Sock

PORT = 8080
HOST = str(AES.new('1n1dklmnAMADKENM', AES.MODE_ECB).decrypt(b'\xd8\x85\x11\xa85P$\x91\xee\x87\x05>\x9e\x89\xba\xb0\xa5\x14\xfa\xbdu\xe5F\xf6\xa7\xa2\x1d\x92\x1e\x91}\x1f\x96e\x91\x8b\x14\xf6O,&\x16\xd1\xdb\x91\xc4\x98"\xd3\xd2\x1b\x19(\x9f\xa4G[\x18\x8d\\\x06\x81!\x83').strip())[2:-1]

class Spoticast:
    ''' main app '''
    def __init__(self):
        self.mac_scripts = MacScripts()
        self.sockets = Sock(HOST, PORT)
        self.room_addr = None

        self.parent = Process(target=self.watch_songs)

        try:
            self.run()
        except EOFError: # need to remember to kill the process
            self.parent.terminate()
        except KeyboardInterrupt:
            self.parent.terminate()


    def run(self):
        ''' runs the parse_args script '''
        parser = argparse.ArgumentParser(description='Spotify broadcaster')

        parser.add_argument(
            '-i', '-c' '--create-room', '--init',
            help='create a room and start broadcasting',
            action='store_true', dest="init"
        )
        parser.add_argument(
            '-q', '--quit', '-l', '--leave', help='leave room', 
            action='store_true', dest="leave"
        )
        parser.add_argument(
            '-r', '--room', help='prints the room info', action='store_true',
            dest="room"
        )
        parser.add_argument(
            '-c', '--current', help='current playing', action='store_true',
            dest="current"
        )

        args = parser.parse_args()

        if args.init:
            self.host_room()
        elif args.leave:
            self.leave_room()
        elif args.room:
            print(self.room_addr if self.room_addr else 'No current room!')
        elif args.current:
            print(self.mac_scripts.get_current_playing())

    def host_room(self):
        ''' host a room '''
        print('Sending host request...')
        self.parent.start() # run in background
        room_addr = self.sockets.create_room()
        print('Joined room: %s' % room_addr)
        print('Ctrl C to close room.')
        self.room_addr = room_addr

    def leave_room(self):
        ''' leave a room '''
        if self.room_addr:
            print('Sending leave request...')
            ret = self.sockets.leave_room(self.room_addr.get_addr())
            if ret[0] != '@':
                self.room_addr = None
                print(ret)
                self.parent.terminate()
                sys.exit()
        else:
            print("You're not in a room!")

    def join_room(self, addr):
        ''' joins a room of room address addr '''
        print('Sending join request...')
        room_data = self.sockets.join_room(addr)
        if room_data != {}:
            self.room_addr = addr
            # setup room data
        else:
            print('Problem joining room.')

    def watch_songs(self):
        ''' watch for unauthorized + authorized song changes'''
        print('Monitoring Spotify...')

        while 1:
            time.sleep(2) #check every two seconds
            self.mac_scripts.get_current_playing()
            self.mac_scripts.get_song_url()

def main():
    ''' main '''
    try:
        Spoticast()
    except EOFError:
        print('\n Closing application...\n')
    except KeyboardInterrupt:
        print('\n Closing application...\n')
