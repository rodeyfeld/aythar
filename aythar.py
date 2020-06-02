import arcade

from entity_sprite import EntitySprite

PLAYER_MOVEMENT_SPEED = 10
BULLET_SPEED = 10


class Aythar(arcade.View):

    def __init__(self, window_width: int, window_length: int, scaling: int):
        super().__init__()
        self.window_width: int = window_width
        self.window_length: int = window_length
        self.scaling: int = scaling
        self.player_character = None
        self.player_character_list: arcade.SpriteList = arcade.SpriteList()
        self.enemy_character_list: arcade.SpriteList = arcade.SpriteList()
        self.bullet_list: arcade.SpriteList = arcade.SpriteList()

    def setup(self):
        self.create_player()

    def on_draw(self):
        arcade.start_render()
        self.player_character_list.draw()
        self.enemy_character_list.draw()
        self.bullet_list.draw()

    def on_update(self, delta_time: float):
        self.player_character_list.update()
        self.enemy_character_list.update()
        self.bullet_list.update()
        for bullet in self.bullet_list:
            if (bullet.center_x > self.window_width or bullet.center_x < 0 or
            bullet.center_y > self.window_length or bullet.center_y < 0):
                bullet.remove_from_sprite_lists()

    def create_player(self):
        self.player_character = EntitySprite("./assets/pixel_ship.png", self.scaling, 50, 50)
        self.player_character_list.append(self.player_character)

    def create_bullet(self, direction):
        if direction == "up" or direction == "down":
            asset = "./assets/pixel_laser_green_vertical.png"
        else:
            asset = "./assets/pixel_laser_green_horizontal.png"
        self.bullet_list.append(EntitySprite(asset,
                                             self.scaling,
                                             self.player_character.center_x,
                                             self.player_character.center_y
                                             ))

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_character.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_character.change_x = 0

    def on_key_press(self, key, modifiers):
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
            bullet = EntitySprite(
                "./assets/pixel_laser_green_vertical.png",
                self.scaling,
                self.player_character.center_x,
                self.player_character.center_y
            )
            bullet.change_y = BULLET_SPEED
            self.bullet_list.append(bullet)
        elif key == arcade.key.A:
            bullet = EntitySprite(
                "./assets/pixel_laser_green_horizontal.png",
                self.scaling,
                self.player_character.center_x,
                self.player_character.center_y
            )
            bullet.change_x = -BULLET_SPEED
            self.bullet_list.append(bullet)
        elif key == arcade.key.S:
            bullet = EntitySprite(
                "./assets/pixel_laser_green_vertical.png",
                self.scaling,
                self.player_character.center_x,
                self.player_character.center_y
            )
            bullet.change_y = -BULLET_SPEED
            self.bullet_list.append(bullet)
        elif key == arcade.key.D:
            bullet = EntitySprite(
                "./assets/pixel_laser_green_horizontal.png",
                self.scaling,
                self.player_character.center_x,
                self.player_character.center_y
            )
            bullet.change_x = BULLET_SPEED
            self.bullet_list.append(bullet)
