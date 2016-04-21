
def create_property(prop):

        def getter(self):
            return self.__dict__.get(prop)

        def setter(self, val):
            if self.__dict__.get(prop) is None:
                self.__dict__[prop] = val
            else:
                raise AttributeError('Cannot set attribute')

        return property(getter, setter)

class RestrictedAccess(type):
    # Metaclass
    def __new__(cls, name, bases, attrs):
        for a in attrs['attributes']:
            attrs.update({a: create_property(a)})
        # Remove the list of "attributes"
        del attrs['attributes']
        return super().__new__(cls, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        fname = args[0]
        lname = args[1]
        alias = args[2]
        # Add the new properties
        instance = super().__call__()
        instance.name = fname
        instance.lastname = lname
        instance.alias = alias
        return instance


class Persona(metaclass=RestrictedAccess):
    attributes = ['name', 'lastname', 'alias']
    def __init__(self, *args):
        pass


if __name__ == '__main__':
    p1 = Persona('Bruce', 'Wayne', 'Batman')
    print(p1.name , p1. lastname , "es", p1.alias , "!")


