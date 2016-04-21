# debes definir la metaclase 'Meta' a continuacion
def create_property(name, type):
    def setter(self, val):
        if isinstance(val, type):
            self.__dict__[name] = val
        else:
            print('Wrong attribute type')

    def getter(self):
        return self.__dict__.get(name)

    return property(getter, setter)


class Meta(type):
    def __new__(cls, name, bases, attrs):
        for key, val in attrs.items():
            if isinstance(val, type):
                # Not protected attributes
                attrs[key] = create_property(key, val)
        return super().__new__(cls, name, bases, attrs)

# debes definir las clases 'Person' y 'Company' a continuacion
class Person(metaclass=Meta):
    name = str
    age = int


class Company(metaclass=Meta):
    name = str
    stock_value = float
    employee = list


# El resto es para probar tu programa
if __name__ == '__main__':

    c = Company()
    c.name = 'Apple'
    c.stock_value = 125.78
    c.employees = ['Tim Cook', 'Kevin Lynch']

    print(c.name, c.stock_value, c.employees, sep=', ')

    p = Person()
    p.name = 'Karim'
    p.age = 'hola'
    # Esto debiese imprimir 'ERROR'

    print(p.name, p.age, sep=', ')
