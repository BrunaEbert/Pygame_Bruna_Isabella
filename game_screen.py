# o loop principal do jogo 
import math
import random
import pygame
from config import (WIDTH, HEIGHT, VIEW_H, FPS, GAME_TIME, COUNTDOWN, GROWTH, SCENES,
                    CARD_RECTS, BUTTON_RECT, WHITE, YELLOW)
from assets import load_assets, SCORE_FONT, FONT, BIG_FONT
from world import World
from desenho import draw_text, draw_world, draw_menu


def game_screen(window):
    clock = pygame.time.Clock()

    assets = load_assets()

    DONE = 0
    PLAYING = 1
    MENU = 2        
    GAME_OVER = 3  
    state = MENU
    selected = 0 
    worlds = []   
    t0 = 0        

    # Loop principal 
    pygame.mixer.music.play(loops=-1)
    while state != DONE:
        clock.tick(FPS)
        now = pygame.time.get_ticks()
        elapsed = (now - t0) / 1000 - COUNTDOWN     
        start = False


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                state = DONE
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_ESCAPE:
                    state = DONE
               
                if state == PLAYING and elapsed >= 0:
                    for w in worlds:
                        if key in (w.key_up, w.key_down):
                            move = -1 if key == w.key_up else 1
                            w.player.lane = max(0, min(3, w.player.lane + move))
                if state == MENU:
                    if key == pygame.K_LEFT:
                        selected = (selected - 1) % len(SCENES)
                    if key == pygame.K_RIGHT:
                        selected = (selected + 1) % len(SCENES)
                    if key in (pygame.K_RETURN, pygame.K_SPACE):
                        start = True
                if state == GAME_OVER:
                    if key == pygame.K_r:
                        start = True
                    if key == pygame.K_m:
                        state = MENU
            if event.type == pygame.MOUSEBUTTONDOWN and state == MENU:
                for i, rect in enumerate(CARD_RECTS):
                    if rect.collidepoint(event.pos):
                        selected = i
                if BUTTON_RECT.collidepoint(event.pos):
                    start = True
 
        # Atualiza estado do jogo
        if start:
            seed = random.randrange(10 ** 6)        # a mesma pista para os dois
            worlds = [World(assets, seed, SCENES[selected], i) for i in range(2)]
            state = PLAYING
            t0 = now
            elapsed = -COUNTDOWN
        if state == PLAYING and elapsed >= GAME_TIME:
            state = GAME_OVER
        elif state == PLAYING and elapsed >= 0:
            for w in worlds:
                w.update(1 + GROWTH * elapsed / GAME_TIME)   # o jogo vai acelerando

        # Gera saídas
        if state == MENU:
            draw_menu(window, assets, selected, now)
        else:
            for i, w in enumerate(worlds):
                draw_world(w, 2 if w.score < worlds[1 - i].score else 1, assets)
                window.blit(w.view, (0, i * VIEW_H))
                if state == PLAYING and elapsed < 0:      # contagem 3, 2, 1
                    draw_text(window, assets[BIG_FONT], str(math.ceil(-elapsed)), (255, 240, 60),
                              center=(WIDTH // 2, i * VIEW_H + 100))
            left = math.ceil(max(0, min(GAME_TIME, GAME_TIME - elapsed)))
            pygame.draw.rect(window, (15, 15, 30), (WIDTH // 2 - 70, VIEW_H - 20, 140, 40))
            draw_text(window, assets[SCORE_FONT], '{}:{:02d}'.format(*divmod(left, 60)),
                      YELLOW, center=(WIDTH // 2, VIEW_H))

            if state == GAME_OVER:
                a, b = worlds
                tie = (a.score, a.hits) == (b.score, b.hits)
                winner = max(worlds, key=lambda w: (w.score, -w.hits))   # desempate: bateu menos
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 170))
                window.blit(overlay, (0, 0))
                draw_text(window, assets[SCORE_FONT], 'FIM DE JOGO', WHITE,
                          center=(WIDTH // 2, HEIGHT // 2 - 80))
                draw_text(window, assets[SCORE_FONT], 'Empate!' if tie else winner.name + ' venceu!',
                          YELLOW if tie else winner.color, center=(WIDTH // 2, HEIGHT // 2 - 30))
                draw_text(window, assets[FONT], '{} {}  x  {} {}'.format(a.name, a.score, b.score, b.name),
                          WHITE, center=(WIDTH // 2, HEIGHT // 2 + 20))
                if a.score == b.score and not tie:
                    draw_text(window, assets[FONT], 'Desempate: bateu menos vezes', YELLOW,
                              center=(WIDTH // 2, HEIGHT // 2 + 50))
                draw_text(window, assets[FONT], 'R = de novo   M = menu   ESC = sair',
                          (200, 200, 200), center=(WIDTH // 2, HEIGHT // 2 + 90))

        pygame.display.update()  # Mostra o novo frame para o jogador