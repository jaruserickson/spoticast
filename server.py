''' server.py '''
import socket
import json
import random
import requests

WORD_SITE = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
WORDS = requests.get(WORD_SITE).content.splitlines()

def random_key():
    ''' get a random key from bsd words '''
    return str(random.choice(WORDS))[2:-1] + '-' + str(random.choice(WORDS))[2:-1]

def create_server():
    ''' create a server object '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = ''
    port = 8080
    sock.bind((host, port)) # bind to the port
    sock.listen(5) # queue up to 5 requests

    rooms = {}
    print('Server initialized at ' + str(port))

    while 1:
        # establish a connection
        client, addr = sock.accept()
        addr = addr[0]

        print('Connection from %s' % str(addr))
        command = client.recv(1024).decode('utf-8')
        if command[0] == '/':
            if command == '/CREATE_ROOM':
                # creates a room at request of host
                print('CREATE_ROOM request from %s' % str(addr))
                room_key = random_key()
                rooms[room_key] = {
                    "song": "",
                    "song_uri": "",
                    "play": False,
                    "time": 0.0
                }
                client.send((room_key).encode('utf-8'))

            elif command == '/JOIN_ROOM':
                # basically syncs the user up to the room
                print('JOIN_ROOM request from %s' % str(addr))
                room_addr = client.recv(1024).decode('utf-8')
                if rooms[room_addr]:
                    client.send(json.dumps(rooms[room_addr]).encode('utf-8'))
                else:
                    client.send(('@ ERROR: Invalid room address').encode('utf-8'))

            elif command == '/SEND_ROOM':
                # take data from the host
                print('SEND_ROOM request from %s' % str(addr))
                room_addr = client.recv(1024).decode('utf-8')
                if rooms[room_addr]:
                    room_data = json.loads(client.recv(1024).decode('utf-8'))
                    rooms[room_addr] = room_data
                    client.send(('Updated.').encode('utf-8'))
                else:
                    client.send(('@ ERROR: Invalid room address').encode('utf-8'))

            elif command == '/GET_ROOM':
                # send data to the user
                print('GET_ROOM request from %s' % str(addr))
                room_addr = client.recv(1024).decode('utf-8')
                if rooms[room_addr]:
                    client.send(json.dumps(rooms[room_addr]).encode('utf-8'))
                else:
                    client.send(('@ ERROR: Invalid room address').encode('utf-8'))

            else:
                print('Unknown command received.')
        else:
            print('Unknown command received.')

        client.close()

    sock.close()

if __name__ == "__main__":
    create_server()
