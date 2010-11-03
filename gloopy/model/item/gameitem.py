
from euclid import Vector3

from ...util.vectors import origin


class GameItem(object):

    _next_id = 0

    def __init__(self, **kwargs):
        self.id = GameItem._next_id
        GameItem._next_id += 1
        self.apply_kwargs(**kwargs)


    def __repr__(self):
        return '<GameItem %s>' % (
            ' '.join(
                '%s=%s' % (name, value)
                for name, value in self.__dict__.iteritems()
                if not name.startswith('_')
            )
        )


    def apply_kwargs(self, **kwargs):
        if 'position' in kwargs:
            position = kwargs.pop('position')
            if position is None:
                position = origin
            elif not isinstance(position, Vector3):
                position = Vector3(*position)
            self.position = position
        
        self.__dict__.update(kwargs)

