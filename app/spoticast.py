#!/usr/bin/python3
''' main cli for spotipy rooms '''
from __future__ import absolute_import, unicode_literals
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

        self.type = None
        self.room_addr = None

        self.room_status = {
            "song": "",
            "song_url": "",
            "play": False,
            "time": 0.0
        }

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
            '-j', '--join', help='join room [ADDR]', type=str, dest="join"
        )

        args = parser.parse_args()
        if args.init:
            self.host_room()
        elif args.join:
            self.join_room(args.join)

    def host_room(self):
        ''' host a room '''
        print('Sending host request...')
        self.parent.start() # run in background
        self.room_addr = self.sockets.create_room()

        self.mac_scripts.play()
        artist, song, current_time = self.mac_scripts.get_current_playing().split(" - ")
        uri = self.mac_scripts.get_song_url()

        self.room_status = {
            "song": artist + " - " + song,
            "song_url": uri,
            "play": True,
            "time": float(current_time)
        }

        self.sockets.send_room(self.room_addr, self.room_status)
        self.type = 'HOST'

        print('Joined room: %s' % self.room_addr)
        print('Ctrl C to close room.')

    def join_room(self, addr):
        ''' joins a room of room address addr '''
        print('Sending join request...')
        self.room_status = self.sockets.join_room(addr)
        if self.room_status != {}:
            self.room_addr = addr
            self.type = 'USER'
            self.mac_scripts.listen_uri(self.room_status.song_uri)
            self.mac_scripts.set_time(self.room_status.time)
        else:
            print('Problem joining room.')

    def send_room(self):
        ''' sends room info for hosts '''
        self.sockets.send_room(self.room_addr, self.room_status) # status

    def check_room(self):
        ''' checks room info for users '''
        return self.sockets.check_room(self.room_addr) # {} or data

    def watch_songs(self):
        ''' watch for song changes from the host '''
        print('Monitoring Spotify...')
        last_time = 0.0
        last_uri = ''
        last_state = True

        while 1:
            # current spotify status
            artist, song, current_time = self.mac_scripts.get_current_playing().split(" - ")
            uri = self.mac_scripts.get_song_url()

            if self.type == 'HOST':
                self.room_status = {
                    "song": artist + " - " + song,
                    "song_url": uri,
                    "play": current_time > last_time,
                    "time": float(current_time)
                }
                if last_uri != uri:
                    self.send_room()
                time.sleep(2) # faster checking for host
            elif self.type == 'USER':
                self.room_status = self.check_room()
                if self.room_status != {}:
                    if last_state != self.room_status.play:
                        self.mac_scripts.play_pause()
                    if last_uri != self.room_status.song_uri:
                        self.mac_scripts.listen_uri(self.room_status.song_uri)
                time.sleep(10) # dont want to overload the server
            else:
                time.sleep(2)

            last_state = current_time > last_time
            last_uri, last_time = uri, float(current_time)


def main():
    ''' main '''
    try:
        Spoticast()
    except EOFError:
        print('\n Closing application...\n')
    except KeyboardInterrupt:
        print('\n Closing application...\n')
