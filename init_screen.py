# Importando as bibliotecas necessárias.
import pygame
from os import path

# Importando algumas constantes do arquivo 'config.py'.
from config import IMG_DIR, YELLOW, FPS, QUIT, INST

# Definindo uma função para a tela de início do jogo.
def init_screen(screen):
    # Variável para o ajuste de velocidade de atualização do jogo.
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(IMG_DIR, 'telainicio.png')).convert()
    background = pygame.transform.smoothscale(background, (450, 600)) # Redimensionando o tamanho da imagem.
    background_rect = background.get_rect()

    running = True # Variável 'running' é definida como 'True' para indicar que o jogo está em execução.
    while running:
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(YELLOW)
        screen.blit(background, background_rect)
        pygame.display.update()

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = INST
                running = False

            if event.type == pygame.QUIT:
                state = QUIT
                running = False
                
    return state