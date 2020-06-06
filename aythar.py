import arcade
import math
from random import randint

from animated_entity_sprite import AnimatedEntitySprite
from animated_prop_sprite import AnimatedPropSprite
from boss_character import BossCharacter
from entity_sprite import EntitySprite
from prop_sprite import PropSprite
from config import *


class Aythar(arcade.View):

    def __init__(self):
        super().__init__()
        self.player_character = None
        self.score = 0
        # All spritelists in game
        self.background_list: arcade.SpriteList = arcade.SpriteList()
        self.player_character_list: arcade.SpriteList = arcade.SpriteList()
        self.enemy_character_list: arcade.SpriteList = arcade.SpriteList()
        self.enemy_boss_character_list: arcade.SpriteList = arcade.SpriteList()
        self.bullet_list: arcade.SpriteList = arcade.SpriteList()
        self.explosion_list: arcade.SpriteList = arcade.SpriteList()
        # Textures for the explosions assigned in setup
        self.explosion_texture_list = []
        self.enemy_boss_character_texture_list = []
        self.time_elapsed: float = 0.0

    def setup(self):
        self.create_player()
        # Create vertically scrolling background image
        self.background_list.append(PropSprite(
            asset="./assets/space_background.png",
            scaling=SCALING * 10,
            x=WINDOW_WIDTH // 2,
            y=BACKGROUND_HEIGHT // 2,
            change_y=-BACKGROUND_SCROLL_SPEED
        ))
        self.background_list.append(PropSprite(
            asset="./assets/space_background.png",
            scaling=SCALING * 10,
            x=WINDOW_WIDTH // 2,
            y=BACKGROUND_HEIGHT + WINDOW_LENGTH // 2,
            change_y=-BACKGROUND_SCROLL_SPEED
        ))
        # Currently 3 explosion types available
        for i in range(0, 3):
            # Number of columns in spritesheet
            columns = 10
            # Total number of individual frames in spritesheet
            count = 70
            # Length and width of each sprite frame
            sprite_width = 100
            sprite_height = 100
            # Load the explosions from sprite sheet
            asset = "./assets/explosion_" + str(i) + ".png"
            self.explosion_texture_list.append(arcade.load_spritesheet(
                asset,
                sprite_width,
                sprite_height,
                columns,
                count
            ))
        # Setup textures for boss
        columns = 2
        # Total number of individual frames in spritesheet
        count = 2
        # Length and width of each sprite frame
        sprite_width = 32
        sprite_height = 32
        self.enemy_boss_character_texture_list = arcade.load_spritesheet(
            "./assets/enemy_boss.png",
            # "./assets/enemy_boss.png",
            sprite_width,
            sprite_height,
            columns,
            count
        )

    def schedule_enemies(self):
        # Every ENEMY_SPAWN_TIMER seconds, call the create_enemy function
        arcade.schedule(self.create_enemy, ENEMY_SPAWN_TIMER)

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()
        self.player_character_list.draw()
        self.player_character.prop_sprite_list.draw()
        self.enemy_character_list.draw()
        self.enemy_boss_character_list.draw()
        self.bullet_list.draw()
        self.explosion_list.draw()
        score_str = "Score: {0}".format(self.score)
        # Display score
        arcade.draw_text(score_str, SCORE_POS_X, SCORE_POS_Y, arcade.color.WHITE, SCORE_FONT_SIZE)

    def on_update(self, delta_time: float):
        self.time_elapsed += delta_time

        # Loop background
        background_one = self.background_list[0]
        background_two = self.background_list[1]
        if background_one.bottom == -BACKGROUND_HEIGHT:
            background_one.center_y = WINDOW_LENGTH + BACKGROUND_HEIGHT // 2
        if background_two.bottom == -BACKGROUND_HEIGHT:
            background_two.center_y = WINDOW_LENGTH + BACKGROUND_HEIGHT // 2
        self.background_list.update()
        if math.floor(self.time_elapsed) == 1 and len(self.enemy_boss_character_list) < 1:
            self.create_boss()
            arcade.unschedule(self.create_enemy)

        # for boss in self.enemy_boss_character_list:
        #     boss.update()
        self.enemy_character_list.update()
        self.enemy_boss_character_list.update()
        self.bullet_list.update()
        self.explosion_list.update()
        self.player_character_list.update()
        self.player_character.prop_sprite_list.update()

        for enemy in self.enemy_character_list:
            collisions = enemy.collides_with_list(self.bullet_list)
            if collisions:
                self.create_explosion(enemy.center_x, enemy.center_y)
                self.score += 1
                for collision in collisions:
                    collision.remove_from_sprite_lists()
                    enemy.remove_from_sprite_lists()
            elif (enemy.center_x > WINDOW_WIDTH or enemy.center_x < 0 or
                  enemy.center_y > WINDOW_LENGTH or enemy.center_y < 0):
                enemy.remove_from_sprite_lists()

        for bullet in self.bullet_list:
            if (bullet.center_x > WINDOW_WIDTH or bullet.center_x < 0 or
                    bullet.center_y > WINDOW_LENGTH or bullet.center_y < 0):
                bullet.remove_from_sprite_lists()

            # TODO send player to game over screen when hit by enemy
            # if enemy.collides_with_list(self.player_character_list):

    def create_player(self):
        # Initialize player character at the bottom middle of the window
        self.player_character = EntitySprite("./assets/pixel_ship.png", SCALING, WINDOW_WIDTH // 2, 25)
        self.player_character_list.append(self.player_character)

    def create_enemy(self, delta_time: float):
        # delta_time param required by arcade library
        # Add an enemy starting at the top of the window and at a random position on the x axis
        enemy_center_x = randint(0 + ENEMY_SPAWN_OFFSET, WINDOW_WIDTH - ENEMY_SPAWN_OFFSET)
        enemy_center_y = WINDOW_LENGTH
        enemy_character = EntitySprite("./assets/enemy_ship.png", SCALING, enemy_center_x, enemy_center_y)
        enemy_character.change_y = -ENEMY_MOVEMENT_SPEED
        self.enemy_character_list.append(enemy_character)

    def create_boss(self):
        enemy_center_x = WINDOW_WIDTH // 2
        enemy_center_y = WINDOW_LENGTH
        enemy_character = BossCharacter(
            self.enemy_boss_character_texture_list,
            enemy_center_x,
            enemy_center_y,
        )
        enemy_character.change_y = -BOSS_MOVEMENT_SPEED
        self.enemy_boss_character_list.append(enemy_character)

    def create_explosion(self, center_x, center_y):
        # Choose random explosion from explosions list
        explosion_type = self.explosion_texture_list[randint(0, len(self.explosion_texture_list) - 1)]
        explosion = AnimatedPropSprite(explosion_type, center_x, center_y)
        explosion.update()
        self.explosion_list.append(explosion)

    def on_key_release(self, key, modifiers):
        # TODO: Improve player movement mechanics
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_character.change_y = 0
            self.player_character.clear_props()
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_character.change_x = 0
            self.player_character.adjust_props(
                change_x=self.player_character.change_x,
                change_y=self.player_character.change_y
            )

    def on_key_press(self, key, modifiers):
        # TODO: Split key presses into more concise definitions
        # TODO: Fix propulsion sprite leaving player character on left/right movement before pressing up
        # Keys for controlling player movement
        if key == arcade.key.UP:
            self.player_character.change_y = PLAYER_MOVEMENT_SPEED
            propulsion = PropSprite(
                asset="./assets/thruster_bottom.png",
                scaling=SCALING,
                x=self.player_character.center_x,
                y=self.player_character.bottom - PLAYER_PROP_DISTANCE
            )
            propulsion.change_y = PLAYER_MOVEMENT_SPEED
            self.player_character.prop_sprite_list.append(propulsion)
        elif key == arcade.key.DOWN:
            self.player_character.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_character.change_x = -PLAYER_MOVEMENT_SPEED
            self.player_character.adjust_props(
                change_x=self.player_character.change_x,
                change_y=self.player_character.change_y
            )
        elif key == arcade.key.RIGHT:
            self.player_character.change_x = PLAYER_MOVEMENT_SPEED
            self.player_character.adjust_props(
                change_x=self.player_character.change_x,
                change_y=self.player_character.change_y
            )
        # Keys for controlling player firing
        elif key == arcade.key.W:
            bullet = EntitySprite(
                "./assets/pixel_laser_green_vertical.png",
                SCALING,
                self.player_character.center_x,
                self.player_character.center_y
            )
            bullet.change_y = BULLET_SPEED
            self.bullet_list.append(bullet)
        elif key == arcade.key.A:
            bullet = EntitySprite(
                "./assets/pixel_laser_green_horizontal.png",
                SCALING,
                self.player_character.center_x,
                self.player_character.center_y
            )
            bullet.change_x = -BULLET_SPEED
            self.bullet_list.append(bullet)
        elif key == arcade.key.S:
            bullet = EntitySprite(
                "./assets/pixel_laser_green_vertical.png",
                SCALING,
                self.player_character.center_x,
                self.player_character.center_y
            )
            bullet.change_y = -BULLET_SPEED
            self.bullet_list.append(bullet)
        elif key == arcade.key.D:
            bullet = EntitySprite(
                "./assets/pixel_laser_green_horizontal.png",
                SCALING,
                self.player_character.center_x,
                self.player_character.center_y
            )
            bullet.change_x = BULLET_SPEED
            self.bullet_list.append(bullet)
