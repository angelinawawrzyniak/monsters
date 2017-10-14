from random import random, randint


class GameOverError(Exception):
    pass


class Board:

    def __init__(self):
        self._fields = [
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
        ]

    def draw(self, graphic_buffer,):
        for index_y in range(len(self._fields)):
            for index_x in range(len(self._fields[index_y])):
                if self._fields[index_y][index_x] == 'o':
                    graphic_buffer[index_y][index_x] = ' '
                else:
                    graphic_buffer[index_y][index_x] = 'x'

    def find_occupied_field(self):
        for x in range(len(self._fields)):
            if self._fields[x] == 'o':
                pass

    def is_field_occupied(self, y, index_x):
        return self._fields[y][index_x] == 'x'


class Monster:

    def __init__(self, y, x, step):
        self.x = x
        self.y = y
        self._step = step

    def draw(self, graphic_buffer):
        graphic_buffer[self.y][self.x] = 'M'

    def make_step(self, board, user):
        self._set_new_direction()
        if board.is_field_occupied(self.y, self.x + self._step):
            self._step *= -1
        self.x = self.x + self._step
        if (self.y, self.x) == (user.y, user.x):
            user.take_life()

    def _set_new_direction(self):
        random_float = random()
        if random_float <= 0.1:
            self._step *= -1


class User:

    def __init__(self, y, x, step, life, backpack):
        self.x = x
        self.y = y
        self.step = step
        self.life = life
        self.backpack = backpack

    def draw(self, graphic_buffer):
        graphic_buffer[self.y][self.x] = 'U'

    def take_life(self):
        self.life -= 1
        if self.life == 0:
            raise GameOverError('Monster ate Human')


class Portal:

    def __init__(self, board, user):
        self._set_up_portal(board, user)

    def draw(self,graphic_buffer):
        graphic_buffer[self.y][self.x] = 'P'

    def _set_up_portal(self,board, user):
        while True:
            x = randint(0, 11)
            y = randint(0, 6)
            if (y, x) == (user.y, user.x):
                continue
            if board.is_field_occupied(y, x):
                continue
            else:
                self.x = x
                self.y = y
                break


class Artifact:

    def __init__(self, board, portal):
        self._set_up_an_artifact(board, portal)

    def draw(self, graphic_buffer):
        graphic_buffer[self.y][self.x] = 'A'

    def _set_up_an_artifact(self, board, portal):
        while True:
            x = randint(0, 11)
            y = randint(0, 6)
            if (y, x) == (portal.y, portal.x):
                continue
            if board.is_field_occupied(y, x):
                continue
            else:
                self.x = x
                self.y = y
                break


def draw_scene(board, monsters, user, portal, artifacts, graphic_buffer):
    board.draw(graphic_buffer)
    for monster in monsters:
        monster.draw(graphic_buffer)
    user.draw(graphic_buffer)
    portal.draw(graphic_buffer)
    for artifact in artifacts:
        artifact.draw(graphic_buffer)
    for line in graphic_buffer:
        print('  '.join(line))
    print('items: {}, life: {}, level: {}'.format(len(user.backpack), user.life, game_level))


graphic_buffer = [
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', ''],
]
board = Board()
monsters = [Monster(2, 3, 1)]  # Monster(0, 1), Monster(10, -1)]
user = User(2, 5, 1, 3, [])
portal = Portal(board, user)
artifacts = [Artifact(board, portal), Artifact(board, portal),]
try:
    game_level = 1
    while True:
        draw_scene(board, monsters, user, portal, artifacts, graphic_buffer)
        if (portal.y, portal.x) != (user.y, user.x):
            chosen_direction = input('Choose direction: Up/Down/Left/Right: w/s/a/d')
        else:
            game_level += 1
            if game_level == 4:
                print('You have won')
                break
            monsters = [Monster(2, 3, 1)]  # Monster(0, 1), Monster(10, -1)]
            user = User(2, 5, 1, user.life, user.backpack)
            portal = Portal(board, user)
            artifacts = [Artifact(board, portal), Artifact(board, portal), ]
        # TODO: refactor code
        if chosen_direction == 'a':
            if board.is_field_occupied(user.y, user.x - user.step):
                print('You can\'t go there')
            else:
                user.x -= user.step
        elif chosen_direction == 'd':
            if board.is_field_occupied(user.y, user.x + user.step):
                print('You can\'t go there')
            else:
                user.x += user.step
        elif chosen_direction == 'w':
            if board.is_field_occupied(user.y - user.step, user.x):
                print('You can\'t go there')
            else:
                user.y -= user.step
        elif chosen_direction == 's':
            if board.is_field_occupied(user.y + user.step, user.x):
                print('You can\'t go there')
            else:
                user.y += user.step
        for artifact in artifacts:
            if (user.y, user.x) == (artifact.y, artifact.x):
                user.backpack.append(artifact)
                artifacts.remove(artifact)
        for monster in monsters:
            if (user.y, user.x) == (monster.y, monster.x):
                user.take_life()

        for monster in monsters:
            monster.make_step(board, user)
except GameOverError as error:
    draw_scene(board, monsters, user, portal, artifacts, graphic_buffer)
    print('GAME OVER')
    print(error)

