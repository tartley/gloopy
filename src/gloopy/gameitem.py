
from .geom.vector import Vector
from .geom.orientation import Orientation


class GameItem(object):
    '''
    A dumb collection of attributes, representing a single item to be rendered.

    .. function:: __init__(**kwargs)

        ``kwargs``: contains attributes which are attached to the returned
        instance, for example:
        
        ``shape``: specifies the appearance of the item, as an instance of
        :class:`~gloopy.shapes.shape.Shape`.

        ``position``: specified as a :class:`~gloopy.geom.vector.Vector`.

        ``orientation``: specified as an
        :class:`~gloopy.geom.orientation.Orientation`.

        ``update``: a callable, of the signature:
        
            .. function:: update(self, time, dt)

            This is called in between every render (unless it is None.)

        You should feel free to pass in other attributes, which you might
        use in this item's ``update`` method, for example ``.velocity``, which
        you could use to move this item.

        ``glyph``: is used to store the shape converted into a VBO which OpenGL
        can render. If you update a ``GameItem`` shape, you must also update
        its glyph attribute using
        :func:`~gloopy.view.shape_to_glyph.shape_to_glyph`.

        In addition, the attribute ``.id`` is assigned a unique integer.
    '''

    _next_id = 0

    def __init__(self, **kwargs):
        self.id = GameItem._next_id
        GameItem._next_id += 1

        self.shape = None
        self.glyph = None

        self.position = Vector.origin
        self.velocity = None
        self.acceleration = None

        self.orientation = Orientation.Identity
        self.angular_velocity = None

        self.update = None

        self._apply_kwargs(**kwargs)


    def __repr__(self):
        return '<GameItem %s>' % (
            ' '.join(
                '%s=%s' % (name, value)
                for name, value in self.__dict__.items()
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
    '''
    If item is a :class:`~gloopy.geom.vector.Vector`, return it, otherwise
    assume it is a :class:`GameItem` with a position attribute, and return
    that instead.
    '''
    if isinstance(item, Vector):
        return item
    else:
        return item.position

