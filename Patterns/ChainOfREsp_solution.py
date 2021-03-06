class EventGet:

    def __init__(self, type_):
        self.name = 'get'
        self.type_ = type_


class EventSet:

    def __init__(self, value):
        self.name = 'set'
        self.value = value
        self.type_ = type(value)


class NullHandler:

    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class StrHandler(NullHandler):

    def handle(self, obj, event):
        if issubclass(event.type_, str):
            if event.name == 'set':
                obj.string_field = event.value
            else:
                return obj.string_field
        else:
            return super().handle(obj, event)


class IntHandler(NullHandler):

    def handle(self, obj, event):
        if issubclass(event.type_, int):
            if event.name == 'set':
                obj.integer_field = event.value
            else:
                return obj.integer_field
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):

    def handle(self, obj, event):
        if issubclass(event.type_, float):
            if event.name == 'set':
                obj.float_field = event.value
            else:
                return obj.float_field
        else:
            return super().handle(obj, event)


if __name__ == '__main__':
    class SomeObject:
        def __init__(self):
            self.integer_field = 0
            self.float_field = 0.0
            self.string_field = ""

    # from solution import *
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"
    chain = IntHandler(FloatHandler(StrHandler(NullHandler())))
    chain.handle(obj, EventGet(int))

    chain.handle(obj, EventGet(float))

    chain.handle(obj, EventGet(str))

    chain.handle(obj, EventSet(100))
    chain.handle(obj, EventGet(int))
    chain.handle(obj, EventSet(0.5))
    chain.handle(obj, EventGet(float))
    chain.handle(obj, EventSet('new text'))
    chain.handle(obj, EventGet(str))
    obj = SomeObject()
    obj.integer_field = 33
    obj.float_field = -8.5058
    obj.string_field = "NbJPnz"
    chain.handle(obj, EventGet(int))
