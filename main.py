import arcade
from game import Game

# Ship and laser assets provided by Hex:
# https://hexadecimalwtf.itch.io/space-pixels
# Explosions by Will Tice:
# https://untiedgames.itch.io/five-free-pixel-explosions

def main():
    game = Game()
    game.setup()
    arcade.run()


main()
