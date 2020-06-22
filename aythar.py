import arcade
import math
from random import randint

from animated_entity_sprite import AnimatedEntitySprite
from animated_prop_sprite import AnimatedPropSprite
from boss_character import BossCharacter
from bullet_sprite import BulletSprite
from bullet_type import BulletType
from entity_sprite import EntitySprite
from level import Level
from player_character import PlayerCharacter
from prop_sprite import PropSprite
from config import *


class Aythar(arcade.View):

    def __init__(self):
        super().__init__()
        self.player_character = None
        self.score = 0
        # All spritelists in game
        self.background_list: arcade.SpriteList = arcade.SpriteList()
        # SpriteList for player character
        self.player_character_list: arcade.SpriteList = arcade.SpriteList()
        self.player_bullet_list: arcade.SpriteList = arcade.SpriteList()
        # SpriteList for enemies
        self.enemy_character_list: arcade.SpriteList = arcade.SpriteList()
        self.enemy_boss_character_list: arcade.SpriteList = arcade.SpriteList()
        # SpriteList for explosions
        # TODO: Move to individual enemy/player classes
        self.explosion_list: arcade.SpriteList = arcade.SpriteList()
        # Textures for the explosions assigned in setup
        self.explosion_texture_list = []
        # Textures for boss
        self.enemy_boss_character_texture_list = None
        self.enemy_boss_character_texture_list = None
        self.enemy_boss_bullet_types = []
        self.enemy_boss_bullet_list = arcade.SpriteList()
        # Total time elapsed in view
        self.time_elapsed: float = 0.0
        # Levels
        self.levels = []
        self.curr_level = None
        self.curr_level_num = 0

    def setup(self):
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
            asset = "./assets/explosion_" + str(i) + ".png"
            self.explosion_texture_list.append(
                self.create_texture_list(
                    asset=asset,
                    sprite_width=100,
                    sprite_height=100,
                    columns=10,
                    count=70
                )
            )
        # Texture list for boss
        self.enemy_boss_character_texture_list = self.create_texture_list(
            asset="./assets/big_boss.png",
            sprite_width=512,
            sprite_height=512,
            columns=2,
            count=2
        )
        # Texture list for boss bullets
        self.enemy_boss_bullet_types.append(self.create_texture_list(
            asset="./assets/star_bullet.png",
            sprite_width=64,
            sprite_height=64,
            columns=64,
            count=64
        ))

        # Setup levels
        self.curr_level = Level(number=1, num_max_enemies=10, num_max_bosses=1)
        self.levels.append(self.curr_level)

    def schedule_enemies(self):
        # Every ENEMY_SPAWN_TIMER seconds, call the create_enemy function
        arcade.schedule(self.create_enemy, ENEMY_SPAWN_TIMER)

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()
        self.player_character_list.draw()
        self.player_bullet_list.draw()
        self.enemy_character_list.draw()
        self.enemy_boss_character_list.draw()
        self.enemy_boss_bullet_list.draw()
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

        # Level is not complete, continue with enemy logic
        curr_level = self.levels[self.curr_level_num]
        if curr_level.is_complete is False:
            if curr_level.enemies_spawning is False and curr_level.num_spawned_enemies < curr_level.num_max_enemies:
                arcade.schedule(self.create_enemy, 1)
                curr_level.enemies_spawning = True
            elif curr_level.enemies_spawning and curr_level.num_spawned_enemies >= curr_level.num_max_enemies:
                arcade.unschedule(self.create_enemy)
                curr_level.enemies_spawning = False
            elif curr_level.boss_spawning is False and curr_level.num_spawned_enemies == curr_level.num_max_enemies:
                self.create_boss()
                curr_level.boss_spawning = True
        # Level is complete, move to next level if available
        elif self.curr_level_num <= len(self.levels):
            self.curr_level_num += 1
        # No more levels
        else:
            pass

        if math.floor(self.time_elapsed) == 0 and len(self.player_character_list) < 1:
            self.create_player()

        # arcade.unschedule(self.create_enemy)

        # Update basic enemies
        self.enemy_character_list.update()
        # Update enemy bosses
        self.enemy_boss_character_list.update()
        self.enemy_boss_bullet_list.update()
        # Update explosions
        self.explosion_list.update()
        # Update player
        self.player_character_list.update()
        self.player_bullet_list.update()
        for enemy_boss in self.enemy_boss_character_list:
            collisions = enemy_boss.collides_with_list(self.player_character.bullet_list)
            if collisions:
                for collision in collisions:
                    self.create_explosion(collision.center_x, collision.center_y)
                    collision.remove_from_sprite_lists()
                    enemy_boss.health -= 1

        for enemy in self.enemy_character_list:
            collisions = enemy.collides_with_list(self.player_bullet_list)
            if collisions:
                self.create_explosion(enemy.center_x, enemy.center_y)
                self.score += 1
                for collision in collisions:
                    collision.remove_from_sprite_lists()
                enemy.remove_from_sprite_lists()


            # TODO send player to game over screen when hit by enemy
            # if enemy.collides_with_list(self.player_character_list):

    def create_player(self):
        # Initialize player character at the bottom middle of the window
        # Texture
        player_texture_list = self.create_texture_list(
            asset="./assets/player_starship.png",
            sprite_width=32,
            sprite_height=16,
            columns=2,
            count=2
        )
        player_bullet_types = [BulletType(self.create_texture_list(
            asset="./assets/laser_bullet.png",
            sprite_width=128,
            sprite_height=128,
            columns=1,
            count=9
        ))]

        self.player_character = PlayerCharacter(
            texture_list=player_texture_list,
            center_x=WINDOW_WIDTH // 2,
            center_y=25,
            bullet_types=player_bullet_types
        )
        # self.player_character.setup()
        self.player_bullet_list = self.player_character.bullet_list
        self.player_character_list.append(self.player_character)

    def create_enemy(self, delta_time: float):
        # delta_time param required by arcade library
        # Add an enemy starting at the top of the window and at a random position on the x axis
        enemy_center_x = randint(0 + ENEMY_SPAWN_OFFSET, WINDOW_WIDTH - ENEMY_SPAWN_OFFSET)
        enemy_center_y = WINDOW_LENGTH
        enemy_character = EntitySprite("./assets/enemy_ship.png", SCALING, enemy_center_x, enemy_center_y)
        enemy_character.change_y = -ENEMY_MOVEMENT_SPEED
        self.enemy_character_list.append(enemy_character)
        self.curr_level.num_spawned_enemies += 1

    def create_boss(self):
        enemy_center_x = WINDOW_WIDTH // 2
        enemy_center_y = WINDOW_LENGTH
        boss_bullet_types = [
            BulletType(self.create_texture_list(
                asset="./assets/star_bullet.png",
                sprite_width=64,
                sprite_height=64,
                columns=64,
                count=64
            )),
            BulletType(self.create_texture_list(
                asset="./assets/plasma_bullet.png",
                sprite_width=64,
                sprite_height=64,
                columns=4,
                count=4
            )),
        ]
        boss_character = BossCharacter(
            texture_list=self.enemy_boss_character_texture_list,
            center_x=enemy_center_x,
            center_y=enemy_center_y,
            bullet_types=boss_bullet_types,
        )
        boss_character.change_y = -BOSS_MOVEMENT_SPEED
        boss_character.setup()
        self.enemy_boss_bullet_list = boss_character.bullet_list
        self.enemy_boss_character_list.append(boss_character)

    def create_explosion(self, center_x, center_y):
        # Choose random explosion from explosions list
        explosion_type = self.explosion_texture_list[randint(0, len(self.explosion_texture_list) - 1)]
        explosion = AnimatedPropSprite(explosion_type, center_x, center_y)
        explosion.update()
        self.explosion_list.append(explosion)

    @staticmethod
    def create_texture_list(asset, columns, count, sprite_width, sprite_height):
        texture_list = arcade.load_spritesheet(
            file_name=asset,
            sprite_width=sprite_width,  # Sprite width of each frame
            sprite_height=sprite_height,  # Sprite height of each frame
            columns=columns,  # Number of columns in spritesheet
            count=count  # Total number of frames in spritesheet
        )
        return texture_list

    def on_key_release(self, key, modifiers):
        # TODO: Improve player movement mechanics
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_character.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_character.change_x = 0

    def on_key_press(self, key, modifiers):
        # TODO: Fix propulsion sprite leaving player character on left/right movement before pressing up
        # Keys for controlling player movement
        if key == arcade.key.UP:
            self.player_character.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_character.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_character.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_character.change_x = PLAYER_MOVEMENT_SPEED
        # Keys for controlling player firing
        elif key == arcade.key.W:
            self.player_character_list[0].create_bullet(change_x=0, change_y=PLAYER_BULLET_SPEED)
        # TODO: Enable cardinal shots after character overhauls
        # elif key == arcade.key.A:
        #     self.create_bullet(
        #         origin_character=self.player_character,
        #         asset="./assets/pixel_laser_green_horizontal.png",
        #         change_x=-1,
        #         change_y=0,
        #         bullet_speed=PLAYER_BULLET_SPEED,
        #     )
        # elif key == arcade.key.S:
        #     self.create_bullet(
        #         origin_character=self.player_character,
        #         change_x=0,
        #         change_y=-1,
        #         bullet_speed=PLAYER_BULLET_SPEED,
        #         asset="./assets/pixel_laser_green_vertical.png"
        #     )
        # elif key == arcade.key.D:
        #     self.create_bullet(
        #         origin_character=self.player_character,
        #         change_x=1,
        #         change_y=0,
        #         bullet_speed=PLAYER_BULLET_SPEED,
        #         asset="./assets/pixel_laser_green_horizontal.png"
        #     )
