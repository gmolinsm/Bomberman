from PlayerCharacter import *

hww = int(win_width/2)
hwh = int(win_height/2)

# Some colors

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
YELLOW = (255, 204, 0, 255)

# Initialize variables and load sprites
FPS = 60
offset = (-7, -40)

pygame.font.init()
title = pygame.font.Font("assets/Fonts/Bungee-Regular.ttf", 40)
tag = pygame.font.Font("assets/Fonts/FjallaOne-Regular.ttf", 20)

border_sprite = Sprite("assets/Border.png")
grass_sprite = Sprite("assets/Grass.png")
soft_wall_sprite = Sprite("assets/Soft_Wall.png")
hard_wall_sprite = Sprite("assets/Hard_Wall.png")

player_sprites = [["assets/BomberMovement.png", 32, 6],
          ["assets/Idle1.png", 5, 12],
          ["assets/Idle2.png", 5, 12],
          ["assets/Death.png", 5, 6]]

explosions = [["assets/Bomb_pre_explosion.png", 5, 15], ["assets/Bomb_explosion.png", 5, 5],
              ["assets/Flames_left_end.png", 5, 5], ["assets/Flames_right_end.png", 5, 5],
              ["assets/Flames_top_end.png", 5, 5], ["assets/Flames_bottom_end.png", 5, 5],
              ["assets/Middle_horizontal.png", 5, 5], ["assets/Middle_vertical.png", 5, 5],
              ["assets/Wall_destruction.png", 7, 6]]

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
grid.build_grid(map_layout, explosions)

players = [PlayerCharacter(grid.cell_list[14].x, grid.cell_list[14].y, player_sprites, [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_e], "Player 1"),
           PlayerCharacter(grid.cell_list[24].x, grid.cell_list[24].y, player_sprites, [pygame.K_f, pygame.K_h, pygame.K_t, pygame.K_g, pygame.K_y], "Player 2"),
           PlayerCharacter(grid.cell_list[144].x, grid.cell_list[144].y, player_sprites, [pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k, pygame.K_u], "Player 3"),
           PlayerCharacter(grid.cell_list[154].x, grid.cell_list[154].y, player_sprites, [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE], "Player 4")]
bombs = []
colliding_cells = grid.get_colliding_cells()