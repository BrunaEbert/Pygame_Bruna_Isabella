# Arquivo principal: inicia o pygame, chama a tela do jogo e finaliza o pygame.

#Importa e inicia pacotes
import pygame
from config import WIDTH, HEIGHT
from game_screen import game_screen

pygame.init()
pygame.mixer.init()

#Gera tela principal
window= pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Corrida Assombrada")

game_screen(window)

#Finalizacao 
pygame.quit() #funcao que finaliza os recursos utilizados