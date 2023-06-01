import random
import pygame
from config import WIDTH, HEIGHT, BALL_WIDTH, BALL_HEIGHT, BAR_WIDTH, BAR_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT, BRAZIL_WIDTH, BRAZIL_HEIGHT
from assets import GOAL_IMG, BALL_IMG, BAR_IMG, BRAZIL_IMG, EXPLOSION_ANIMATION, GOAL_SOUND, DIE_SOUND, KICK_SOUND

class Bar(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[BAR_IMG]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT + 12
        self.groups = groups
        self.speedx = 0

    def update(self):
        # Atualização da posição da chuteira
        self.rect.x += self.speedx

        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[BALL_IMG]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-BALL_WIDTH)
        self.rect.y = random.randint(-100, -BALL_HEIGHT)
        self.speedx = random.randint(-7, 7)
        self.speedy = random.randint(5, 9)
        self.groups = groups

    def update(self):
        # Atualizando a posição da bola
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se a bola passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top < 0:
            self.speedx = random.randint(-9, 9)
            while self.speedx == 0:
                self.speedx = random.randint(-9, 9)
            self.speedy = random.randint(5, 12)
            while self.speedy == 0:
                self.speedy = random.randint(5, 12)
        if self.rect.right > WIDTH:
            self.speedx = random.randint(-9, -5)
            while self.speedx == 0:
                self.speedx = random.randint(-9, -5)
            self.speedy = random.randint(-12, 12)
            while self.speedy == 0:
                self.speedy = random.randint(-12, 12)
        if self.rect.left < 0:
            self.speedx = random.randint(5, 9)
            while self.speedx == 0:
                self.speedx = random.randint(5, 9)
            self.speedy = random.randint(-12, 12)
            while self.speedy == 0:
                self.speedy = random.randint(-12, 12)

class Goal(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[GOAL_IMG]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(GOAL_WIDTH/2, WIDTH - GOAL_WIDTH/2)
        self.rect.bottom = random.randint(GOAL_HEIGHT/2 + 20, HEIGHT/2)
        self.groups = groups
        self.speedx = 0

    def update(self):
        # Atualização da posição da chuteira
        self.rect.x += self.speedx

        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0 

# Classe que representa uma explosão de meteoro
class Explosion(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, center, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação de explosão
        self.explosion_anim = assets[EXPLOSION_ANIMATION]

        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0  # Armazena o índice atual na animação
        self.image = self.explosion_anim[self.frame]  # Pega a primeira imagem
        self.rect = self.image.get_rect()
        self.rect.center = center  # Posiciona o centro da imagem

        # Guarda o tick da primeira imagem, ou seja, o momento em que a imagem foi mostrada
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        # Quando pygame.time.get_ticks() - self.last_update > self.frame_ticks a
        # próxima imagem da animação será mostrada
        self.frame_ticks = 50

    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Verifica se já chegou no final da animação.
            if self.frame == len(self.explosion_anim):
                # Se sim, tchau explosão!
                self.kill()
            else:
                # Se ainda não chegou ao fim da explosão, troca de imagem.
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center