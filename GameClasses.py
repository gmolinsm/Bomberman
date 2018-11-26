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

        self.build_grid()

    def build_grid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.cell_list.append(Cell(j * self.cell_width, i * self.cell_height, self))

    def draw_grid(self, sprite, surface):
        for i in range(self.cell_count):
            sprite.draw(surface, self.cell_list[i].x, self.cell_list[i].y)

    def draw_cell(self, sprite, surface, index):
        sprite.draw(surface, self.cell_list[index].x, self.cell_list[index].y)


class Cell(object):
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.width = grid.cell_width
        self.height = grid.cell_height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class PlayerCharacter(object):
    def __init__(self, x, y, grid, speed, tag="Player", key_set=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]):
        w = self.width = grid.cell_width
        h = self.height = grid.cell_height
        hw = int(w/2)
        hh = int(h/2)
        self.speed = speed
        self.tag = tag

        if 0 < x - hw < win_width:
            self.x = x - hw
        else:
            self.x = -hw
        if 0 < y - hh < win_height:
            self.y = y - hh
        else:
            self.y = -hh

        self.rect = pygame.Rect(self.x, self.y, grid.width, grid.height)
        self.move = [False, False, False, False]
        self.last_move = 0
        self.colliding = False
        self.key_set = key_set

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

    def check_move(self, direction, players):
        collisions = self.get_collisions(players)
        if direction == "left" and not collisions[0]:
            self.move = [True, False, False, False]
            self.move_left()
        elif direction == "right" and not collisions[1]:
            self.move = [False, True, False, False]
            self.move_right()
        elif direction == "up" and not collisions[2]:
            self.move = [False, False, True, False]
            self.move_up()
        elif direction == "down" and not collisions[3]:
            self.move = [False, False, False, True]
            self.move_down()
        else:
            self.colliding = True

    def idle(self):
        self.move = [False, False, False, False]

    def get_collisions(self, element_list):
        p = []
        for i in range(len(element_list)):
            p.append(element_list[i])

        for i in range(len(p)):
            if p[i].tag == self.tag:
                p.pop(i)
                break

        # Update Rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        elements = p
        for i in range(len(elements)):
            elements[i].rect = pygame.Rect(elements[i].x, elements[i].y, elements[i].width, elements[i].height)

        # Return colliding Rects
        collider_index = self.rect.collidelistall(elements)
        colliders = []
        for j in range(len(collider_index)):
            colliders.append(elements[collider_index[j]])

        # Determine side of collision
        sides = [False, False, False, False]
        for k in range(len(colliders)):
            if self.determine_side(colliders[k].rect) == "left":
                sides[0] = True
            if self.determine_side(colliders[k].rect) == "right":
                sides[1] = True
            if self.determine_side(colliders[k].rect) == "top":
                sides[2] = True
            if self.determine_side(colliders[k].rect) == "bottom":
                sides[3] = True

        return sides

    def determine_side(self, rect2):
        if self.rect.midtop[1] > rect2.midtop[1]:
            return "top"
        elif self.rect.midleft[0] > rect2.midleft[0]:
            return "left"
        elif self.rect.midright[0] < rect2.midright[0]:
            return "right"
        elif self.rect.midbottom[1] > rect2.midbottom[1]:
            return "bottom"

    def draw_player_movement(self, spritesheet, surface, offset):
        walking_frames = [24, 8, 16, 0]

        if not self.move == [False, False, False, False] and not self.colliding:
            if self.move[0]:
                spritesheet.draw(surface, self.x, self.y, walking_frames[0] + spritesheet.index, offset)
                spritesheet.update_animation_frames(walking_frames[0], walking_frames[0]+7)
                self.last_move = 31
            elif self.move[1]:
                spritesheet.draw(surface, self.x, self.y, walking_frames[1] + spritesheet.index, offset)
                spritesheet.update_animation_frames(walking_frames[1], walking_frames[1]+7)
                self.last_move = walking_frames[1]
            elif self.move[2]:
                spritesheet.draw(surface, self.x, self.y, walking_frames[2] + spritesheet.index, offset)
                spritesheet.update_animation_frames(walking_frames[2], walking_frames[2]+7)
                self.last_move = walking_frames[2]
            elif self.move[3]:
                spritesheet.draw(surface, self.x, self.y, walking_frames[3] + spritesheet.index, offset)
                spritesheet.update_animation_frames(walking_frames[3], walking_frames[3]+7)
                self.last_move = walking_frames[3]
        else:
            spritesheet.draw(surface, self.x, self.y, self.last_move, offset)

    def draw_player_anim(self, spritesheet, surface, offset, start, end):
        spritesheet.draw(surface, self.x, self.y, spritesheet.index, offset)
        spritesheet.update_animation_frames(start, end)