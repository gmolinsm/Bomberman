from Config import *
import sys

pygame.init()
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("BomberMan")
clock = pygame.time.Clock()


# Game events
def events():
    global colliding_cells
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Create a list of colliders to feed into the functions
    colliders = colliding_cells

    # Player movement events
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
                bombs.append(Bomb(pos, pygame.time.get_ticks(), explosions))

    if keys[pygame.K_ESCAPE]:
        run = False
        pygame.quit()
        sys.exit()

    # Player general events
    for i in range(len(players)):
        if players[i].lives <= 0:
            if players[i].death.count >= 1:
                players.pop(i)
                break
            else:
                players[i].speed = 0

        if len(players) == 1:
            win.fill(BLACK)
            message = str(players[i].tag) + " WINS!"
            text(win, title, message, YELLOW)

    # Bomb events
    for i in range(len(bombs)):
        if bombs[i].timer < current_time:
            if not bombs[i].exploded:
                bombs[i].exploded = True
                bombs[i].explode(grid, players, explosions)
            colliding_cells = grid.get_colliding_cells()
            if bombs[i].explosion.count >= 1:
                bombs.pop(i)
                break


def redraw_game_elements():
    elements = players + grid.cell_list + bombs

    # Order of displaying elements must be respected
    win.fill(BLACK)
    grid.draw_grid(grass_sprite, win)

    # Render the elements with greater "y" attribute first
    elements.sort(key=lambda element: element.y + element.height/2, reverse=False)
    for i in range(len(elements)):
        if type(elements[i]) == PlayerCharacter:
            if elements[i].lives > 0:
                elements[i].draw_player_movement(win, offset)
            else:
                if elements[i].death.count < 1:
                    elements[i].draw_player_anim(elements[i].death, win, offset, 0, 4)
        elif type(elements[i]) == Ground:
            if elements[i].destroyed:
                if elements[i].destroyed_spritesheet.count < 1:
                    elements[i].draw_anim(elements[i].destroyed_spritesheet, win, 0, 6)
                else:
                    elements[i].destroyed = False
            if not elements[i].collides and not elements[i].destroyed:
                if elements[i].flame_type == "left_end":
                    if elements[i].flames_left_end.count < 1:
                        elements[i].draw_anim(elements[i].flames_left_end, win, 0, 4)
                    else:
                        elements[i].flames_left_end.count = 0
                        elements[i].flame_type = ""
                if elements[i].flame_type == "right_end":
                    if elements[i].flames_right_end.count < 1:
                        elements[i].draw_anim(elements[i].flames_right_end, win, 0, 4)
                    else:
                        elements[i].flames_right_end.count = 0
                        elements[i].flame_type = ""
                if elements[i].flame_type == "top_end":
                    if elements[i].flames_top_end.count < 1:
                        elements[i].draw_anim(elements[i].flames_top_end, win, 0, 4)
                    else:
                        elements[i].flames_top_end.count = 0
                        elements[i].flame_type = ""
                if elements[i].flame_type == "bottom_end":
                    if elements[i].flames_bottom_end.count < 1:
                        elements[i].draw_anim(elements[i].flames_bottom_end, win, 0, 4)
                    else:
                        elements[i].flames_bottom_end.count = 0
                        elements[i].flame_type = ""
                if elements[i].flame_type == "mid_horizontal":
                    if elements[i].flames_middle_horizontal.count < 1:
                        elements[i].draw_anim(elements[i].flames_middle_horizontal, win, 0, 4)
                    else:
                        elements[i].flames_middle_horizontal.count = 0
                        elements[i].flame_type = ""
                if elements[i].flame_type == "mid_vertical":
                    if elements[i].flames_middle_vertical.count < 1:
                        elements[i].draw_anim(elements[i].flames_middle_vertical, win, 0, 4)
                    else:
                        elements[i].flames_middle_vertical.count = 0
                        elements[i].flame_type = ""
        elif type(elements[i]) == Wall:

            if elements[i].type == 0:
                elements[i].draw(border_sprite, win)
            elif elements[i].type == 1:
                elements[i].draw(hard_wall_sprite, win)
            elif elements[i].type == 2:
                elements[i].draw(soft_wall_sprite, win)
        elif type(elements[i]) == Bomb:
            if not elements[i].exploded:
                elements[i].draw_anim(elements[i].pre_explosion, win, 0, 4)
            elif elements[i].exploded:
                if elements[i].explosion.count < 1:
                    elements[i].draw_anim(elements[i].explosion, win, 0, 4)

    # Reference point


def text(surface, font, message, color):
    screen_text = font.render(message, True, color)
    surface.blit(screen_text, (hww - screen_text.get_rect().width/2, hwh - screen_text.get_rect().height/2))


run = True
while run:
    clock.tick(FPS)
    redraw_game_elements()
    events()
    pygame.display.update()
    pygame.display.flip()
exit(0)