import arcade

from aythar import Aythar
from menu_button import MenuButton
from config import WINDOW_WIDTH, WINDOW_LENGTH, SCALING


class MainMenu(arcade.View):

    def __init__(self):
        super().__init__()
        self.start_button_list = arcade.SpriteList()
        self.aythar_view = None

    def setup(self):
        self.create_buttons()
        self.aythar_view = Aythar()
        self.aythar_view.setup()

    def on_draw(self):
        arcade.start_render()
        self.start_button_list.draw()

    def create_buttons(self):
        # Create "Start" button
        self.start_button_list.append(MenuButton(asset="./assets/start_button.png",
                                                 scaling=SCALING,
                                                 x=WINDOW_WIDTH // 2,
                                                 y=WINDOW_LENGTH // 2,
                                                 ))

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # If button pressed, move to game view
        if self.is_button_pressed(_x, _y):
            self.window.show_view(self.aythar_view)
            self.aythar_view.schedule_enemies()

    def is_button_pressed(self, x, y):
        # Check if x, y coordinates of mouse click collides with button
        start_button: MenuButton = self.start_button_list[0]
        # Account for offsets caused by checking from center of button
        start_width_center_offset = start_button.width // 2
        start_height_center_offset = start_button.height // 2
        if (
                start_button.center_x + start_width_center_offset
                > x >
                start_button.center_x - start_width_center_offset
                and
                start_button.center_y + start_height_center_offset
                > y >
                start_button.center_y - start_height_center_offset
        ):
            return True
        return False
