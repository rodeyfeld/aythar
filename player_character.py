import arcade
import animated_entity_sprite
import bullet_sprite
from config import *


class PlayerCharacter(animated_entity_sprite.AnimatedEntitySprite):

    def __init__(self, texture_list, center_x, center_y, bullet_types, health=3, damage=1):
        super().__init__(texture_list=texture_list, center_x=center_x, center_y=center_y)
        self.scale = SCALING
        self.bullet_types = bullet_types
        self.bullet_list = arcade.SpriteList()
        self.health = health
        self.damage = damage
        print("Player", self.textures)

    # def setup(self):
    #     self.bullet_list = arcade.SpriteList()

    def create_bullet(self, change_x, change_y):
        bullet_type = self.bullet_types[0]
        bullet = bullet_sprite.BulletSprite(
            bullet_type=bullet_type,
            center_x=self.center_x,
            center_y=self.center_y + PLAYER_SPRITE_OFFSET,
            change_x=change_x,
            change_y=change_y
        )
        bullet.scale = .5
        self.bullet_list.append(bullet)

    def update(self):
        super().update()
        if self.change_y != 0:
            self.center_y += self.change_y
        if self.change_x != 0:
            self.center_x += self.change_x
