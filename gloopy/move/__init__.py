'''
The classes in this package are designed to be instantiated, setting parameters
such as speed of movement or angular velocity, and then assigned to a
GameItem's ``update`` attribute. 

Every frame, world.update will invoke the update attribute of each item,
passing the item, the time, and the dt since the last frame.

These classes, when invoked like this, will modify the position or
orientation of the passed item.
'''
from . newtonian import Newtonian
from . orbit import Orbit, WobblyOrbit
from . spin import Spinner, WobblySpinner

