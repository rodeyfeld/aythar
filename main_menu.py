import arcade

from aythar import Aythar
from menu_button import MenuButton


class MainMenu(arcade.View):

    def __init__(self, window_width, window_length, scaling):
        super().__init__()
        self.window_width = window_width
        self.window_length = window_length
        self.scaling = scaling
        self.start_button_list = arcade.SpriteList()
        self.aythar_view = None

    def setup(self):
        self.create_buttons()
        self.aythar_view = Aythar(window_width=self.window_width, window_length=self.window_length, scaling=self.scaling)
        self.aythar_view.setup()

    def on_draw(self):
        arcade.start_render()
        self.start_button_list.draw()

    def create_buttons(self):
        # Create "Start" button
        self.start_button_list.append(MenuButton(asset="./assets/start_button.png",
                                                 scaling=self.scaling,
                                                 x=self.window_width // 2,
                                                 y=self.window_length // 2,
                                                 ))

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # If button pressed, move to game view
        if self.is_button_pressed(_x, _y):
            self.window.show_view(self.aythar_view)

    def is_button_pressed(self, x, y):
        # Check if x, y coordinates of mouse click collides with button
        start_button: MenuButton = self.start_button_list[0]
        # Account for offsets caused by checking from center of button
        start_width_center_offset = start_button.width // 2
        start_height_center_offset = start_button.height // 2
        print(x, y)
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
