import arcade
from game import Game

# Ship and laser assets provided by Hex:
# https://hexadecimalwtf.itch.io/space-pixels
# Explosions by Will Tice:
# https://untiedgames.itch.io/five-free-pixel-explosions
# Plasma ball by Geni and Thane Brimhall
# http://commons.wikimedia.org/wiki/File:Plasmaball_vid2.ogg


def main():
    game = Game()
    game.setup()
    arcade.run()


main()
