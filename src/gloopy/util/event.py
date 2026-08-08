
class Event(object):
    '''
    Used when many subscribers would to recieve a function call from a single
    sender.

    .. function:: __init__()

    Subscribe by in-place-add (+= or __iadd__) a callable of the right
    signature. e.g::

        def handler(this, that):
            pass

        event = Event()
        event += handler

        event.fire(1, 2)

    The .fire call will invoke `handler`, passing 1 and 2, and will also
    invoke all other subscribers to this event.
    '''
    def __init__(self):
        self.listeners = []

    def __iadd__(self, listener):
        self.listeners.append(listener)
        return self

    def fire(self, *args, **kwargs):
        '''
        call all subscribers to the event
        '''
        for listener in self.listeners:
            listener(*args, **kwargs)

