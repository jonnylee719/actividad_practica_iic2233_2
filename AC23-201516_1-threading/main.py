__author__ = ['Bastian','Jm']
import threading
import time
import random


class MegaGodzilla(threading.Thread):

    ###
    # Tienen que completar la clase (piensen en los locks necesarios)
    ###
    gozilla_lock = threading.Lock()

    def __init__(self, hp):
        super().__init__()
        self.hp = hp
        self.soldados = []

    @property
    def vivo(self):
        if self.hp > 0:
            return True
        return False

    ###
    # Tienen que programar el método run
    ###
    def run(self):
        while True:
            s_vivo = list(filter(lambda s: s.vivo, self.soldados))
            if len(s_vivo) > 0:
                # Hay soldados vivo
                rand_ataque = random.random()
                if rand_ataque < 0.7:
                    # ataque normal
                    self.ataque_normal()
                else:
                    self.ataque_ultima()
                # descansar despues el ataque
                time.sleep(random.randint(3, 6))
            else:
                # Todos los soldados estan muertos
                return

    def atacado(self, soldado):
        self.hp -= soldado.ataque
        if not self.vivo:
            print("MegaGodzilla ha muerto!!")
        else:
            print(
                "Mega-Godzilla ha sido atacado! El soldado le ha hecho " + str(
                    soldado.ataque) + " de dano" +
                ". HP Godzilla " + str(self.hp))
            soldado.atacado(int(soldado.ataque / 4))

    ###
    # Programar método atacar
    ###
    def ataque_normal(self):
        for s in self.soldados:
            # Hace 3 danos a cada soldado
            if s.vivo:
                s.atacado(3)

    def ataque_ultima(self):
        Soldado.inmovilizado = True
        for s in self.soldados:
            if s.vivo:
                s.atacado(6)


class Soldado(threading.Thread):

    ###
    # Tienen que completar la clase (piensen en los locks necesarios)
    ###
    # Lock para soldados ataqas
    lock_soldado = threading.Lock()
    inmovilizado = False

    def __init__(self, MegaGodzilla, velocidad, hp, ataque):
        super().__init__()
        self.MegaGodzilla = MegaGodzilla
        self.velocidad = velocidad
        self.hp = hp
        self.ID = next(Soldado.get_i)
        self.ataque = ataque

    @property
    def vivo(self):
        if self.hp > 0:
            return True
        return False

    ###
    # Tienen que programar el método run
    ###
    def run(self):
        # metodo para ejecutar en thread.start()
        with Soldado.lock_soldado:
            if Soldado.inmovilizado:
                time.sleep(10)
                Soldado.inmovilizado = False
            # hace el ataque si tiene lock
            self.MegaGodzilla.atacado(self)
            # la duracion del ataque
            time.sleep(random.randint(1, 3))
        # Descansar despues el ataque
        time.sleep(random.randint(4, 19))

    def atacado(self, ataque):
        self.hp -= ataque
        print("El soldado" + str(self.ID) +
              " ha sido danado!!  HP " + str(self.hp))
        if not self.vivo:
            print("El soldado" + str(self.ID) + " ha muerto :( !!!")

    def id_():
        i = 0
        while True:
            yield i
            i += 1

    get_i = id_()


if __name__ == "__main__":
    print("Comenzo la Simulacion!")

    ###
    # Tienen que programar el main completo
    ###
    gozilla = MegaGodzilla(100)
    soldados = []
    for __ in range(0, 10):
        # 10 soldados
        s = Soldado(gozilla, 2, 50, 2)
        s.start()
        soldados.append(s)
    gozilla.soldados = soldados
    gozilla.start()

