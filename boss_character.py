import arcade
import animated_entity_sprite
import bullet_sprite
from config import *


class BossCharacter(animated_entity_sprite.AnimatedEntitySprite):

    def __init__(self, texture_list, center_x, center_y, bullet_types, health=1, damage=1):
        super().__init__(texture_list=texture_list, center_x=center_x, center_y=center_y)
        self.scale = SCALING * 4
        self.bullet_types = bullet_types
        self.health = health
        self.damage = damage
        print("Boss", self.textures)

    def update(self):
        super().update()
        self.center_y += self.change_y
        if self.center_y < WINDOW_LENGTH - WINDOW_LENGTH // 4:
            self.change_y = 0
        #     self.change_x = BOSS_MOVEMENT_SPEED
        # if self.center_x == 0:
        #     self.center_x += BOSS_MOVEMENT_SPEED
        # elif self.center_x == WINDOW_WIDTH:
        #     self.center_x -= BOSS_MOVEMENT_SPEED
