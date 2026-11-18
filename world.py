import random
import pygame
from config import (WIDTH, VIEW_H, FPS, GAME_TIME, GROWTH, SCREEN_X, STUN_FRAMES, STUN_SLOW, PLAYERS)
from assets import PLAYER_IMGS, BOOM_SOUND, DESTROY_SOUND
from sprites import Player, Item, Explosion

class World:
    def __init__(self, assets, seed, scene, index):
        self.assets=assets
        self.scene=scene
        self.name, self.color, self.key_up, self.key_down=PLAYERS[index]
        self.rng=random.Random(seed)
        self.view=pygame.Surface((WIDTH, VIEW_H))

        self.all_sprites=pygame.sprite.Group()
        self.items=pygame.sprite.Group()

        self.player=Player(assets[PLAYER_IMGS][index])
        self.all_sprites.add(self.player)

        self.dist=0
        self.score=0
        self.hits=0
        self.next_x=600
        self.last_free=1

    def add(self, kind, x, lane):
        item=Item(self.assets, kind, x - self.dist + SCREEN_X, lane)
        self.all_sprites.add(item)
        self.items.add(item)

    def spawn(self):
        rng, x, scene=self.rng, self.next_x, self.scene
        t=min(1.0, x / (scene['base'] * (1 + GROWTH / 2) * FPS * GAME_TIME))
        d=scene['start'] + 0.5 * t
        gap=int(rng.randint(150, 230) * (1 - 0.3 * d))
        lane=rng.randrange(4)
        r=rng.random()
        gate=0.1 + 0.3 * d
        if r<gate:
            free=max(0, min(3, self.last_free + rng.choice((-1, 0, 1))))
            for l in range(4):
                is_free=l==free or (d < 0.35 and l == free + 1)
                self.add('ghost' if is_free else 'tomb', x, l)
            self.last_free=free
            gap=max(gap, 190)
        elif r<gate + 0.1:
            for i in range(3):
                self.add('ghost', x + i * 60, lane)
            gap+=120
        elif r<gate + 0.55 - 0.2 * d:
            self.add('ghost', x, lane)
        else:
            self.add('tomb', x, lane)
        self.next_x+=gap

    def update(self, mult):
        speed=max(1, round(self.scene['base'] * mult * (STUN_SLOW if self.player.stun else 1)))
        self.dist+=speed
        while self.next_x<self.dist + WIDTH - SCREEN_X + 60:
            self.spawn()
        self.all_sprites.update(speed)

        hits=pygame.sprite.spritecollide(self.player, self.items, True, pygame.sprite.collide_mask)
        for item in hits:
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