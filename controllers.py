from .geometery import Vector


WASD_Controls = {
    "w": Vector(0, 1),
    "s": Vector(0, -1),
    "a": Vector(-1, 0),
    "d": Vector(1, 0),
}


Arrow_Controls = {
    "UPARROW": Vector(0, 1),
    "DOWNARROW": Vector(0, -1),
    "LEFTARROW": Vector(-1, 0),
    "RIGHTARROW": Vector(1, 0),
}


class _KeyBoardController:
    def __init__(self, parent):
        self.parent = parent

    def slow_x(self, engine):
        if self.parent.velocity.x:
            velocity_change = engine.clock.dtime * (self.parent.velocity.x / abs(self.parent.velocity.x)) * self.deceleration
            if abs(velocity_change) > abs(self.parent.velocity.x):
                self.parent.velocity.x = 0
            else:
                self.parent.velocity.x -= velocity_change

    def slow_y(self, engine):
        if self.parent.velocity.y:
            velocity_change = engine.clock.dtime * (self.parent.velocity.y / abs(self.parent.velocity.y)) * self.deceleration
            if abs(velocity_change) > abs(self.parent.velocity.y):
                self.parent.velocity.y = 0
            else:
                self.parent.velocity.y -= velocity_change


class MouseController:
    def __init__(self, parent):
        self.parent = parent

    def update(self, engine):
        if engine.clock.dtime:
            self.parent.pos = engine.mouse.pos
            self.parent.velocity = engine.mouse.pos_change / engine.clock.dtime
        else:
            self.parent.velocity = Vector(0, 0)


class KeyBoardControllerFixed(_KeyBoardController):
    def __init__(self, parent, controls):
        _KeyBoardController.__init__(self, parent)
        self.speed = 1000
        self.controls = controls

    def update(self, engine):
        self.parent.velocity = Vector(0, 0)
        for key_name, movement in self.controls.items():
            if engine.keyboard.is_pressed(key_name):
                self.parent.velocity += movement * engine.clock.dtime * self.speed


class KeyBoardControllerSmooth(_KeyBoardController):
    def __init__(self, parent, controls):
        _KeyBoardController.__init__(self, parent)
        self.deceleration = 50
        self.acceleration = 100
        self.controls = controls

    def update(self, engine):
        total_movement = Vector(0, 0)
        for key_name, movement in self.controls.items():
            if engine.keyboard.is_pressed(key_name):
                total_movement += movement

        self.parent.velocity += total_movement * engine.clock.dtime * self.acceleration
        self.slow_x(engine)
        self.slow_y(engine)

