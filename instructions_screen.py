# Importando as bibliotecas necessárias.
import pygame
from os import path

# Importando algumas constantes do arquivo 'config.py'.
from config import IMG_DIR, YELLOW, FPS, GAME, QUIT, OVER, INST

def instructions_screen(screen):
    clock = pygame.time.Clock()
    
    background = pygame.image.load(path.join(IMG_DIR, 'instrucoes.png')).convert()
    background = pygame.transform.smoothscale(background, (450, 600)) # Redimensionando o tamanho da imagem.
    background_rect = background.get_rect()

    clock.tick(FPS)

    screen.blit(background, background_rect)

    pygame.display.update()  # Mostra o novo frame para o jogador