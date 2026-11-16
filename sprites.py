import pygame
from config import SCREEN_X, LANES_Y, LANE_SPEED
from assets import GHOST_IMG, TOMB_IMG, EXPLOSION_ANIM

def feet_mask(image):
    feet=pygame.Surface(image.get_size(), pygame.SRCALPHA)
    feet.fill((255, 255, 255, 255), (8, image.get_height() - 14, image.get_width() - 16, 14))
    return pygame.mask.from_surface(feet)

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        # Construtor da classe mãe (Sprite)
        pygame.sprite.Sprite.__init__(self)
        self.image=image
        self.mask=feet_mask(image)
        self.rect=image.get_rect()
        self.rect.centerx=SCREEN_X
        self.lane=1
        self.rect.bottom=LANES_Y[self.lane]
        self.stun=0
    def update(self, speed):
        diff=LANES_Y[self.lane]-self.rect.bottom
        self.rect.bottom+=max(-LANE_SPEED, min(LANE_SPEED, diff))
        self.stun=max(0, self.stun - 1)

class Item(pygame.sprite.Sprite):
    def __init__(self, assets, kind, x, lane):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        self.kind=kind            
        self.image=assets[GHOST_IMG] if kind == 'ghost' else assets[TOMB_IMG]
        self.mask=feet_mask(self.image)
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.bottom=LANES_Y[lane]

    def update(self, speed):
        self.rect.x-=speed
        if self.rect.right<0:
            self.kill()

# Classe que representa uma explosão
class Explosion(pygame.sprite.Sprite):
    # Construtor da classe
    def __init__(self, center, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação de explosão
        self.explosion_anim=assets[EXPLOSION_ANIM]

        # Inicia o processo de animação colocando a primeira imagem na tela
        self.frame=0
        self.image=self.explosion_anim[self.frame]
        self.rect=self.image.get_rect()
        self.rect.center=center  # Posiciona o centro da imagem

        # Guarda o tick da primeira imagem
        self.last_update=pygame.time.get_ticks()

        # Troca de imagem a cada self.frame_ticks milissegundos
        self.frame_ticks=50

    def update(self, speed=0):
        # Verifica o tick atual
        now=pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde a ultima mudança de frame
        elapsed_ticks=now-self.last_update

        if elapsed_ticks>self.frame_ticks:
            self.last_update=now

            self.frame+=1

            if self.frame==len(self.explosion_anim):
                self.kill()
            else:
                center=self.rect.center
                self.image=self.explosion_anim[self.frame]
                self.rect=self.image.get_rect()
                self.rect.center=center
