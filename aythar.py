import arcade

from entity_sprite import EntitySprite

PLAYER_MOVEMENT_SPEED = 10


class Aythar(arcade.View):

    def __init__(self, window_width: int, window_length: int, scaling: int):
        super().__init__()
        self.window_width: int = window_width
        self.window_length: int = window_length
        self.scaling: int = scaling
        self.player_character = None
        self.player_character_list: arcade.SpriteList = arcade.SpriteList()
        self.enemy_character_list: arcade.SpriteList = arcade.SpriteList()

    def setup(self):
        self.create_player()

    def create_player(self):
        self.player_character = EntitySprite("./assets/player_character.png", self.scaling, 50, 50)
        self.player_character_list.append(self.player_character)

    def on_draw(self):
        arcade.start_render()
        self.player_character_list.draw()
        self.enemy_character_list.draw()

    def on_update(self, delta_time: float):
        self.player_character_list.update()
        self.enemy_character_list.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_character.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_character.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_character.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_character.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_character.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_character.change_x = 0
