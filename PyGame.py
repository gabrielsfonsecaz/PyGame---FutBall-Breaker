# ===== Inicialização =====
# ----- Importa e inicia pacotes 
import pygame
import time
from config import WIDTH, HEIGHT, INIT, GAME, QUIT, INST
from init_screen import init_screen
from game_screen import game_screen
from gameover_screen import gameover_screen
from instructions_screen import instructions_screen

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('FutBall Breaker')
 
state = INIT
while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    if state == INST:
        state == instructions_screen(window)
        time.sleep(5)
        state = GAME
    if state == GAME:
        state = game_screen(window)
    else:
        state = gameover_screen(window)
        time.sleep(2.5)
        state = QUIT

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados