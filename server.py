''' server.py '''
import socket
import json
import pickle
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
                print('CREATE_ROOM request from %s' % str(addr))
                room_key = random_key()
                rooms[room_key] = {
                    "songs": [],
                    "state": "PAUSE",
                    "users": [],
                    "host": str(addr)
                }
                client.send((room_key).encode('utf-8'))

            elif command == '/JOIN_ROOM':
                print('JOIN_ROOM request from %s' % str(addr))
                room_addr = client.recv(1024).decode('utf-8')
                if rooms[room_addr]:
                    if str(addr) not in rooms[room_addr]["users"]:
                        rooms[room_addr]["users"].append(str(addr))
                    client.send(json.dumps(rooms[room_addr]).encode('utf-8'))
                else:
                    client.send(('@ ERROR: Invalid room address').encode('utf-8'))

            elif command == '/LEAVE_ROOM':
                print('LEAVE_ROOM request from %s' % str(addr))
                room_addr = client.recv(1024).decode('utf-8')
                if rooms[room_addr]:
                    # reassign host if host leaves
                    if rooms[room_addr]["host"] == str(addr):
                        if len(rooms[room_addr]["users"]) > 0:
                            rooms[room_addr]["host"] = rooms[room_addr]["users"].pop(0)
                        else:
                            del rooms[room_addr]
                    else:
                        rooms[room_addr]["users"].remove(str(addr))
                    client.send(('Room ' + room_addr + ' left.').encode('utf-8'))
                else:
                    client.send(('@ ERROR: Invalid room address').encode('utf-8'))

            elif command == '/PLAY_PAUSE':
                print('PLAYPAUSE request from %s' % str(addr))
                room_addr = client.recv(1024).decode('utf-8')
                if rooms[room_addr]:
                    if rooms[room_addr].host == str(addr):
                        if rooms[room_addr]["state"] == "PLAY":
                            rooms[room_addr]["state"] = "PAUSE"
                        else:
                            rooms[room_addr]["state"] = "PLAY"
                        client.send(json.dumps(rooms[room_addr]).encode('utf-8'))
                    else:
                        client.send(('@ ERROR: Invalid permissions').encode('utf-8'))
                else:
                    client.send(('@ ERROR: Invalid room address').encode('utf-8'))

            elif command == '/NEXT_SONG':
                print('NEXT_SONG request from %s' % str(addr))
                room_addr = client.recv(1024).decode('utf-8')
                if rooms[room_addr]:
                    if rooms[room_addr].host == str(addr):
                        rooms[room_addr]["state"] = "PLAY"
                        rooms[room_addr]["songs"].pop(0)
                        client.send(json.dumps(rooms[room_addr]).encode('utf-8'))
                    else:
                        client.send(('@ ERROR: Invalid permissions').encode('utf-8'))
                else:
                    client.send(('@ ERROR: Invalid room address').encode('utf-8'))

            elif command == '/UPDATE_Q':
                print('UPDATE_Q request from %s' % str(addr))
                room_addr = client.recv(1024).decode('utf-8')
                new_queue = pickle.loads(client.recv(4096))
                if rooms[room_addr]:
                    rooms[room_addr]["songs"] = new_queue["queue"]
                    client.send(('^ Queue updated.').encode('utf-8'))
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
