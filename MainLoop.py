from GameClasses import *
import sys

pygame.init()
hww = int(win_width/2)
hwh = int(win_height/2)
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("BomberMan")
clock = pygame.time.Clock()

# Some colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)

# Initialize variables and load images
FPS = 60
offset = (-6, -40)

bomber_movement = [SpriteSheet("assets/BomberMovement.png", 32, 6),
                   SpriteSheet("assets/BomberMovement.png", 32, 6),
                   SpriteSheet("assets/BomberMovement.png", 32, 6)]
bomber_idle = [SpriteSheet("assets/Idle1.png", 5, 12), SpriteSheet("assets/Idle2.png", 5, 12)]
border_sprite = Sprite("assets/Border.png")
grass_sprite = Sprite("assets/Grass.png")
soft_wall_sprite = Sprite("assets/Soft_Wall.png")
hard_wall_sprite = Sprite("assets/Hard_Wall.png")

map_layout = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 1,
              1, 0, 2, 3, 2, 0, 2, 0, 2, 3, 2, 0, 1,
              1, 3, 3, 0, 3, 3, 3, 3, 3, 0, 3, 3, 1,
              1, 3, 2, 3, 2, 0, 2, 0, 2, 3, 2, 3, 1,
              1, 3, 0, 3, 0, 0, 0, 0, 0, 3, 0, 3, 1,
              1, 3, 2, 3, 2, 0, 2, 0, 2, 3, 2, 3, 1,
              1, 3, 0, 3, 0, 0, 0, 0, 0, 3, 0, 3, 1,
              1, 3, 2, 3, 2, 0, 2, 0, 2, 3, 2, 3, 1,
              1, 3, 3, 0, 3, 3, 3, 3, 3, 0, 3, 3, 1,
              1, 0, 2, 3, 2, 0, 2, 0, 2, 3, 2, 0, 1,
              1, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 1,
              1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

grid = Grid(40, 40)
grid.build_grid(map_layout)

players = [PlayerCharacter(grid.cell_list[14].x, grid.cell_list[14].y, grid, 3, [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s], "Player 1"),
           PlayerCharacter(hww, hwh, grid, 3, [pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k], "Player 2"),
           PlayerCharacter(grid.cell_list[154].x, grid.cell_list[154].y, grid, 3, [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN], "Player 3")]

colliders = players + grid.get_colliding_cells()

# Game events
def events():
    global players
    global colliders

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    for i in range(len(players)):
        if keys[players[i].key_set[0]]:
            players[i].check_move("left", colliders)
        elif keys[players[i].key_set[1]]:
            players[i].check_move("right", colliders)
        elif keys[players[i].key_set[2]]:
            players[i].check_move("up", colliders)
        elif keys[players[i].key_set[3]]:
            players[i].check_move("down", colliders)
        else:
            players[i].idle()

    if keys[pygame.K_ESCAPE]:
        run = False
        pygame.quit()
        sys.exit()

    pygame.display.update()


def redraw_game_elements():
    global offset
    global players
    global bomber_movement

    elements = players + grid.cell_list

    # Order of displaying elements must be respected
    win.fill(BLACK)
    grid.draw_grid(grass_sprite, win)

    # Render the elements with greater "y" attribute first
    elements.sort(key=lambda element: element.y + element.height/2, reverse=False)
    for i in range(len(elements)):
        if type(elements[i]) == PlayerCharacter:
            if elements[i].tag == "Player 1":
                elements[i].draw_player_movement(bomber_movement[0], win, offset)
            elif elements[i].tag == "Player 2":
                elements[i].draw_player_movement(bomber_movement[1], win, offset)
            elif elements[i].tag == "Player 3":
                elements[i].draw_player_movement(bomber_movement[2], win, offset)
        elif type(elements[i]) == Cell:
            if elements[i].cell_type == 1:
                elements[i].draw(border_sprite, win)
            elif elements[i].cell_type == 2:
                elements[i].draw(hard_wall_sprite, win)
            elif elements[i].cell_type == 3:
                elements[i].draw(soft_wall_sprite, win)

    # Reference point
    pygame.draw.rect(win, WHITE, players[0].rect)
    pygame.draw.rect(win, WHITE, players[1].rect)
    pygame.draw.rect(win, WHITE, players[2].rect)


run = True
while run:
    clock.tick(FPS)
    events()
    redraw_game_elements()
    pygame.display.flip()
exit(0)