import pygame
from config import SCREEN_X, LANES_Y, LANE_SPEED #Importa configuração de posição e movimento
from assets import GHOST_IMG, TOMB_IMG, EXPLOSION_ANIM #Importa a bisca por imagens

# Criação de uma máscara para ela ser usada como área de colisão, evitando que a parte de cima
   # dos personagens em pistas próximas cause uma colisão
def feet_mask(image):
    feet=pygame.Surface(image.get_size(), pygame.SRCALPHA)
    feet.fill((255, 255, 255, 255), (8, image.get_height() - 14, image.get_width() - 16, 14))
    return pygame.mask.from_surface(feet) # Retorno é um retângulo na base do personagem

# Criação do jogador e controlador da sua posição
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        # Preepara a imagem, a máscara de colisão e a posição inicial
        pygame.sprite.Sprite.__init__(self)
        self.image=image
        self.mask=feet_mask(image)
        self.rect=image.get_rect() 
        self.rect.centerx=SCREEN_X
        self.lane=1 # Começa inicialmente na segunda pista 
        self.rect.bottom=LANES_Y[self.lane] # Coloca a base do personagem na linha dois
        self.stun=0 # Incia com nenhuma penalidade por colisão
    def update(self, speed):
        diff=LANES_Y[self.lane]-self.rect.bottom # Calcula quanto falta para chegar a linha escolihida 
                                                    # (positivo: descer; negativo: subir; zero: nada)
        self.rect.bottom+=max(-LANE_SPEED, min(LANE_SPEED, diff)) # Limita o deslocamento de -6 a 6
        self.stun=max(0, self.stun - 1) #Diminuição do contador de penalidade em uma unidade, sem
                                          # deixar que ele seja menor que zero 
# Criação dos fantasma e lápides
class Item(pygame.sprite.Sprite):
    def __init__(self, assets, kind, x, lane):
        # Escolhe a imagem e a posiciona
        pygame.sprite.Sprite.__init__(self)
        self.kind=kind
        self.image=assets[GHOST_IMG] if kind == 'ghost' else assets[TOMB_IMG]
        self.mask=feet_mask(self.image)
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.bottom=LANES_Y[lane]

    # Move o item para a esquerda e o remove dos grupos quando sai da tela (isso que da a sensação 
       # do personagem estar correndo, mas na verdade os itens que vão em sua direção)
    def update(self, speed):
        self.rect.x-=speed
        if self.rect.right<0:
            self.kill()

# Criação da explosão
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, assets):
        pygame.sprite.Sprite.__init__(self)
        self.explosion_anim=assets[EXPLOSION_ANIM] #lista de imagens da animação

        # Inicia o processo de animação colocando a primeira imagem na tela
        self.frame=0
        self.image=self.explosion_anim[self.frame]
        self.rect=self.image.get_rect()
        self.rect.center=center  # Posiciona a explosão no centro da imagem
        
        self.last_update=pygame.time.get_ticks() # Guarda o tick da primeira imagem
        self.frame_ticks=50 # Troca de imagem a cada 50 milissegundos

    def update(self, speed=0):
        now=pygame.time.get_ticks() # Guarda o tick atual
        elapsed_ticks=now-self.last_update # Calcula quantos ticks se passaram desde a ultima mudança

        if elapsed_ticks>self.frame_ticks: # Se ja se passaram mais de 50 milissegundos
            self.last_update=now

            self.frame+=1 # Incrementa o índice

            if self.frame==len(self.explosion_anim): # Verifica se todas as imagens já foram exibidas
                self.kill()
            else: #Mantém a troca de imagens
                center=self.rect.center
                self.image=self.explosion_anim[self.frame]
                self.rect=self.image.get_rect()
                self.rect.center=center
