# coding=utf-8
import socket as sock
from threading import Thread
from threading import Lock
import sys
import time
import os

HOSTNAME = '127.0.0.1'
PORT = 9999
NO_TURNO = 'No es tu turno'
TERMINAR_JUEGO = 'EXIT'

class Client:
    def __init__(self, name):
        self.s_client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.connected = True
        self.username = name
        try:
            self.s_client.connect((HOSTNAME, PORT))
            receiver = Thread(target=self.listen)
            receiver.start()
        except sock.error:
            print('No fue posible hacer la conexion')
            sys.exit()

    def listen(self):
        while self.connected:
            data = self.s_client.recv(1024)
            assert isinstance(data, bytes)
            message = data.decode('utf-8')
            if TERMINAR_JUEGO in message:
                print(message)
                print('Juego termino')
                self.s_client.close()
            else:
                print('Historia actual: {}'.format(message))
                timer = Thread(target=self.clean_console, daemon=True)
                timer.start()

    def send_message(self, text):
        message = self.username + ': ' + text
        self.s_client.send(message.encode())

    def clean_console(self):
        time.sleep(20)
        os.system('cls')


class Server:
    def __init__(self):
        self.s_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.s_server.bind((HOSTNAME, PORT))
        self.s_server.listen(5)
        self.connected = True
        self.jugadores = []

        self.lock = Lock()
        self.turno = None
        self.historia = []
        while True:
            s_client, addr = self.s_server.accept()
            self.jugadores.append(s_client)
            if not self.turno:
                self.turno = s_client
            thread_client = Thread(target=self.listen, args=(s_client,), daemon=True)
            thread_client.start()

    def listen(self, s_client):
        while self.connected:
            # recibe las palabras de la historia
            historia_nueva = s_client.recv(1024)
            historia_nueva = historia_nueva.decode('utf-8')
            # chaquear si es su turno
            assert isinstance(historia_nueva, str)
            print('Server received: {}'.format(historia_nueva))
            assert ': ' in historia_nueva
            jugador, historia = historia_nueva.split(': ')
            if s_client != self.turno:
                self.send_message(NO_TURNO, s_client)
            else:
                # hace una lista de palabras la historia
                historia_lista = historia.split(' ')
                if self.historia_valida(historia_lista):
                    self.historia = historia_lista
                    for jugador in self.jugadores:
                        if jugador != s_client:
                            self.send_message(' '.join(self.historia), jugador)
                    # busca el siguiente jugador
                    i = self.jugadores.index(self.turno)
                    # actualiza jugador
                    i = (i + 1) % len(self.jugadores)
                    self.turno = self.jugadores[i]
                else:
                    # termina juego
                    self.termina_juego()

    def historia_valida(self, nuevo_historia):
        nueva_palabras = nuevo_historia[-3:]
        return nuevo_historia[:-3] == self.historia

    def send_message(self, text, s_client):
        assert isinstance(s_client, sock.socket)
        s_client.send(text.encode())

    def termina_juego(self):
        for c in self.jugadores:
            c.send(TERMINAR_JUEGO.encode())
        time.sleep(5)
        sys.exit()


if __name__ == '__main__':
    r = input('Ingrese S para servidor o C para cliente')
    if r == "S":
        server = Server()

    elif r == "C":
        nombre = input("Ingrese el nombre del usuario: ")
        client = Client(nombre)
        while True:
            texto = input()
            client.send_message(texto)