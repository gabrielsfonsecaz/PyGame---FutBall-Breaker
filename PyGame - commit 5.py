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
explosion_animation = []
for i in range(9):
    # Os arquivos de animação são numerados de 00 a 08
    filename = 'assets/img/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img = pygame.transform.smoothscale(img, (40, 40))
    explosion_animation.append(img)
assets['explosion_animation'] = explosion_animation

assets["fonte_placar"] = pygame.font.Font('assets/font/Rumbling.ttf', 36)

# Carrega os sons do jogo
pygame.mixer.music.load('assets/snd/torcidafutebol.ogg')
pygame.mixer.music.set_volume(0.2)
assets['goal_sound'] = pygame.mixer.Sound('assets/snd/gol.wav')
assets['die_sound'] = pygame.mixer.Sound('assets/snd/mariodies.wav')
assets['kick_sound'] = pygame.mixer.Sound('assets/snd/chute.wav')

class Bar(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['bar_img']
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

        self.image = assets['ball_img']
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-BALL_WIDTH)
        self.rect.y = random.randint(-100, -BALL_HEIGHT)
        self.speedx = random.randint(-6, 6)
        self.speedy = random.randint(1, 9)
        self.groups = groups

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
    def __init__(self, groups, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['goal_img']
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
        self.explosion_anim = assets['explosion_animation']

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

# ----- Inicia estruturas de dados
game = True
# Variável para o ajuste de velocidade
clock = pygame.time.Clock()
FPS = 30

# Criando um grupo de 'gols'
all_sprites = pygame.sprite.Group()
all_goals = pygame.sprite.Group()
all_balls = pygame.sprite.Group()
groups = {}
groups['all_sprites'] = all_sprites
groups['all_goals'] = all_goals
groups['all_balls'] = all_balls
ball1 = Ball(groups, assets)
barra = Bar(groups, assets)
all_sprites.add(barra)
all_sprites.add(ball1)
all_balls.add(ball1)

for i in range(3):
    goal = Goal(groups, assets)
    all_sprites.add(goal)
    all_goals.add(goal)

DONE = 0
PLAYING = 1
EXPLODING = 2
state = PLAYING

score = 0
# ===== Loop principal =====
pygame.mixer.music.play(loops=-1)
while state != DONE:
    clock.tick(FPS)
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            state = DONE
        if state == PLAYING:
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
    
    if state == PLAYING:
        # Verifica se houve colisão entre a bola e a chuteira
        hits = pygame.sprite.spritecollide(barra, all_balls, False)
        if len(hits) > 0:
            ball1.speedx = random.randint(-8, 8)
            while ball1.speedx == 0:
                ball1.speedx = random.randint(-8, 8)
            ball1.speedy = random.randint(-12, -1)
            while ball1.speedy == 0:
                ball1.speedy = random.randint(-12, -1)
            assets['kick_sound'].play()
            assets['kick_sound'].set_volume(0.3)
            
        hits = pygame.sprite.spritecollide(ball1, all_goals, True)
        if len(hits) > 0:
            ball1.speedx = random.randint(-8, 8)
            while ball1.speedx == 0:
                ball1.speedx = random.randint(-8, 8)
            ball1.speedy = random.randint(-12, 12)
            while ball1.speedy == 0:
                ball1.speedy = random.randint(-12, 12)
            goal_new = Goal(groups, assets)
            goal_new.add(all_goals)
            goal_new.add(all_sprites)
            assets['goal_sound'].play()
            assets['goal_sound'].set_volume(0.25)
            explosao = Explosion(ball1.rect.center, assets)
            all_sprites.add(explosao)

            score += 75

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(assets['background'], (0, 0))
    all_sprites.draw(window)

    text_surface = assets['fonte_placar'].render("{:08d}".format(score), True, (19, 23, 208))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (80,  5)
    window.blit(text_surface, text_rect)

    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados