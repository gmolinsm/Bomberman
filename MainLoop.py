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
offset = (5, 32)
bomber_m = SpriteSheet("assets/BomberMovement.png", 32)
border_sprite = Sprite("assets/Border.png")
player1 = PlayerCharacter(hww, hwh, grid, 3)
walking_frames = [24, 8, 16, 0]
index = 0
last_move = 0
frame_interpolation = frame_interpolation_init = 7


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


def redraw_game_window():
    global walking_frames
    global offset
    global index
    global last_move
    global frame_interpolation

    # Window
    win.fill(BLACK)
    # Stage
    border_sprite.draw(win, 0, 0)
    # Bomber movement
    if index+1 >= 8:
        index = 0

    if player1.is_moving():
        if player1.moving[0]:
            bomber_m.draw(win, player1.x, player1.y, walking_frames[0] + index, offset)
            last_move = 31
        elif player1.moving[1]:
            bomber_m.draw(win, player1.x, player1.y, walking_frames[1] + index, offset)
            last_move = walking_frames[1]
        elif player1.moving[2]:
            bomber_m.draw(win, player1.x, player1.y, walking_frames[2] + index, offset)
            last_move = walking_frames[2]
        elif player1.moving[3]:
            bomber_m.draw(win, player1.x, player1.y, walking_frames[3] + index, offset)
            last_move = walking_frames[3]
        if frame_interpolation == 0:
            index += 1
            frame_interpolation = frame_interpolation_init
        else:
            frame_interpolation -= 1
    else:
        bomber_m.draw(win, player1.x, player1.y, last_move, offset)

    # Reference point
    pygame.draw.circle(win, WHITE, (hww, hwh), 2, 0)
    pygame.display.update()


run = True
while run:
    clock.tick(FPS)
    events()
    redraw_game_window()
exit(0)