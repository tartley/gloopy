
from euclid import Vector3


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
        # if any supposed Vector3 attributes have been passed as a tuple for
        # convenience, convert them into Vector3
        vec3_attributes = [
            'position', 'velocity', 'accelleration',
        ]
        for attr in vec3_attributes:
            if attr in kwargs:
                if not isinstance(kwargs[attr], Vector3):
                    kwargs[attr] = Vector3(*kwargs[attr])

        # kwargs with a .gameitem attribute should be told which gameitem
        # instance they are being attached to
        for name, value in kwargs.items():
            if hasattr(value, 'gameitem'):
                value.gameitem = self

        # attach all passed kwargs to ourself as attributes
        self.__dict__.update(kwargs)

