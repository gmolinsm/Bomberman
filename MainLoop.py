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
grid = Grid(32, 32)
offset = (0, 0)
bomber_movement = SpriteSheet("assets/BomberMovement.png", 32, 6)
bomber_idle1 = SpriteSheet("assets/Idle1.png", 5, 12)
bomber_idle2 = SpriteSheet("assets/Idle2.png", 5, 12)
border_sprite = Sprite("assets/Border.png")
player1 = PlayerCharacter(hww, hwh, grid, 3)
player2 = PlayerCharacter(hww+50, hwh+50, grid, 3)
player3 = PlayerCharacter(hww-50, hwh-50, grid, 3)


# Game events
def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player1.move_left()
    elif keys[pygame.K_RIGHT]:
        player1.move_right()
    elif keys[pygame.K_UP]:
        player1.move_up()
    elif keys[pygame.K_DOWN]:
        player1.move_down()

    if keys[pygame.K_ESCAPE]:
        run = False
        pygame.quit()
        sys.exit()

    pygame.display.update()


def redraw_game_elements():
    global offset

    # Order of displaying elements must be respected
    win.fill(BLACK)
    border_sprite.draw(win, 0, 0)
    player1.draw_player_movement(bomber_movement, win, offset)
    player2.draw_player_anim(bomber_idle1, win, offset, 0, 4)
    player3.draw_player_anim(bomber_idle2, win, offset, 0, 4)

    # Reference point
    pygame.draw.circle(win, WHITE, (hww, hwh), 2, 0)


run = True
while run:
    clock.tick(FPS)
    events()
    redraw_game_elements()
exit(0)