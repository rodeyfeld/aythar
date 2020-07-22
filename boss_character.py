import arcade
import animated_entity_sprite
import bullet_sprite
from config import *


class BossCharacter(animated_entity_sprite.AnimatedEntitySprite):

    def __init__(self, texture_list, center_x, center_y, bullet_types, health=10):
        super().__init__(texture_list=texture_list, center_x=center_x, center_y=center_y)
        self.scale = SCALING
        self.bullet_types = bullet_types
        self.primary_bullet_types = None
        self.secondary_bullet_types = None
        self.bullet_list = arcade.SpriteList()
        self.health = health
        print("Boss", self.textures)

    def update(self):
        super().update()
        self.center_y += self.change_y
        if self.center_y < WINDOW_LENGTH - WINDOW_LENGTH // 4:
            self.change_y = 0
        for bullet in self.bullet_list:
            if (bullet.center_x > WINDOW_WIDTH or bullet.center_x < 0 or
                    bullet.center_y > WINDOW_LENGTH or bullet.center_y < 0):
                bullet.remove_from_sprite_lists()

    def setup(self):
        self.primary_bullet_types = [self.bullet_types[0]]
        self.secondary_bullet_types = self.bullet_types[1:]
        self.attack()

    def create_bullet(self, bullet_type, change_x, change_y):
        bullet = bullet_sprite.BulletSprite(
            bullet_type=bullet_type,
            center_x=self.center_x,
            center_y=self.bottom,
            change_x=change_x,
            change_y=change_y
        )
        # bullet.scale = .25
        self.bullet_list.append(bullet)

    def split_attack(self, delta_time):
        num_attacks = 10
        for i in range(1, num_attacks):
            from random import randint
            bullet_type = self.secondary_bullet_types[randint(0, len(self.secondary_bullet_types) - 1)]
            # bullet_trajectory = (WINDOW_WIDTH // 2) + (i * bullet_distance)
            bullet_trajectory = i
            self.create_bullet(bullet_type=bullet_type, change_x=bullet_trajectory, change_y=BOSS_BULLET_SPEED)
            self.create_bullet(bullet_type=bullet_type, change_x=-bullet_trajectory, change_y=BOSS_BULLET_SPEED)

    def forward_attack(self, delta_time):
        bullet_type = self.primary_bullet_types[0]
        self.create_bullet(bullet_type=bullet_type, change_x=0, change_y=BOSS_BULLET_SPEED+1)

    def attack(self):
        # delta_time param required by arcade library
        split_attack_rate = 3
        forward_attack_rate = 1.5
        arcade.schedule(self.split_attack, split_attack_rate)
        arcade.schedule(self.forward_attack, forward_attack_rate)

    def ceasefire(self):
        arcade.unschedule(self.split_attack)
        arcade.unschedule(self.forward_attack)
