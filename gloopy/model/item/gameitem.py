
from ...geom.vec3 import Vec3


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
        # if any supposed Vec3 attributes have been passed as a tuple for
        # convenience, convert them into Vec3
        for attr in ['position', 'velocity', 'acceleration']:
            if attr in kwargs:
                if not isinstance(kwargs[attr], Vec3):
                    kwargs[attr] = Vec3(*kwargs[attr])

        # attach all passed kwargs to ourself as attributes
        self.__dict__.update(kwargs)


def position_or_gameitem(item):
    if isinstance(item, Vec3):
        return item
    else:
        return item.position

