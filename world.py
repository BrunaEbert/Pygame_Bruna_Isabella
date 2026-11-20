import random
import pygame
from config import (WIDTH, VIEW_H, FPS, GAME_TIME, GROWTH, SCREEN_X, STUN_FRAMES, STUN_SLOW, PLAYERS)
from assets import PLAYER_IMGS, BOOM_SOUND, DESTROY_SOUND
from sprites import Player, Item, Explosion


class World:
    # Recebe as imagens e sons, valor usado para iniciar os sorteios, dicionário da cena, índice do jogador
    def __init__(self, assets, seed, scene, index):
        self.assets=assets
        self.scene=scene
        self.name, self.color, self.key_up, self.key_down=PLAYERS[index]  # Configura esses 4 elementos
                                                                            # dependendo do índice (0 ou 1) 
        self.rng=random.Random(seed) # Gerador de sorteios para ambos mundos (sequencia de desafios justa)
        self.view=pygame.Surface((WIDTH, VIEW_H)) # Superfície de corrida do jogador

        self.all_sprites=pygame.sprite.Group() # Reune personagens, itens e explosões
        self.items=pygame.sprite.Group() # Apenas os itens

        self.player=Player(assets[PLAYER_IMGS][index]) # Cria o personagem
        self.all_sprites.add(self.player) # Adiciona-o no grupo

        self.dist=0 # Distância inicial
        self.score=0 # Pontos iniciais
        self.hits=0 # Colisões iniciais
        self.next_x=600 # Coordenada da pista (não da tela) que será gerado o item
        self.last_free=1 # Pista de referência para o obstáculo (será a segunda pista)

    # Cria um item e o adiciona ao grupo geral e ao grupo do item
    def add(self, kind, x, lane):
        item=Item(self.assets, kind, x - self.dist + SCREEN_X, lane) # Parâmetros usados na criação de itens
                                                                      # (o x tá convertido em posição na tela) 
        self.all_sprites.add(item)
        self.items.add(item)

    # Gera o próximo item, variando conforme a dificuldade
    def spawn(self):
        rng, x, scene=self.rng, self.next_x, self.scene # Criação de variáveis
        t=min(1.0, x/(scene['base']*(1 + GROWTH / 2)*FPS* GAME_TIME)) # Calcula um progresso aproximado ao
                                                                    # longo da pista, menor ou igual a 1.0
        d=scene['start']+0.5*t # Calculo da dificuldade, levando em consideração o valor inicial e progresso
        gap=int(rng.randint(150, 230)*(1-0.3*d)) # Calculo do espaçamento dos itens por sorteio
                                                    # (reduz conforme a dificuldade aumenta)
        lane=rng.randrange(4) # Sorteio da pista que vai ganhar o item
        r=rng.random() # Sorteia um numero decimal de zero a um
        gate=0.1+0.3*d # Define o limite usado na escolha do primeiro padrão
        if r<gate:
            free=max(0, min(3, self.last_free + rng.choice((-1, 0, 1)))) # Escolhe uma passegem que fique
                                                                 # na mesma pista, na de cima ou de baixo
            for l in range(4):
                is_free=l==free or (d<0.35 and l==free+1) # Checa se a passagem ta livre de lápides
                self.add('ghost' if is_free else 'tomb', x, l) # Adiciona fantasmas nas passagens e 
                                                                 # lápides nas demais pistas
            self.last_free=free # Atualização da passagem
            gap=max(gap, 190) # Garante um espaçamento mínimo
        elif r<gate + 0.1:
            for i in range(3):
                self.add('ghost', x+i*60, lane) # Adicona 3 fantasmas na mesma pista
            gap+=120 # Aumenta o intervalo
        elif r<gate + 0.55-0.2*d:
            self.add('ghost', x, lane) # Adiciona um fantasma isolado
        else:
            self.add('tomb', x, lane) # Adiciona uma lápide isolada
        self.next_x+=gap # Avança a coordenada para o próximo conjunto

    def update(self, mult):
        speed=max(1, round(self.scene['base']*mult*(STUN_SLOW if self.player.stun else 1))) # Calculo da 
        # velocidade, que leva em consideração a velocidade base, a aceleração e a penalidade (pelo menos =1)
        self.dist+=speed # Avanço
        while self.next_x<self.dist+WIDTH-SCREEN_X+60: # Gera os próximos conjuntos até preencher a pista
                                                          # 60 pixels depois da borda direita
            self.spawn()
        self.all_sprites.update(speed) # Atualiza os personagens, itens e explosões

        hits=pygame.sprite.spritecollide(self.player, self.items, True, pygame.sprite.collide_mask) # Guarda
                             # em uma lista os itens que colidiram (a partir das máscaras) e remove do grupo
        for item in hits: # Checa o que colidiu, toca o som específico, registra, soma ou subtrai pontos
            if item.kind=='ghost':
                self.assets[DESTROY_SOUND].play()
                self.all_sprites.add(Explosion(item.rect.center, self.assets))
                self.score+=1
            else:
                self.assets[BOOM_SOUND].play()
                self.all_sprites.add(Explosion(self.player.rect.center, self.assets))
                self.score=max(0, self.score - 1)
                self.hits+=1
                self.player.stun=STUN_FRAMES