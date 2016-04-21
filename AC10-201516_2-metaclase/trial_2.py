
def create_property(name):
    def setter(self, val):
        if self.__dict__.get(name) is None:
            self.__dict__[name] = val
        else:
            raise AttributeError

    def getter(self):
        return self.__dict__.get(name)

    return property(getter, setter)


class RestrictedAccess(type):
    def __new__(cls, name, bases, attrs):
        for a in attrs['attributes']:
            attrs.update({a: create_property(a)})
        return super().__new__(cls, name, bases, attrs)

    def __call__(self, *args, **kwargs):
        inst = super().__call__(*args, **kwargs)
        for i in range(len(inst.attributes)):
            setattr(inst, inst.attributes[i], args[i])
        del inst.__class__.attributes
        return inst


class Persona(metaclass=RestrictedAccess):
    attributes = ['name', 'lastname', 'alias']
    def __init__(self, *args):
        pass


class Singleton(type):
    instance = None
    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = super().__call__(*args, **kwargs)
        return self.instance


class A(metaclass=Singleton):
    def __init__(self, value):
        self.val = value

if __name__ == '__main__':
    p1 = Persona('Bruce', 'Wayne', 'Batman')
    print(p1.name , p1. lastname , "es", p1.alias , "!")
    print(p1.__dict__)

    a = A(10)
    b = A(20)
    print(a.val, b.val)
    print(a is b)