import arcade


class EntitySprite(arcade.Sprite):
    def __init__(self, asset, scaling, x, y):
        super().__init__(asset, scaling)
        self.center_x = x
        self.center_y = y
        self.prop_sprite_list = arcade.SpriteList()

    def clear_props(self):
        for _ in range(0, len(self.prop_sprite_list)):
            self.prop_sprite_list.pop()

    def adjust_props(self, change_x=0, change_y=0):
        for prop in self.prop_sprite_list:
            prop.change_x = change_x
            prop.change_y = change_y
