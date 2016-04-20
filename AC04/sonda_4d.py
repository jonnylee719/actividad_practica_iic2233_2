

'''
Modulo para sonda
'''


class Sonda():

    def __init__(self, minerales):
        # lista de las cordinadas de minerales
        self.minerales = minerales
        self.dict_coord = dict()
        self.leer(minerales)

    def leer(self, minerales):
        for line in minerales:
            split = line.split(',')

            # Testing purpose
            # print(split)

            # coordinada
            coor = (split[0].strip(), split[1].strip(), split[2].strip(), split[3].strip())
            # valor
            mineral = split[4].strip()
            self.dict_coord[coor] = mineral

    def run(self):
        pass
        # Pregunta al usuario numero de consulta
        exit_loop = False

        while not exit_loop:
            print(""" Numero de consultas """)
            numero = int(input())

            while numero > 0:
                # pregunta por cordinada
                cord = input()
                cord_split = cord.split(",")
                while len(cord_split) != 4:
                    cord = input()
                    cord_split = cord.split(",")
                # cord_split tiene 4 numeros
                self.pregunta_cordinada(cord_split[0].strip(), cord_split[1].strip(),
                                        cord_split[2].strip(), cord_split[3].strip())

    def pregunta_cordinada(self, x, y, z, u):
        coord = (str(x), str(y), str(z), str(u))

        #Testing purpose
        #print(coord)

        mineral = self.dict_coord.get(coord, "No hay nada")
        print(mineral)

