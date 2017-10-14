<p align="center">
<img src='SPOTIPLAY.png' height='200'>
</p>

Ever wanted to be your own DJ for your friends? spoticast is here for ya!

### Installation

Installing is as easy as 1, 2, 3!
```bash
$ git clone https://github.com/jaruserickson/spoticast.git
$ cd spoticast
$ sudo python setup.py install
```

### Usage

#### Hosting:
```bash
$ spoticast -i
Created room barnacle-hunter.
Ctrl C to close room.
```
You can then simply play songs from the spotify app, and spoticast will broadcast it to your friends :). 

#### Joining friends:
```bash
$ spoticast -j barnacle-hunter
Joined room barnacle-hunter.
Now Playing: HUMBLE - Kendrick Lamar @ 1:23
$ spoticast -q
Left room barnacle-hunter.
Bye!
```

### Tech

- Python3
- AppleScript
- Multiprocessing
- Sockets
- AWS EC2
