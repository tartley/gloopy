
from ...geom.vector import Vector


class GameItem(object):

    _next_id = 0

    def __init__(self, **kwargs):
        self.id = GameItem._next_id
        GameItem._next_id += 1

        self.shape = None
        self.glyph = None

        self.position = None
        self.velocity = None
        self.acceleration = None

        self.orientation = None
        self.angular_velocity = None

        self.update = None

        self._apply_kwargs(**kwargs)


    def __repr__(self):
        return '<GameItem %s>' % (
            ' '.join(
                '%s=%s' % (name, value)
                for name, value in self.__dict__.iteritems()
                if not name.startswith('_')
            )
        )


    def _apply_kwargs(self, **kwargs):
        '''
        Attach the given kwargs as attributes on self
        '''
        # if any supposed Vector attributes have been passed as a tuple for
        # convenience, convert them into Vector
        for attr in ['position', 'velocity', 'acceleration']:
            if attr in kwargs:
                if not isinstance(kwargs[attr], Vector):
                    kwargs[attr] = Vector(*kwargs[attr])

        # attach all passed kwargs to ourself as attributes
        self.__dict__.update(kwargs)


def position_or_gameitem(item):
    if isinstance(item, Vector):
        return item
    else:
        return item.position

