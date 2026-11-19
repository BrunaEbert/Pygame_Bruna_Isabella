# Importa ferramentas para caminhos de arquivos e recursos do Pygame
from os import path
import pygame

# Define a pasta onde esse arquivo está salvo
BASE_DIR=path.dirname(path.abspath(__file__))
# Define o caminho onde as imagens e sons estão
IMG_DIR=path.join(BASE_DIR, 'assets', 'img')
SND_DIR=path.join(BASE_DIR, 'assets', 'snd')

WIDTH=800
HEIGHT=600
VIEW_H=HEIGHT // 2
FPS=30

GAME_TIME=120
COUNTDOWN=3
GROWTH=1.0

SCREEN_X=180 # Define o centro horizontal do personagem
HORIZON=130 # Define onde começa o chão do mapa
LANES_Y=[175, 210, 245, 280] # Gurada a posição vertical do personagem ou dos itens em cada uma das quatro pistas
LANE_SPEED=6 # Quantidade de pixels que o personagem se desloca ao trocar de pista
STUN_FRAMES=30 # Penalidade caso colida
STUN_SLOW=0.35 # Redução da velocidade quando colide

PLAYER_SIZE=(52, 52)
ITEM_SIZE=(40, 46)
MID_W=1600

WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
YELLOW=(255, 255, 0)

# Definição dos jogadores e como se movem
PLAYERS = [('Scooby', (205, 133, 63), pygame.K_UP, pygame.K_DOWN),('Salsicha', (80, 200, 120), pygame.K_w, pygame.K_s)]

# Definição dos cenários com nome, dificuldade, cores e velocidade
SCENES = [
    {'name': 'Floresta Sombria', 'level': 'FACIL', 'level_color': (80, 220, 100),
     'color': (18, 44, 38), 'ground': (20, 38, 24), 'base': 5, 'start': -0.2},
    {'name': 'Casa Assombrada', 'level': 'MEDIO', 'level_color': (255, 220, 60),
     'color': (36, 28, 58), 'ground': (22, 34, 28), 'base': 6, 'start': 0.1},
    {'name': 'Navio Fantasma', 'level': 'DIFICIL', 'level_color': (255, 80, 80),
     'color': (20, 34, 66), 'ground': (34, 28, 22), 'base': 7, 'start': 0.4},
]

# Criação de retângulos para o desenho e interação
CARD_RECTS=[pygame.Rect(20 + i * 260, 330, 240, 130) for i in range(len(SCENES))]
# Criação do retângulo do botão iniciar
BUTTON_RECT=pygame.Rect(WIDTH // 2 - 150, 495, 300, 50)