
from __future__ import division

from pyglet.window import key 

from ..util.vectors import (
    neg_x_axis, neg_y_axis, neg_z_axis, x_axis, y_axis, z_axis,
)

controls = {
    key.D: x_axis,
    key.A: neg_x_axis,
    key.S: z_axis,
    key.W: neg_z_axis,
    key.UP: y_axis,
    key.DOWN: neg_y_axis,
}


class KeyHandler(object):

    def __init__(self, player):
        self.player = player
        self.pressed = set()
        self.pressed_order = []


    def on_key_press(self, symbol, modifiers):
        self.pressed.add(symbol)
        self.pressed_order.append(symbol)
        self.send_input(self.pressed_order[-1])


    def on_key_release(self, symbol, modifiers):
        self.pressed.remove(symbol)
        while self.pressed_order and self.pressed_order[-1] not in self.pressed:
            self.pressed_order.pop()

        if self.pressed:
            last_key = self.pressed_order[-1]
            self.send_input(last_key)
        else:
            self.player.update.input = None


    def send_input(self, symbol):
        if symbol in controls:
            self.player.update.input = controls[symbol]

