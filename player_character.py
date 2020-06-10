import arcade
import animated_entity_sprite
import bullet_sprite
from config import *


class PlayerCharacter(animated_entity_sprite.AnimatedEntitySprite):

    def __init__(self, texture_list, center_x, center_y, bullet_types, health=1, damage=1):
        super().__init__(texture_list=texture_list, center_x=center_x, center_y=center_y)
        self.scale = SCALING
        self.bullet_types = bullet_types
        self.bullet_list = None
        self.health = health
        self.damage = damage
        print("Player", self.textures)

    def setup(self):
        self.bullet_list = arcade.SpriteList()

    def create_bullet(self, change_x, change_y):
        bullet_type = self.bullet_types[0]
        bullet = bullet_sprite.BulletSprite(
            texture_list=bullet_type,
            center_x=self.center_x,
            center_y=self.center_y,
            change_x=change_x,
            change_y=change_y
        )
        self.bullet_list.append(bullet)

    def update(self):
        super().update()
        if self.change_y != 0:
            self.center_y += self.change_y
        if self.change_x != 0:
            self.center_x += self.change_x
