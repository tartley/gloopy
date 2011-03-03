
class Event(object):

    def __init__(self):
        self.listeners = []

    def __iadd__(self, listener):
        self.listeners.append(listener)
        return self

    def fire(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)

