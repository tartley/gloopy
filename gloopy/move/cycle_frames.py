
class CycleFrames(object):
    '''
    cycles the item's `frame` attribute through values 0...n-1, where n is
    length of the item's `shape` collection. `frame` is advanced every `period`
    seconds.
    '''
    def __init__(self, period):
        self.period = period

    def __call__(self, item, time, dt):
        if isinstance(item.shape, list):
            if hasattr(item, 'frame_changed'):
                if (time - item.frame_changed) > self.period:
                    item.frame = (item.frame + 1) % len(item.shape)
                    item.frame_changed = time
            else:
                item.frame = 0
                item.frame_changed = time
        else:
            item.frame = 0

