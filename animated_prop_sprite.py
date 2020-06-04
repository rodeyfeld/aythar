import arcade


class AnimatedPropSprite(arcade.Sprite):

    def __init__(self, texture_list, center_x, center_y):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list
        self.center_x = center_x
        self.center_y = center_y

    def __str__(self):
        return "({0}, {1}) - {2}".format(self.center_x, self.center_y, self.textures)

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()