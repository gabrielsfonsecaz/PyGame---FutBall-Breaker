# Importando as bibliotecas necessárias.
import pygame
import random
import time

# Importando funções e classes de arquivos.
from config import FPS, WIDTH, HEIGHT, BLACK, YELLOW, RED
from assets import load_assets, GOAL_SOUND, DIE_SOUND, BACKGROUND, KICK_SOUND, FONTE_PLACAR, BRAZIL_IMG
from sprites import Bar, Ball, Goal, Explosion

def game_screen(window):
    # Variável para o ajuste da taxa de atualização do jogo.
    clock = pygame.time.Clock()

    assets = load_assets()

    # Criando grupos de sprites para os objetos.
    all_sprites = pygame.sprite.Group()
    all_goals = pygame.sprite.Group()
    all_balls = pygame.sprite.Group()
    all_logo = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_goals'] = all_goals
    groups['all_balls'] = all_balls
    groups['all_logo'] = all_logo

    # Criando os objetos do jogo e adicionando aos grupos.
    ball1 = Ball(groups, assets)
    all_sprites.add(ball1)
    all_balls.add(ball1)
    barra = Bar(groups, assets)
    all_sprites.add(barra)

    # Criando os gols para que quando sejam destruídos.
    for i in range(3):
        goal = Goal(groups, assets)
        all_sprites.add(goal)
        all_goals.add(goal)

    # Definindo estados para o jogo e definindo parâmetros para a pontuação e vidas.
    DONE = 0
    PLAYING = 1
    state = PLAYING
    lives = 3
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
                        barra.speedx -= 8.5
                    if event.key == pygame.K_RIGHT:
                        barra.speedx += 8.5
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        barra.speedx += 8.5
                    if event.key == pygame.K_RIGHT:
                        barra.speedx -= 8.5

        # ----- Atualiza estado do jogo
        # Atualizando a posição da bola
        all_sprites.update()
        
        if state == PLAYING:
            
            # Verifica se houve colisão entre a bola e a chuteira
            hits = pygame.sprite.spritecollide(barra, all_balls, False, pygame.sprite.collide_mask)
            if len(hits) > 0:
                ball1.speedx = random.randint(-9, 9)
                while ball1.speedx == 0:
                    ball1.speedx = random.randint(-9, 9)
                ball1.speedy = random.randint(-9, -5)
                while ball1.speedy == 0:
                    ball1.speedy = random.randint(-9, -5)
                assets[KICK_SOUND].play()
                assets[KICK_SOUND].set_volume(0.3)
                
            hits = pygame.sprite.spritecollide(ball1, all_goals, True, pygame.sprite.collide_mask)
            if len(hits) > 0:
                ball1.speedx = random.randint(-9, 9)
                while ball1.speedx == 0:
                    ball1.speedx = random.randint(-9, 9)
                ball1.speedy = random.randint(-12, 12)
                while ball1.speedy == 0:
                    ball1.speedy = random.randint(-12, 12)
                goal_new = Goal(groups, assets)
                goal_new.add(all_goals)
                goal_new.add(all_sprites)
                assets[GOAL_SOUND].play()
                assets[GOAL_SOUND].set_volume(0.25)
                explosao = Explosion(ball1.rect.center, assets)
                all_sprites.add(explosao)

                score += 75
            
            # Estabelecendo condição para caso a bolinha 'morra'.
            if ball1.rect.y > 599:
                lives -= 1
                time.sleep(0.75)
                ball1.rect.x = WIDTH/2
                ball1.rect.y = -20
                ball1.speedx = random.randint(-9, 9)
                while ball1.speedx == 0:
                    ball1.speedx = random.randint(-9, 9)
                ball1.speedy = random.randint(5, 10)

            # Definindo a condição para quando o jogador perder todas as vidas ele perca.
            if lives == 0:
                state = DONE
                pygame.QUIT

            # ----- Gera saídas
            window.fill((0, 0, 0))  # Preenche com a cor branca
            window.blit(assets[BACKGROUND], (0, 0))
            
            # Condição para que o número de camisetas do Brasil desenhadas seja equivalente ao número de vidas.
            x_vida = WIDTH - 130
            for i in range(lives):
                    window.blit(assets[BRAZIL_IMG], (x_vida, 8))
                    x_vida += 40
            
            # Desenhando todos os sprites - objetos.
            all_sprites.draw(window)

            # Desenhando e dimensionando a pontuação.
            text_surface = assets[FONTE_PLACAR].render("{0}".format(score), True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.midtop = (55,  15)
            window.blit(text_surface, text_rect)

            pygame.display.update()  # Mostra o novo frame para o jogador