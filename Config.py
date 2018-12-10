import pygame

win_width = 520
win_height = 520
hww = int(win_width/2)
hwh = int(win_height/2)


# Some colors

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
YELLOW = (255, 204, 0, 255)

# Initialize variables and load sprites
FPS = 60
offset = (-8, -40)

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