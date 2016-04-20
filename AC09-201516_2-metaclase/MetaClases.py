import functools

class MetaRobot(type):
    def __new__(cls, cls_name, bases, attrs):
        # Coroborrar cls_name es Robot, tirar error si no
        if cls_name != 'Robot':
            raise AttributeError('Clase no es Robot')
        # Agregar creador y ip_inicio como atributos de la clase
        # Suponga creador id = 123
        # ip_inicio = 190.102.62.283
        attrs.update({'creador': 'abc'})
        attrs.update({'ip_inicio': '190.102.62.283'})
        # crear un metodo check_creator
        def check_creator(self):
            lst = list(filter(lambda x: x == self.creador, self.creadores))
            return len(lst) > 0
        # crear un metodo cortar_conexion
        def cortar_conexion(self):
            if self.actual.hacker != 0:
                # tenemos un hacker
                print('Tenemos un hacker')
                self.actual.hacker = 0
        # crear un metodo cambiar_nodo
        def cambiar_nodo(self, puerto):
            print("de {0} a ".format(self.actual.ide), end="")
            self.actual = puerto
            print("{0}".format(puerto.ide))
        attrs.update({'check_creator': check_creator})
        attrs.update({'cortar_conexion': cortar_conexion})
        attrs.update({'cambiar_nodo': cambiar_nodo})
        return super().__new__(cls, cls_name, bases, attrs)

    def __init__(cls, cls_name, bases, attrs):
        pass
