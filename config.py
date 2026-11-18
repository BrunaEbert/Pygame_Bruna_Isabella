from os import path
import pygame

BASE_DIR=path.dirname(path.abspath(__file__))
IMG_DIR=path.join(BASE_DIR, 'assets', 'img')
SND_DIR=path.join(BASE_DIR, 'assets', 'snd')

WIDTH=800
HEIGHT=600
VIEW_H=HEIGHT // 2
FPS=30

GAME_TIME=120
COUNTDOWN=3
GROWTH=1.0

SCREEN_X=180
HORIZON=130
LANES_Y=[175, 210, 245, 280]
LANE_SPEED=6
STUN_FRAMES=30
STUN_SLOW=0.35

PLAYER_SIZE=(52, 52)
ITEM_SIZE=(40, 46)
MID_W=1600

WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
YELLOW=(255, 255, 0)

PLAYERS = [('Scooby', (205, 133, 63), pygame.K_UP, pygame.K_DOWN),('Salsicha', (80, 200, 120), pygame.K_w, pygame.K_s)]

SCENES = [
    {'name': 'Floresta Sombria', 'level': 'FACIL', 'level_color': (80, 220, 100),
     'color': (18, 44, 38), 'ground': (20, 38, 24), 'base': 5, 'start': -0.2},
    {'name': 'Casa Assombrada', 'level': 'MEDIO', 'level_color': (255, 220, 60),
     'color': (36, 28, 58), 'ground': (22, 34, 28), 'base': 6, 'start': 0.1},
    {'name': 'Navio Fantasma', 'level': 'DIFICIL', 'level_color': (255, 80, 80),
     'color': (20, 34, 66), 'ground': (34, 28, 22), 'base': 7, 'start': 0.4},
]

CARD_RECTS=[pygame.Rect(20 + i * 260, 330, 240, 130) for i in range(len(SCENES))]
BUTTON_RECT=pygame.Rect(WIDTH // 2 - 150, 495, 300, 50)