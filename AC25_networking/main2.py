import socket as sock
from threading import Thread
import os
import time
import sys

HOST = '127.0.0.1'
PORT = 9999
END_GAME = 'EXIT'
STORY = 'STORY'
USER = 'USER'


class Client:
    def __init__(self, username):
        self.s_client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.connected = True
        self.username = username
        self.cur_line = ''
        try:
            self.s_client.connect((HOST, PORT))
            self.listen_thread = Thread(target=self.listen, daemon=True)
            self.listen_thread.start()
        except sock.error as e:
            print(e)
            print('Could not connect to the server')

    def listen(self):
        # send username
        username_bytes = str(USER + ': ' + self.username).encode()
        self.s_client.send(username_bytes)
        while self.connected:
            data = self.s_client.recv(1024)
            message = data.decode()
            # check if it is end game
            if END_GAME in message:
                print(message)
                break
            elif STORY in message:
                self.cur_line = message
                print(message)
                # start thread to clean consoler
                timer = Thread(target=self.clean_window, args=(message,), daemon=True)
                timer.start()
            else:
                print(message)
        self.s_client.close()

    def send_message(self, text):
        # encode text
        data = text.encode()
        self.s_client.send(data)

    def clean_window(self, line):
        time.sleep(20)
        # clean consoler
        os.system('cls')


class Server:
    def __init__(self):
        self.s_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.s_server.bind((HOST, PORT))
        self.connected = True
        self.players = []
        self.player_usernames = dict()
        # marking whose turn it is
        self.turn = None
        # current STORY
        self.story = []
        self.s_server.listen(5)
        while self.connected:
            new_player, addr = self.s_server.accept()
            print('New connection: {}'.format(addr))
            self.players.append(new_player)
            if not self.turn:
                # new_player is the first player
                self.turn = new_player
            client_thread = Thread(target=self.handle, args=(new_player,), daemon=True)
            client_thread.start()
        self.close_all(self.players)
        self.s_server.close()
        sys.exit()

    def handle(self, client_socket):
        # receives a client socket and does the listening and sending
        # messages
        assert isinstance(client_socket, sock.socket)
        while self.connected:
            data = client_socket.recv(1024)
            message = data.decode()
            if USER in message:
                # add user to dict
                username = message.strip(USER + ': ')
                self.player_usernames[client_socket] = username
            else:
                new_story_list = message.split(' ')
                if client_socket != self.turn:
                    # not his turn yet
                    message = 'Not your turn yet'
                    client_socket.send(message.encode())
                elif self.check_story(new_story_list, self.story):
                    print('STORY CHECKED OUT')
                    # story checks out, update story
                    self.story = new_story_list
                    # send new story to everyone
                    self.send_story_to_all(self.story, self.players)
                    # update to the next player
                    index = self.players.index(self.turn)
                    self.turn = self.players[(index + 1) % len(self.players)]
                else:
                    print('ENDING STORY')
                    # player got it wrong, end game
                    self.send_end_game_to_all(self.players, s_loser=client_socket)
                    self.connected = False


    def check_story(self, new_story_list, story_list):
        # check if new_story_list matches with story_list
        if len(story_list) == 0:
            return True
        if len(new_story_list) < 3:
            # need at least three wordss
            return False
        return new_story_list[:-3] == story_list

    def send_story_to_all(self, story_list, players):
        # sends story list to all players
        # convert story list to a story string by adding spaces
        story = STORY + ': ' + ' '.join(story_list)
        story_bytes = story.encode()
        for p in players:
            assert isinstance(p, sock.socket)
            p.send(story_bytes)
        time.sleep(3)

    def close_all(self, players):
        print('CLOSING ALL PLAYERS')
        for p in players:
            p.close()

    def send_end_game_to_all(self, players, s_loser):
        message = 'Game ended: ' + END_GAME
        loser = 'Loser: {l}'.format(l=self.player_usernames[s_loser])
        message += '\n' + loser
        message_bytes = message.encode()
        for p in players:
            assert isinstance(p, sock.socket)
            p.send(message_bytes)


if __name__ == '__main__':
    reply = input('Enter s for server and c for client: \n')
    if reply == 's':
        s = Server()
    elif reply == 'c':
        username = input('Enter username: ')
        c = Client(username)
        while c.connected:
            r = input('Enter: ')
            c.send_message(r)
