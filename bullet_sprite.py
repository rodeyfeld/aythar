import arcade
import animated_entity_sprite


class BulletSprite(animated_entity_sprite.AnimatedEntitySprite):
    def __init__(self, texture_list, center_x, center_y, change_x, change_y):
        super().__init__(texture_list=texture_list, center_x=center_x, center_y=center_y)
        # self.textures = texture_list
        self.change_x = change_x
        self.change_y = change_y
        # Texture has to be set in order for on_draw not to crash
        self.texture = texture_list[0]

    def __str__(self):
        return "BulletSprite: ({0}, {1}) - {2}".format(self.center_x, self.center_y, self.textures)

    def update(self):
        super().update()
        self.center_x += self.change_x
        self.center_y += self.change_y

