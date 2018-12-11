from GameClasses import *


class PlayerCharacter(object):
    def __init__(self, x, y, spritesheets, key_set=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE], tag="Player"):
        self.width = 28
        self.height = 28
        self.lives = 1
        self.speed = 3
        self.tag = tag
        self.movement = SpriteSheet(spritesheets[0][0], spritesheets[0][1], spritesheets[0][2])
        self.waiting1 = SpriteSheet(spritesheets[1][0], spritesheets[1][1], spritesheets[1][2])
        self.waiting2 = SpriteSheet(spritesheets[2][0], spritesheets[2][1], spritesheets[2][2])
        self.death = SpriteSheet(spritesheets[3][0], spritesheets[3][1], spritesheets[3][2])

        if 0 < x < win_width:
            self.x = x
        else:
            self.x = 0
        if 0 < y < win_height:
            self.y = y
        else:
            self.y = 0

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.move = [False, False, False, False]
        self.last_move_frame = 0
        self.not_moving = False
        self.key_set = key_set

    def move_left(self):
        if self.x - self.speed > 0:
            self.x -= self.speed
            self.not_moving = False
        else:
            self.not_moving = True

    def move_right(self):
        if self.x + self.width + self.speed < win_width:
            self.x += self.speed
            self.not_moving = False
        else:
            self.not_moving = True

    def move_up(self):
        if self.y - self.speed > 0:
            self.y -= self.speed
            self.not_moving = False
        else:
            self.not_moving = True

    def move_down(self):
        if self.y + self.height + self.speed < win_height:
            self.y += self.speed
            self.not_moving = False
        else:
            self.not_moving = True

    def check_move(self, direction, elements):

        collisions = self.get_collisions(elements)
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
            self.not_moving = True

    def idle(self):
        self.move = [False, False, False, False]

    def get_collisions(self, element_list):
        # Update Rect of player and elements
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        elements = element_list
        for i in range(len(elements)):
            elements[i].rect = pygame.Rect(elements[i].x, elements[i].y,
                                           elements[i].width, elements[i].height)

        # Return colliding Rects
        colliders = []
        for j in range(len(elements)):
            if self.rect.colliderect(elements[j].rect):
                colliders.append(elements[j])

        # Determine side of collision
        sides = [False, False, False, False]
        for k in range(len(colliders)):
            side = self.determine_side(colliders[k].rect)
            if side == "left":
                sides[0] = True
            elif side == "right":
                sides[1] = True
            elif side == "top":
                sides[2] = True
            elif side == "bottom":
                sides[3] = True
        return sides

    def determine_side(self, rect2):
        margin = 20
        border_margin = 5
        side = ""
        if self.x + margin > rect2.x + rect2.width \
                and (rect2.y + border_margin <= self.y <= rect2.y + rect2.height - border_margin
                     or rect2.y + border_margin <= self.y + self.height <= rect2.y + rect2.height - border_margin
                     or rect2.y + border_margin <= self.y + self.height/2 <= rect2.y + rect2.height - border_margin):
            side = "left"
        if self.x + self.width < rect2.x + margin \
                and (rect2.y + border_margin <= self.y <= rect2.y + rect2.height - border_margin
                     or rect2.y + border_margin <= self.y + self.height <= rect2.y + rect2.height - border_margin
                     or rect2.y + border_margin <= self.y + self.height / 2 <= rect2.y + rect2.height - border_margin):
            side = "right"
        if self.y + margin > rect2.y + rect2.height \
                and (rect2.x + border_margin <= self.x <= rect2.x + rect2.width - border_margin
                     or rect2.x + border_margin <= self.x + self.width <= rect2.x + rect2.width - border_margin
                     or rect2.x + border_margin <= self.x + self.width / 2 <= rect2.x + rect2.width - border_margin):
            side = "top"
        if self.y + self.width < rect2.y + margin \
                and (rect2.x + border_margin <= self.x <= rect2.x + rect2.width - border_margin
                     or rect2.x + border_margin <= self.x + self.width <= rect2.x + rect2.width - border_margin
                     or rect2.x + border_margin <= self.x + self.width / 2 <= rect2.x + rect2.width - border_margin):
            side = "bottom"
        return side

    def get_pos(self, grid):
        for i in range(grid.cell_count):
            if grid.cell_list[i].rect.collidepoint(self.x + int(self.width/2), self.y + int(self.height/2)):
                return grid.cell_list[i]
        return None

    def draw_player_movement(self, surface, offset):
        walking_frames = [24, 8, 16, 0]

        if not self.move == [False, False, False, False] and not self.not_moving:
            if self.move[0]:
                self.movement.draw(surface, self.x, self.y, walking_frames[0] + self.movement.index, offset)
                self.movement.update_animation_frames(walking_frames[0], walking_frames[0]+7)
                self.last_move_frame = 31
            elif self.move[1]:
                self.movement.draw(surface, self.x, self.y, walking_frames[1] + self.movement.index, offset)
                self.movement.update_animation_frames(walking_frames[1], walking_frames[1]+7)
                self.last_move_frame = walking_frames[1]
            elif self.move[2]:
                self.movement.draw(surface, self.x, self.y, walking_frames[2] + self.movement.index, offset)
                self.movement.update_animation_frames(walking_frames[2], walking_frames[2]+7)
                self.last_move_frame = walking_frames[2]
            elif self.move[3]:
                self.movement.draw(surface, self.x, self.y, walking_frames[3] + self.movement.index, offset)
                self.movement.update_animation_frames(walking_frames[3], walking_frames[3]+7)
                self.last_move_frame = walking_frames[3]
        else:
            if self.last_move_frame == 31:
                self.movement.draw(surface, self.x, self.y, self.last_move_frame, (offset[0] + 7, offset[1]))
            elif self.last_move_frame == walking_frames[1]:
                self.movement.draw(surface, self.x, self.y, self.last_move_frame, (offset[0] - 5, offset[1]))
            else:
                self.movement.draw(surface, self.x, self.y, self.last_move_frame, offset)

    def draw_player_anim(self, spritesheet, surface, offset, start, end):
        spritesheet.draw(surface, self.x, self.y, spritesheet.index, offset)
        spritesheet.update_animation_frames(start, end)

