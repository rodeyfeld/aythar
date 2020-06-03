import arcade


class PropSprite(arcade.Sprite):
    def __init__(self, asset, scaling, x, y):
        super().__init__(asset, scaling)
        self.asset = asset
        self.center_x = x
        self.center_y = y

    def __str__(self):
        return "({0}, {1}) - {2}".format(self.center_x, self.center_y, self.asset)
