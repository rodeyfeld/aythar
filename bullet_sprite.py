import arcade
import animated_entity_sprite


class BulletSprite(animated_entity_sprite.AnimatedEntitySprite):
    def __init__(self, texture_list, center_x, center_y, change_x, change_y):
        super().__init__(texture_list, center_x, center_y)

