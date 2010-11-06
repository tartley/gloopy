
class Linear(object):

    gameitem = None

    def __call__(self, dt, t):
        item = self.gameitem
        if item.velocity is not None and item.acceleration is not None:
            item.velocity += item.acceleration
        if item.position is not None and item.velocity is not None:
            item.position += item.velocity

