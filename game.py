from time import sleep

import arcade

from main_menu import MainMenu

WINDOW_LENGTH = 600
WINDOW_WIDTH = 800
SCALING = 1


class Game(arcade.Window):

    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_LENGTH, "Aythar")
        self.main_menu_view = None
        self.aythar_view = None

    def setup(self):
        # When game starts, setup and display main menu
        self.main_menu_view = MainMenu(WINDOW_WIDTH, WINDOW_LENGTH, SCALING)
        self.main_menu_view.setup()
        self.show_view(self.main_menu_view)



