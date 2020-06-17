

class Level:

    def __init__(
            self,
            number,
            num_max_enemies,
            num_max_bosses,
    ):
        self.number = number
        self.num_max_enemies = num_max_enemies
        self.num_max_bosses = num_max_bosses
        self.is_complete = False
        self.enemies_spawning = False
        self.boss_spawning = False
        self.num_spawned_enemies = 0
        self.num_curr_bosses = 0
        self.num_curr_enemies = 0

