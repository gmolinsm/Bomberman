import pygame
win_width = 480
win_height = 480


class PlayerCharacter(object):
    def __init__(self, x, y, grid, speed, tag="Player", key_set=[pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]):
        w = self.width = grid.cell_width/2
        h = self.height = grid.cell_height/2
        self.hw = int(w/2)
        self.hh = int(h/2)
        self.speed = speed
        """self.tag = tag"""

        if 0 < x - self.hw < win_width:
            self.x = x - self.hw
        else:
            self.x = -self.hw
        if 0 < y - self.hh < win_height:
            self.y = y - self.hh
        else:
            self.y = -self.hh

        self.rect = pygame.Rect(self.x, self.y, grid.width, grid.height)
        self.move = [False, False, False, False]
        self.last_move = False
        self.last_move_frame = 0
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
            self.colliding = True

    def idle(self):
        self.move = [False, False, False, False]

    def get_collisions(self, element_list):
        """p = []
        for i in range(len(element_list)):
            p.append(element_list[i])

        for i in range(len(p)):
            if p[i].tag == self.tag:
                p.pop(i)
                break"""

        # Update Rect of player and elements
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        elements = element_list
        for i in range(len(elements)):
            elements[i].rect = pygame.Rect(elements[i].x, elements[i].y, elements[i].width, elements[i].height)

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
            if side == "right":
                sides[1] = True
            if side == "top":
                sides[2] = True
            if side == "bottom":
                sides[3] = True
        return sides

    def determine_side(self, rect2):
        margin = 10
        if self.x + margin > rect2.x + rect2.width:
            return "left"
        if self.x + self.width < rect2.x + margin:
            return "right"
        if self.y + margin > rect2.y + rect2.height:
            return "top"
        if self.y + self.width < rect2.y + margin:
            return "bottom"

    def draw_player_movement(self, spritesheet, surface, offset):
        walking_frames = [24, 8, 16, 0]

        if not self.move == [False, False, False, False] and not self.colliding:
            if self.move[0]:
                spritesheet.draw(surface, self.x, self.y, walking_frames[0] + spritesheet.index, offset)
                spritesheet.update_animation_frames(walking_frames[0], walking_frames[0]+7)
                self.last_move_frame = 31
            elif self.move[1]:
                spritesheet.draw(surface, self.x, self.y, walking_frames[1] + spritesheet.index, offset)
                spritesheet.update_animation_frames(walking_frames[1], walking_frames[1]+7)
                self.last_move_frame = walking_frames[1]
            elif self.move[2]:
                spritesheet.draw(surface, self.x, self.y, walking_frames[2] + spritesheet.index, offset)
                spritesheet.update_animation_frames(walking_frames[2], walking_frames[2]+7)
                self.last_move_frame = walking_frames[2]
            elif self.move[3]:
                spritesheet.draw(surface, self.x, self.y, walking_frames[3] + spritesheet.index, offset)
                spritesheet.update_animation_frames(walking_frames[3], walking_frames[3]+7)
                self.last_move_frame = walking_frames[3]
        else:
            spritesheet.draw(surface, self.x, self.y, self.last_move_frame, offset)

    def draw_player_anim(self, spritesheet, surface, offset, start, end):
        spritesheet.draw(surface, self.x, self.y, spritesheet.index, offset)
        spritesheet.update_animation_frames(start, end)