''' applescript file '''
from __future__ import absolute_import, unicode_literals
import sys
import subprocess

class MacScripts:
    ''' applescript init '''
    def __init__(self):
        '''
            Check if there is a Spotify process running and if not,
            run Spotify.
        '''
        try:
            count = int(subprocess.check_output([
                'osascript',
                '-e', 'tell application "System Events"',
                '-e', 'count (every process whose name is "Spotify")',
                '-e', 'end tell'
                ]).strip())
            if count == 0:
                print('\n[OPENING SPOTIFY] The Spotify app was not open.\n')

                applescript(
                    'tell application "Spotify" to activate'
                )
        except Exception:
            sys.exit('You don\'t have Spotify installed. Please install it.')

    def listen_uri(self, uri):
        ''' tells the spotify app to listen to a song '''
        applescript('tell app "Spotify" to play track "%s"' % uri)

    def set_time(self, time):
        applescript('tell app "Spotify" to set player position to %s' % time)

    def play(self):
        applescript('tell app "Spotify" to play')

    def pause(self):
        applescript('tell app "Spotify" to pause')

    def play_pause(self):
        applescript('tell app "Spotify" to playpause')

    def get_song_url(self):
        out, err = subprocess.Popen(['osascript', '-e', (
                'on getCurrentUrl()\n'
                ' tell application "Spotify"\n'
                '  return id of current track\n'
                ' end tell\n'
                'end getCurrentUrl\n'
                'getCurrentUrl()'
            )], stdout=subprocess.PIPE).communicate()
        return out.decode(sys.getfilesystemencoding()).rstrip()

    def get_current_playing(self):
        ''' returns the current playing song '''
        instruction = ('on getCurrentTrack()\n'
            ' tell application "Spotify"\n'
            '  set currentArtist to artist of current track as string\n'
            '  set currentTitle to name of current track as string\n'
            '  set currentTime to player position as string\n'
            '  return currentArtist & " - " & currentTitle & " - " & currentTime\n'
            ' end tell\n'
            'end getCurrentTrack\n'
            'getCurrentTrack()')
        proc = subprocess.Popen(
            ['osascript', '-e', instruction],
            stdout=subprocess.PIPE)

        out, err = proc.communicate()
        return out.decode(sys.getfilesystemencoding()).rstrip()

def applescript(command):
    ''' makes applescript call '''
    subprocess.call([
        'osascript',
        '-e',
        command
    ])
