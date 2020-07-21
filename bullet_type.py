class BulletType:
    def __init__(self, texture_list, damage=1):
        self.texture_list = texture_list
        self.damage = damage

    def __str__(self):
        return "BulletType: {0}".format(self.texture_list)

