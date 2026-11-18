import pygame
from config import (WIDTH, VIEW_H, HORIZON, LANES_Y, MID_W, SCENES, CARD_RECTS, BUTTON_RECT,
                    WHITE, YELLOW)
from assets import BACKGROUND, MIDS, SCORE_FONT, FONT
from sprites import Explosion


def draw_text(window, font, text, color, **anchor):
    surf = font.render(text, True, color)
    window.blit(surf, surf.get_rect(**anchor))


def draw_background(surf, assets, scene, dist):
    """Céu, cenário, chão e pistas. Usado no jogo e no menu."""
    bg = assets[BACKGROUND]
    for x in range(-(dist // 20 % bg.get_width()), WIDTH, bg.get_width()):   # o céu rola devagar
        surf.blit(bg, (x, 0))
    pygame.draw.circle(surf, (245, 240, 200), (660, 44), 28)                  # lua
    mid = assets[MIDS][scene['name']]
    surf.blit(mid, (-(dist // 3 % MID_W), 0))                                  # cenário rola mais rápido
    surf.blit(mid, (MID_W - dist // 3 % MID_W, 0))
    pygame.draw.rect(surf, scene['ground'], (0, HORIZON, WIDTH, VIEW_H - HORIZON))
    for x in range(-(dist % 80), WIDTH + 80, 80):                              # chão
        pygame.draw.line(surf, [c + 12 for c in scene['ground']], (x, HORIZON), (x - 40, VIEW_H), 3)
    for y in [y - 24 for y in LANES_Y] + [LANES_Y[-1] + 10]:                   # divisórias das pistas
        for x in range(-(dist % 60), WIDTH, 60):
            pygame.draw.line(surf, (70, 90, 80), (x, y), (x + 30, y), 2)


def draw_world(w, rank, assets):
    draw_background(w.view, assets, w.scene, w.dist)
    # Quem está mais embaixo na tela fica na frente; explosões ficam por cima
    for s in sorted(w.all_sprites, key=lambda s: s.rect.bottom + 99 * isinstance(s, Explosion)):
        w.view.blit(s.image, s.rect)
    pygame.draw.rect(w.view, w.color, (0, 0, WIDTH, 4))
    draw_text(w.view, assets[FONT], w.name, w.color, topleft=(12, 8))
    draw_text(w.view, assets[SCORE_FONT], '{:03d}'.format(w.score), YELLOW, topleft=(12, 32))
    draw_text(w.view, assets[SCORE_FONT], '{}o'.format(rank), w.color, topright=(WIDTH - 14, 12))


def draw_menu(window, assets, selected, now):
    """Tela inicial. A cena escolhida aparece rolando no topo."""
    preview = pygame.Surface((WIDTH, VIEW_H))
    draw_background(preview, assets, SCENES[selected], now // 6)
    window.fill((10, 10, 20))
    window.blit(preview, (0, 0))
    draw_text(window, assets[SCORE_FONT], 'CORRIDA ASSOMBRADA', (255, 230, 80), center=(WIDTH // 2, 90))
    draw_text(window, assets[FONT], 'Scooby x Salsicha', WHITE, center=(WIDTH // 2, 140))
    draw_text(window, assets[FONT], 'Escolha a cena', WHITE, center=(WIDTH // 2, 310))
    for i, scene in enumerate(SCENES):
        rect = CARD_RECTS[i]
        pygame.draw.rect(window, (30, 30, 55), rect, border_radius=10)
        border, width = (WHITE, 4) if i == selected else ((80, 80, 110), 2)
        pygame.draw.rect(window, border, rect, width, border_radius=10)
        draw_text(window, assets[FONT], scene['name'], WHITE, center=(rect.centerx, rect.y + 45))
        draw_text(window, assets[SCORE_FONT], scene['level'], scene['level_color'],
                  center=(rect.centerx, rect.y + 90))
    pygame.draw.rect(window, (60, 170, 80), BUTTON_RECT, border_radius=12)
    pygame.draw.rect(window, WHITE, BUTTON_RECT, 3, border_radius=12)
    draw_text(window, assets[SCORE_FONT], 'INICIAR', WHITE, center=BUTTON_RECT.center)
    draw_text(window, assets[FONT], 'SETAS < > escolhem   ENTER ou clique inicia',
              (200, 200, 200), center=(WIDTH // 2, 565))
    draw_text(window, assets[FONT], 'Scooby: setas CIMA/BAIXO   Salsicha: W/S',
              (200, 200, 200), center=(WIDTH // 2, 586))