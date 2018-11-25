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
offset = (-9, -35)

bomber_movement = SpriteSheet("assets/BomberMovement.png", 32, 6)
bomber_idle1 = SpriteSheet("assets/Idle1.png", 5, 12)
bomber_idle2 = SpriteSheet("assets/Idle2.png", 5, 12)
border_sprite = Sprite("assets/Border.png")
grass_sprite = Sprite("assets/Grass.png")

grid = Grid(40, 40)


players = [PlayerCharacter(hww, hwh, grid, 3, [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]),
           PlayerCharacter(hww+100, hwh+100, grid, 3, [pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k]),
           PlayerCharacter(hww-100, hwh-100, grid, 3)]


# Game events
def events():
    global players

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    for i in range(0, len(players)):
        if keys[players[i].key_set[0]]:
            players[i].move_left()
        elif keys[players[i].key_set[1]]:
            players[i].move_right()
        elif keys[players[i].key_set[2]]:
            players[i].move_up()
        elif keys[players[i].key_set[3]]:
            players[i].move_down()

    if keys[pygame.K_ESCAPE]:
        run = False
        pygame.quit()
        sys.exit()

    pygame.display.update()


def redraw_game_elements():
    global offset
    global players

    # Order of displaying elements must be respected
    win.fill(BLACK)
    grid.draw_grid(grass_sprite, win)
    grid.draw_cell(border_sprite, win, 34)
    players[0].draw_player_movement(bomber_movement, win, offset)
    players[1].draw_player_anim(bomber_idle1, win, offset, 0, 4)

    if players[0].is_colliding(players[1]):
        print("Colliding")
    players[2].draw_player_anim(bomber_idle2, win, offset, 0, 4)

    # Reference point
    pygame.draw.circle(win, WHITE, (hww-2, hwh-2), 2, 0)


run = True
while run:
    clock.tick(FPS)
    events()
    redraw_game_elements()
exit(0)