class Robber:
    def __init__(self, x, y):
        self.pos = PVector(x,y)
        self.speed = 1
        self.col = color(255,33,33)
        self.last = PVector(0, 0)