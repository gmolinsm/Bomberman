from PlayerCharacter import *
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

# Initialize variables and load sprites
FPS = 60
offset = (-6, -30)

bomber_movement = ["assets/BomberMovement.png", 32, 6]
bomber_idle1 = ["assets/Idle1.png", 5, 12]
bomber_idle2 = ["assets/Idle2.png", 5, 12]
bomb_pre_explosion = ["assets/Bomb_pre_explosion.png", 5, 15]
bomb_explosion = ["assets/Bomb_explosion.png", 5, 5]
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

players = [PlayerCharacter(grid.cell_list[72].x, grid.cell_list[72].y, bomber_movement, [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_e], "Player 1"),
           PlayerCharacter(grid.cell_list[85].x, grid.cell_list[85].y, bomber_movement, [pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k, pygame.K_u], "Player 2"),
           PlayerCharacter(grid.cell_list[154].x, grid.cell_list[154].y, bomber_movement, [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE], "Player 3")]
bombs = []


# Game events
def events():
    global players
    global bombs
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Create a list of colliders to feed into the functions
    colliders = players + grid.get_colliding_cells() + bombs

    # Check for user input
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

        if keys[players[i].key_set[4]]:
            pos = players[i].get_pos(grid)
            for j in range(len(bombs)):
                if bombs[j].cell == pos:
                    pos = None
            if pos is not None:
                bombs.append(Bomb(pos, pygame.time.get_ticks(), bomb_pre_explosion, bomb_explosion))

    if keys[pygame.K_ESCAPE]:
        run = False
        pygame.quit()
        sys.exit()

    pygame.display.update()

    # Explode and remove bombs
    for i in range(len(bombs)):
        if bombs[i].timer - 500 <= current_time:
            bombs[i].exploded = True
        if bombs[i].timer <= current_time:
            bombs[i].explode(grid, players)
            bombs.pop(i)
            break

    # Check for player lives
    for i in range(len(players)):
        if players[i].lives <= 0:
            players.pop(i)
            break


def redraw_game_elements():
    global offset
    global players
    global bomber_movement

    elements = players + grid.cell_list + bombs

    # Order of displaying elements must be respected
    win.fill(BLACK)
    grid.draw_grid(grass_sprite, win)

    # Render the elements with greater "y" attribute first
    elements.sort(key=lambda element: element.y + element.height/2, reverse=False)
    for i in range(len(elements)):
        if type(elements[i]) == PlayerCharacter:
                elements[i].draw_player_movement(win, offset)
        elif type(elements[i]) == Cell:
            if elements[i].cell_type == 1:
                elements[i].draw(border_sprite, win)
            elif elements[i].cell_type == 2:
                elements[i].draw(hard_wall_sprite, win)
            elif elements[i].cell_type == 3:
                elements[i].draw(soft_wall_sprite, win)
        elif type(elements[i]) == Bomb:
            if not elements[i].exploded:
                elements[i].draw(elements[i].pre_explosion, win, 0, 4)
            elif elements[i].exploded:
                elements[i].draw(elements[i].explosion, win, 0, 4)

    # Reference point


run = True
while run:
    clock.tick(FPS)
    events()
    redraw_game_elements()
    pygame.display.flip()
exit(0)