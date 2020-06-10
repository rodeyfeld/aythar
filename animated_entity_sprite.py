import arcade


class AnimatedEntitySprite(arcade.Sprite):

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
        # Update to the next frame of the animation. Reset if at end of animation
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
            self.current_texture += 1
        else:
            self.current_texture = 0
