import pygame
win_width = 480
win_height = 480


class Sprite:
    def __init__(self, filename):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.tile_width = self.rect.width
        self.tile_height = self.rect.height

    def draw(self, surface, x, y):
        surface.blit(self.image, (x, y))


class SpriteSheet:
    def __init__(self, filename, columns=0):
        self.sheet = pygame.image.load(filename)
        self.columns = columns

        self.rect = self.sheet.get_rect()
        self.tile_width = self.rect.width/self.columns
        self.tile_height = self.rect.height
        self.tile_list = []

        for move in range(self.columns):
            self.tile_list.append((move * self.tile_width, 0, self.tile_width, self.tile_height))

    def draw(self, surface, x, y, current_frame, offset=(0, 0)):
        surface.blit(self.sheet, (x-offset[0], y-offset[1]), self.tile_list[current_frame])


class Grid(object):
    def __init__(self, cell_width, cell_height):
        self.width = win_width
        self.height = win_height
        self.cell_width = cell_width
        self.cell_height = cell_height

        if self.width % self.cell_width == 0 and self.height % self.cell_height == 0:
            self.columns = int(self.width / self.cell_width)
            self.rows = int(self.height / self.cell_height)
        else:
            print("Cannot divide by selected cell_width or cell_height\nCouldn't create grid")
            exit(1)

        self.cell_count = self.rows * self.columns
        self.cell_surface = pygame.Surface((self.cell_width, self.cell_height))
        self.cell_list = []

    def build_grid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.cell_list.append(Cell(j * self.cell_width, i * self.cell_height, self))

    def draw_grid(self, sprite):
        for i in range(self.cell_count):
            sprite.draw(sprite.surface, self.cell_list[i].x, self.cell_list[i].y)


class Cell(object):
    def __init__(self, x, y, grid):
        self.width = grid.cell_width
        self.height = grid.cell_height
        self.x = x
        self.y = y


class PlayerCharacter(object):
    def __init__(self, x, y, grid, speed):
        w = self.width = grid.cell_width
        h = self.height = grid.cell_height
        hw = int(w/2)
        hh = int(h/2)
        self.speed = speed
        if 0 < x - hw < win_width:
            self.x = x - hw
        else:
            self.x = -hw
        if 0 < y - hh < win_height:
            self.y = y - hh
        else:
            self.y = -hh

        self.rect = (self.x, self.y, grid.width, grid.height)

        self.moving = [False, False, False, False]
        self.colliding = False

    def move_left(self):
        if self.x - self.speed > 0:
            self.x -= self.speed
            self.colliding = False
        else:
            self.colliding = True

    def move_right(self):
        if self.x + self.width + self.speed < win_width:
            self.x += self.speed
            self.colliding = False
        else:
            self.colliding = True

    def move_up(self):
        if self.y - self.speed > 0:
            self.y -= self.speed
            self.colliding = False
        else:
            self.colliding = True

    def move_down(self):
        if self.y + self.height + self.speed < win_height:
            self.y += self.speed
            self.colliding = False
        else:
            self.colliding = True

    def is_moving(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not self.colliding:
            self.moving = [True, False, False, False]
            return True
        elif keys[pygame.K_RIGHT] and not self.colliding:
            self.moving = [False, True, False, False]
            return True
        elif keys[pygame.K_UP] and not self.colliding:
            self.moving = [False, False, True, False]
            return True
        elif keys[pygame.K_DOWN] and not self.colliding:
            self.moving = [False, False, False, True]
            return True
        else:
            self.moving = [False, False, False, False]
            return False