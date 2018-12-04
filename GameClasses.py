import pygame
win_width = 520
win_height = 520


class Sprite:
    def __init__(self, filename):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.tile_width = self.rect.width
        self.tile_height = self.rect.height

    def draw(self, surface, x, y):
        surface.blit(self.image, (x, y))


class SpriteSheet:
    def __init__(self, filename, columns=0, interpolation=0):
        self.sheet = pygame.image.load(filename)
        self.columns = columns

        self.rect = self.sheet.get_rect()
        self.tile_width = self.rect.width/self.columns
        self.tile_height = self.rect.height
        self.hw = int(self.tile_width/2)
        self.hh = int(self.tile_height/2)

        self.tile_list = []
        for move in range(self.columns):
            self.tile_list.append((move * self.tile_width, 0, self.tile_width, self.tile_height))

        # This index controls the current frame of the animation
        self.index = 0

        self.frame_interpolation = self.frame_interpolation_init = interpolation

    def draw(self, surface, x, y, current_frame, offset=(0, 0)):
        surface.blit(self.sheet, (x + offset[0], y + offset[1]), self.tile_list[current_frame])

    def update_animation_frames(self, start_frame, end_frame):

        if self.index + start_frame == end_frame:
            self.index = 0

        if self.frame_interpolation == 0:
            self.index += 1
            self.frame_interpolation = self.frame_interpolation_init
        else:
            self.frame_interpolation -= 1


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

    def build_grid(self, map_layout):
        index = 0
        for i in range(self.cell_count):
            for j in range(self.columns):
                cell = Cell(j * self.cell_width, i * self.cell_height, self, index)
                self.cell_list.append(cell)
                index += 1
        for j in range(len(map_layout)):
            if map_layout[j] == 1:
                self.cell_list[j].cell_type = 1
                self.cell_list[j].collides = True
            elif map_layout[j] == 2:
                self.cell_list[j].cell_type = 2
                self.cell_list[j].collides = True
            elif map_layout[j] == 3:
                self.cell_list[j].cell_type = 3
                self.cell_list[j].collides = True

    def draw_grid(self, sprite, surface):
        for i in range(self.cell_count):
            sprite.draw(surface, self.cell_list[i].x, self.cell_list[i].y)

    def get_colliding_cells(self):
        cells = []
        for i in range(self.cell_count):
            if self.cell_list[i].collides:
                cells.append(self.cell_list[i])
        return cells


class Cell(object):
    def __init__(self, x, y, grid, index):
        self.x = x
        self.y = y
        self.width = grid.cell_width
        self.height = grid.cell_height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.index = index
        self.cell_type = 0
        self.collides = False

    def draw(self, sprite, surface):
        sprite.draw(surface, self.x, self.y)


class Bomb(object):
    def __init__(self, cell, start, pre_spritesheet, explosion_spritesheet):
        self.cell = cell
        self.x = cell.x
        self.y = cell.y
        self.width = cell.width
        self.height = cell.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.pre_explosion = SpriteSheet(pre_spritesheet[0], pre_spritesheet[1], pre_spritesheet[2])
        self.explosion = SpriteSheet(explosion_spritesheet[0], explosion_spritesheet[1], explosion_spritesheet[2])
        self.timer = start + 3000
        self.radius = 3
        self.exploded = False

    def draw(self, spritesheet, surface, start, end):
        spritesheet.draw(surface, self.x, self.y, spritesheet.index)
        spritesheet.update_animation_frames(start, end)

    def explode(self, grid, players):
        self.expand_explosion("grid.cell_list[self.cell.index - i]", grid, players)
        self.expand_explosion("grid.cell_list[self.cell.index + i]", grid, players)
        self.expand_explosion("grid.cell_list[self.cell.index - grid.columns * i]", grid, players)
        self.expand_explosion("grid.cell_list[self.cell.index + grid.columns * i]", grid, players)

    def expand_explosion(self, cell_index, grid, players):
        for i in range(1, self.radius):
            cell = eval(cell_index)
            if cell.cell_type == 3:
                cell.cell_type = 0
                cell.collides = False
            elif cell.cell_type == 0:
                for j in range(len(players)):
                    if cell.rect.colliderect(players[j].rect):
                        players[j].lives -= 1
            else:
                break