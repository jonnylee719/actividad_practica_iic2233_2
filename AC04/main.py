import sonda_4d
from collections import deque


# coding=utf-8


# Completen los métodos
# Les estamos dando un empujoncito con la lectura del input
# Al usar la clausula: "with open('sonda.txt', 'r') as f", el archivo se cierra automáticamente al salir de la función.


def sonda():
    with open('sonda.txt', 'r') as f:
        minerales = []
        for line in f:
            minerales.append(line)
        # Creamos una clase sonda que va recibir minerales
        s = sonda_4d.Sonda(minerales)
        # print(s.dict_coord[("7679", "-9626", "9126", "-6320")])
        s.run()


def traidores():
    with open('bufalos.txt', 'r') as f:
        bufalos = set()
        for line in f:
            bufalos.add(line.strip())

    with open('rivales.txt', 'r') as f:
        rivales = set()
        for line in f:
            rivales.add(line.strip())

    print(*bufalos.intersection(rivales), sep='\n')

def pizzas():
    with open('pizzas.txt', 'r') as f:
        p = Pizzeria()
        for line in f.read().splitlines():
            if line.strip() == 'APILAR':
                p.apilar()
            elif line.strip() == 'ENCOLAR':
                p.encolar()
            elif line.strip() == 'SACAR':
                p.sacar()

class Pizzeria():

    def __init__(self):
        self.apila = []
        self.cola = deque()
        self.nombre_pizza = 1

    def apilar(self):
        self.apila.append(self.nombre_pizza)
        self.print_status("apilada", self.nombre_pizza)
        self.nombre_pizza += 1

    def encolar(self):
        pizza_nombre = self.apila.pop()
        self.cola.append(pizza_nombre)
        self.print_status("encolar", pizza_nombre)

    def sacar(self):
        pizza_nombre = self.cola.popleft()
        self.print_status("sacada", pizza_nombre)

    def print_status(self, accion, nombre):
        apilada = len(self.apila)
        encolada = len(self.cola)

        label_apilada = ' Pizzas Apiladas'
        label_encolada = ' Pizzas en cola'

        if apilada == 1:
            label_apilada = ' Pizza Apilada'
        if encolada == 1:
            label_encolada = ' Pizza en cola'

        label_apilada = str(apilada) + label_apilada
        label_encolada = str(encolada) + label_encolada

        print("Pizza {0} {1}. {2} - {3}"
              .format(nombre, accion, label_apilada, label_encolada))

if __name__ == '__main__':
    exit_loop = False

    functions = {"1": sonda, "2": traidores, "3": pizzas}

    while not exit_loop:
        print(""" Elegir problema:
            1. Sonda
            2. Traidores
            3. Pizzas
            Cualquier otra cosa para salir
            Respuesta: """)

        user_entry = input()

        if user_entry in functions:
            functions[user_entry]()
        else:
            exit_loop = True
