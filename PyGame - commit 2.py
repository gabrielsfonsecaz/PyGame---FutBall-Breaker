# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
WIDTH = 450
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('FutBall Breaker')

# ----- Inicia assets
BALL_WIDTH = 20
BALL_HEIGHT = 20
BAR_WIDTH = 80
BAR_HEIGHT = 60
GOAL_WIDTH = 100
GOAL_HEIGHT = 60
assets = {}
font = pygame.font.SysFont(None, 48)
assets['background'] = pygame.image.load('assets/img/quadra.png').convert()
assets['background'] = pygame.transform.smoothscale(assets['background'], (450, 600))
assets['goal_img'] = pygame.image.load('assets/img/goal.png').convert_alpha()
assets['goal_img'] = pygame.transform.smoothscale(assets['goal_img'], (GOAL_WIDTH, GOAL_HEIGHT))
assets['ball_img'] = pygame.image.load('assets/img/ball.png').convert_alpha()
assets['ball_img'] = pygame.transform.smoothscale(assets['ball_img'], (BALL_WIDTH, BALL_HEIGHT))
assets['bar_img']= pygame.image.load('assets/img/chuteira.png').convert_alpha()
assets['bar_img'] = pygame.transform.smoothscale(assets['bar_img'], (BAR_WIDTH, BAR_HEIGHT))

# Carrega os sons do jogo
pygame.mixer.music.load('assets/snd/torcidafutebol.ogg')
pygame.mixer.music.set_volume(0.2)
goal_sound = pygame.mixer.Sound('assets/snd/gol.wav')
die_sound = pygame.mixer.Sound('assets/snd/mariodies.wav')
kick_sound = pygame.mixer.Sound('assets/snd/chute.wav')

class Bar(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT + 12
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
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-BALL_WIDTH)
        self.rect.y = random.randint(-100, -BALL_HEIGHT)
        self.speedx = random.randint(-6, 6)
        self.speedy = random.randint(1, 9)

    def update(self):
        # Atualizando a posição da bola
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se a bola passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top < 0:
            self.speedx = random.randint(-10, 10)
            while self.speedx == 0:
                self.speedx = random.randint(-10, 10)
            self.speedy = random.randint(1, 15)
            while self.speedy == 0:
                self.speedy = random.randint(1, 15)
        if self.rect.right > WIDTH:
            self.speedx = random.randint(-10, -1)
            while self.speedx == 0:
                self.speedx = random.randint(-10, -1)
            self.speedy = random.randint(-15, 15)
            while self.speedy == 0:
                self.speedy = random.randint(-15, 15)
        if self.rect.left < 0:
            self.speedx = random.randint(1, 10)
            while self.speedx == 0:
                self.speedx = random.randint(1, 10)
            self.speedy = random.randint(-15, 15)
            while self.speedy == 0:
                self.speedy = random.randint(-15, 15)
        if self.rect.y > HEIGHT:
            time.sleep(0.5)
            self.rect.x = random.randint(0, WIDTH-BALL_WIDTH)
            self.rect.y = random.randint(-100, -BALL_HEIGHT)
            self.speedx = random.randint(-6, 6)
            while self.speedx == 0:
                self.speedx = random.randint(-6, 6)
            self.speedy = random.randint(1, 9)
            while self.speedy == 0:
                self.speedy = random.randint(1, 9)

    
class Goal(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(GOAL_WIDTH/2, WIDTH - GOAL_WIDTH/2)
        self.rect.bottom = random.randint(GOAL_HEIGHT/2 + 20, HEIGHT/2)
        self.speedx = 0

    def update(self):
        # Atualização da posição da chuteira
        self.rect.x += self.speedx

        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

# ----- Inicia estruturas de dados
game = True
# Variável para o ajuste de velocidade
clock = pygame.time.Clock()
FPS = 30

# Criando um grupo de 'gols'
all_sprites = pygame.sprite.Group()
all_goals = pygame.sprite.Group()
all_balls = pygame.sprite.Group()
ball1 = Ball(ball_img)
barra = Bar(bar_img)
all_sprites.add(barra)
all_sprites.add(ball1)
all_balls.add(ball1)

for i in range(3):
    goal = Goal(goal_img)
    all_sprites.add(goal)
    all_goals.add(goal)

# ===== Loop principal =====
pygame.mixer.music.play(loops=-1)
while game:
    clock.tick(FPS)
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False
        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                barra.speedx -= 8
            if event.key == pygame.K_RIGHT:
                barra.speedx += 8
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                barra.speedx += 8
            if event.key == pygame.K_RIGHT:
                barra.speedx -= 8

    # ----- Atualiza estado do jogo
    # Atualizando a posição da bola
    all_sprites.update()
    
    # Verifica se houve colisão entre a bola e a chuteira
    hits = pygame.sprite.spritecollide(barra, all_balls, False)
    if len(hits) > 0:
        ball1.speedx = random.randint(-8, 8)
        while ball1.speedx == 0:
            ball1.speedx = random.randint(-8, 8)
        ball1.speedy = random.randint(-12, -1)
        while ball1.speedy == 0:
            ball1.speedy = random.randint(-12, -1)
        kick_sound.play()
        kick_sound.set_volume(0.3)
        
    hits = pygame.sprite.spritecollide(ball1, all_goals, True)
    if len(hits) > 0:
        ball1.speedx = random.randint(-8, 8)
        while ball1.speedx == 0:
            ball1.speedx = random.randint(-8, 8)
        ball1.speedy = random.randint(-12, 12)
        while ball1.speedy == 0:
            ball1.speedy = random.randint(-12, 12)
        goal_new = Goal(goal_img)
        goal_new.add(all_goals)
        goal_new.add(all_sprites)
        goal_sound.play()
        goal_sound.set_volume(0.25)

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(background, (0, 0))
    all_sprites.draw(window)
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados