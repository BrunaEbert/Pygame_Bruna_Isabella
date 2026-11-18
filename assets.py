import os
import pygame
from config import IMG_DIR, SND_DIR, PLAYER_SIZE, ITEM_SIZE, MID_W, HORIZON, SCENES


BACKGROUND = 'background'
PLAYER_IMGS = 'player_imgs'
GHOST_IMG = 'ghost_img'
TOMB_IMG = 'tomb_img'
MIDS = 'mids'
EXPLOSION_ANIM = 'explosion_anim'
SCORE_FONT = 'score_font'
FONT = 'font'
BIG_FONT = 'big_font'
BOOM_SOUND = 'boom_sound'
DESTROY_SOUND = 'destroy_sound'


def player_image(filename, paint):
    file = os.path.join(IMG_DIR, filename)
    if os.path.exists(file):
        return pygame.transform.scale(pygame.image.load(file).convert_alpha(), PLAYER_SIZE)
    img = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
    paint(img)
    return img


def paint_scooby(img):
    brown = (150, 100, 55)
    pygame.draw.ellipse(img, brown, (6, 20, 34, 24))                        # corpo
    for x in (12, 18, 30, 36):
        pygame.draw.rect(img, brown, (x, 38, 6, 12))                        # patas
    pygame.draw.circle(img, brown, (40, 20), 11)                            # cabeça
    pygame.draw.ellipse(img, (95, 60, 30), (30, 10, 9, 16))                 # orelha
    pygame.draw.circle(img, (255, 255, 255), (42, 16), 3)                   # olho
    pygame.draw.rect(img, (60, 170, 200), (32, 28, 10, 4))                  # coleira


def paint_salsicha(img):
    hair = (110, 70, 40)
    pygame.draw.rect(img, hair, (17, 38, 18, 12))                           # calça
    pygame.draw.rect(img, (80, 175, 90), (14, 20, 24, 20), border_radius=4)  # camiseta
    pygame.draw.circle(img, (240, 200, 160), (27, 12), 10)                  # cabeça
    pygame.draw.ellipse(img, hair, (17, 1, 20, 9))                          # cabelo
    pygame.draw.circle(img, (20, 20, 20), (31, 12), 2)                      # olho


# Fantasma e lápide
def make_ghost():
    img = pygame.Surface(ITEM_SIZE, pygame.SRCALPHA)
    pygame.draw.circle(img, (235, 240, 255), (20, 20), 20)
    pygame.draw.rect(img, (235, 240, 255), (0, 20, 40, 26))
    for x in (11, 29):
        pygame.draw.circle(img, (20, 20, 40), (x, 18), 5)                   # olhos
    pygame.draw.ellipse(img, (20, 20, 40), (15, 28, 10, 12))                # boca
    return img


def make_tomb():
    img = pygame.Surface(ITEM_SIZE, pygame.SRCALPHA)
    pygame.draw.rect(img, (120, 125, 140), (4, 18, 32, 28))
    pygame.draw.circle(img, (120, 125, 140), (20, 18), 16)
    text = pygame.font.Font(None, 18).render('RIP', True, (55, 60, 75))
    img.blit(text, text.get_rect(center=(20, 28)))
    return img


# Cenários: o que passa ao fundo 
def paint_forest(s, c):
    for x in range(30, MID_W, 110):                                         # pinheiros
        h = 70 + (x * 7) % 40
        for i in range(3):
            top = HORIZON - h + i * (h // 4)
            pygame.draw.polygon(s, c, [(x, top), (x - 18 - 8 * i, top + h // 2),
                                       (x + 18 + 8 * i, top + h // 2)])
    pygame.draw.rect(s, c, (540, HORIZON - 50, 110, 38), border_radius=8)   # van parada
    for x in (564, 628):
        pygame.draw.circle(s, c, (x, HORIZON - 12), 11)
    for x in (260, 800, 1230):                                              # olhos nos arbustos
        pygame.draw.ellipse(s, c, (x, HORIZON - 30, 60, 30))
        pygame.draw.circle(s, (255, 230, 80), (x + 22, HORIZON - 18), 3)
        pygame.draw.circle(s, (255, 230, 80), (x + 36, HORIZON - 18), 3)


def paint_house(s, c):
    for x in (120, 930):                                                    # casas
        pygame.draw.rect(s, c, (x, 60, 190, 70))
        pygame.draw.polygon(s, c, [(x - 15, 62), (x + 95, 18), (x + 205, 62)])
        for wx in (x + 22, x + 110):
            pygame.draw.rect(s, (240, 200, 70), (wx, 72, 18, 24))           # janelas acesas
    for x in range(40, MID_W, 300):                                         # árvores secas
        pygame.draw.line(s, c, (x, HORIZON), (x + 15, 55), 9)
        pygame.draw.line(s, c, (x + 8, 90), (x + 40, 60), 5)


def paint_ship(s, c):
    for x in (120, 960):                                                    # navios
        pygame.draw.polygon(s, c, [(x, 88), (x + 210, 88), (x + 180, 124), (x + 30, 124)])
        for m in (60, 110, 160):
            pygame.draw.line(s, c, (x + m, 88), (x + m, 10), 4)             # mastro
            pygame.draw.polygon(s, c, [(x + m + 3, 16), (x + m + 40, 26),
                                       (x + m + 30, 62), (x + m + 3, 56)])  # vela rasgada
            pygame.draw.circle(s, (120, 255, 170), (x + m, 104), 5)         # luz verde
    pygame.draw.rect(s, c, (0, HORIZON - 8, MID_W, 8))


def load_assets():
    assets = {}
    assets[BACKGROUND] = pygame.image.load(os.path.join(IMG_DIR, 'ceu.png')).convert()
    assets[PLAYER_IMGS] = [player_image('scooby.png', paint_scooby),
                           player_image('salsicha.png', paint_salsicha)]
    assets[GHOST_IMG] = make_ghost()
    assets[TOMB_IMG] = make_tomb()

    # Uma camada de cenário para cada cena 
    assets[MIDS] = {}
    for scene, paint in zip(SCENES, [paint_forest, paint_house, paint_ship]):
        mid = pygame.Surface((MID_W, HORIZON), pygame.SRCALPHA)
        paint(mid, scene['color'])
        assets[MIDS][scene['name']] = mid

    explosion_anim = []
    for i in range(9):
        filename = os.path.join(IMG_DIR, 'explosao{}.png'.format(i))
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img, (48, 48))
        explosion_anim.append(img)
    assets[EXPLOSION_ANIM] = explosion_anim

    assets[SCORE_FONT] = pygame.font.SysFont('arial', 34, True)
    assets[FONT] = pygame.font.SysFont('arial', 20, True)
    assets[BIG_FONT] = pygame.font.SysFont('arial', 110, True)

    # Carrega os sons do jogo
    pygame.mixer.music.load(os.path.join(SND_DIR, 'musica.wav'))
    pygame.mixer.music.set_volume(0.4)
    assets[BOOM_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'bateu.wav'))      # bateu na lápide
    assets[DESTROY_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'pegou.wav'))   # pegou um fantasma
    return assets