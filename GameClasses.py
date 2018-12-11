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

        # This will keep track the number of times an animation has been displayed
        self.count = 0

        self.frame_interpolation = self.frame_interpolation_init = interpolation

    def draw(self, surface, x, y, current_frame, offset=(0, 0)):
        surface.blit(self.sheet, (x + offset[0], y + offset[1]), self.tile_list[current_frame])

    def update_animation_frames(self, start_frame, end_frame):

        if self.index + start_frame == end_frame:
            self.index = 0
            self.count += 1
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

    def build_grid(self, map_layout, spritesheets):
        index = 0
        coords = []
        for i in range(self.rows):
            for j in range(self.columns):
                coords.append([j * self.cell_width, i * self.cell_height])

        for k in range(len(map_layout)):
            if map_layout[k] == 0:
                self.cell_list.append(Ground(coords[k][0], coords[k][1], self, index, spritesheets))
            elif map_layout[k] == 1:
                self.cell_list.append(Wall(coords[k][0], coords[k][1], self, index, 0))
            elif map_layout[k] == 2:
                self.cell_list.append(Wall(coords[k][0], coords[k][1], self, index, 1))
            elif map_layout[k] == 3:
                self.cell_list.append(Wall(coords[k][0], coords[k][1], self, index, 2))
            index += 1

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

    def draw(self, sprite, surface):
        sprite.draw(surface, self.x, self.y)

    def draw_anim(self, spritesheet, surface, start, end):
        spritesheet.draw(surface, self.x, self.y, spritesheet.index)
        spritesheet.update_animation_frames(start, end)


class Wall(Cell):
    def __init__(self, x, y, grid, index, type):
        super().__init__(x, y, grid, index)
        self.collides = True
        self.type = type


class Ground(Cell):
    def __init__(self, x, y, grid, index, spritesheets):
        super().__init__(x, y, grid, index)
        self.collides = False
        self.destroyed = False
        self.flames_left_end = SpriteSheet(spritesheets[2][0], spritesheets[2][1], spritesheets[2][2])
        self.flames_right_end = SpriteSheet(spritesheets[3][0], spritesheets[3][1], spritesheets[3][2])
        self.flames_top_end = SpriteSheet(spritesheets[4][0], spritesheets[4][1], spritesheets[4][2])
        self.flames_bottom_end = SpriteSheet(spritesheets[5][0], spritesheets[5][1], spritesheets[5][2])
        self.flames_middle_horizontal = SpriteSheet(spritesheets[6][0], spritesheets[6][1], spritesheets[6][2])
        self.flames_middle_vertical = SpriteSheet(spritesheets[7][0], spritesheets[7][1], spritesheets[7][2])
        self.destroyed_spritesheet = SpriteSheet(spritesheets[8][0], spritesheets[8][1], spritesheets[8][2])
        self.flame_type = ""


class Bomb(object):
    def __init__(self, cell, start, spritesheets):
        self.cell = cell
        self.spritesheets = spritesheets
        self.x = cell.x
        self.y = cell.y
        self.width = cell.width
        self.height = cell.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.pre_explosion = SpriteSheet(spritesheets[0][0], spritesheets[0][1], spritesheets[0][2])
        self.explosion = SpriteSheet(spritesheets[1][0], spritesheets[1][1], spritesheets[1][2])

        self.timer = start + 3000
        self.radius = 4
        self.exploded = False

    def draw_anim(self, spritesheet, surface, start, end):
        spritesheet.draw(surface, self.x, self.y, spritesheet.index)
        spritesheet.update_animation_frames(start, end)

    def explode(self, grid, players, spritesheets):
        # Bomb cell
        grid.cell_list[self.cell.index] = Ground(self.x, self.y, grid, self.cell.index, self.spritesheets)
        damage_players(self.cell, players)

        # Nearby cells
        destroyed_block = [False, False, False, False]
        for i in range(1, self.radius):
            directions = [self.cell.index - i,
                          self.cell.index + i,
                          self.cell.index - grid.columns * i,
                          self.cell.index + grid.columns * i]
            check = [self.cell.index - (i - 1),
                     self.cell.index + (i - 1),
                     self.cell.index - grid.columns * (i - 1),
                     self.cell.index + grid.columns * (i - 1)]

            for j in range(len(directions)):
                if directions[j] <= grid.cell_count:
                    if type(grid.cell_list[directions[j]]) == Wall and grid.cell_list[directions[j]].type == 2:
                        if not grid.cell_list[check[j]].collides and not destroyed_block[j]:
                            grid.cell_list[directions[j]] = Ground(grid.cell_list[directions[j]].x, grid.cell_list[directions[j]].y, grid, directions[j], spritesheets)
                            grid.cell_list[directions[j]].destroyed = True
                            damage_players(grid.cell_list[directions[j]], players)
                            destroyed_block[j] = True
                    elif type(grid.cell_list[directions[j]]) == Ground:
                        if not grid.cell_list[check[j]].collides and not destroyed_block[j]:
                            if j == 0:
                                if i == self.radius-1:
                                    grid.cell_list[directions[j]].flame_type = "left_end"
                                else:
                                    grid.cell_list[directions[j]].flame_type = "mid_horizontal"
                            elif j == 1:
                                if i == self.radius - 1:
                                    grid.cell_list[directions[j]].flame_type = "right_end"
                                else:
                                    grid.cell_list[directions[j]].flame_type = "mid_horizontal"
                            elif j == 2:
                                if i == self.radius - 1:
                                    grid.cell_list[directions[j]].flame_type = "top_end"
                                else:
                                    grid.cell_list[directions[j]].flame_type = "mid_vertical"
                            elif j == 3:
                                if i == self.radius - 1:
                                    grid.cell_list[directions[j]].flame_type = "bottom_end"
                                else:
                                    grid.cell_list[directions[j]].flame_type = "mid_vertical"
                            damage_players(grid.cell_list[directions[j]], players)


def damage_players(cell, players):
    for i in range(len(players)):
        if cell.rect.colliderect(players[i].rect):
            players[i].lives -= 1