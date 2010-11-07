
class Newtonian(object):
    '''
    Modify locus if item.position by adding item.velocity to it.
    Similarly add item.velocity to item.acceleration, and add angular_velocity
    to item.orientation.
    '''
    def __init__(self):
        self.gameitem = None

    def __call__(self, _, dt):
        item = self.gameitem
        if item.velocity is not None and item.acceleration is not None:
            item.velocity += item.acceleration * dt
        if item.position is not None and item.velocity is not None:
            item.position += item.velocity * dt 
        if item.angular_velocity:
            speed, axis = item.angular_velocity.get_angle_axis()
            item.orientation.rotate_axis(speed * dt, axis)

