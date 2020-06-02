import arcade
from game import Game

# Assets provided by Hex:
# https://hexadecimalwtf.itch.io/space-pixels


def main():
    game = Game()
    game.setup()
    arcade.run()


main()
