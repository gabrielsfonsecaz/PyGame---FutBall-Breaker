import pygame # Importa a biblioteca PyGame, utilizada para criar jogos em Python
import os #  Importa o módulo 'os', que fornece funcionalidades relacionadas ao sistema operacional, como manipulação de arquivos.
from config import BALL_WIDTH, BALL_HEIGHT, BAR_WIDTH, BAR_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT, BRAZIL_WIDTH, BRAZIL_HEIGHT, IMG_DIR, SND_DIR, FNT_DIR # Importa as constantes definidas no arquivo 'config.py', que devem fornecer informações sobre os tamanhos dos objetos do jogo e os diretórios onde os recursos estão armazenados.

# Define variáveis com strings para representar as chaves dos recursos no dicionário 'assets'.
BACKGROUND = 'background' 
GOAL_IMG = 'goal_img'
BALL_IMG = 'ball_img'
BAR_IMG = 'bar_img'
BRAZIL_IMG = 'brazil_img'
EXPLOSION_ANIMATION = 'explosion_animation'
FONTE_PLACAR = 'fonte_placar'
GOAL_SOUND = 'goal_sound'
DIE_SOUND = 'die_sound'
KICK_SOUND = 'kick_sound'

# Função que carrega todos os recursos do jogo e retorna um dicionário contendo esses recursos, que serão posteriormente utilizados na implementação do jogo.
def load_assets():
    assets = {}
    # 'load' -> Carregar as imagens dos arquivos correspondentes aos caminhos definidos em 'IMG_DIR'.
    # 'smoothscale' ->  redimensionar as imagens carregadas para os tamanhos desejados, usando as constantes definidas anteriormente.
    assets[BACKGROUND] = pygame.image.load(os.path.join(IMG_DIR, 'quadra.png')).convert()
    assets[BACKGROUND] = pygame.transform.smoothscale(assets['background'], (450, 600))
    assets[GOAL_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'goal.png')).convert_alpha()
    assets[GOAL_IMG] = pygame.transform.smoothscale(assets['goal_img'], (GOAL_WIDTH, GOAL_HEIGHT))
    assets[BALL_IMG] = pygame.image.load(os.path.join(IMG_DIR, 'ball.png')).convert_alpha()
    assets[BALL_IMG] = pygame.transform.smoothscale(assets['ball_img'], (BALL_WIDTH, BALL_HEIGHT))
    assets[BAR_IMG]= pygame.image.load(os.path.join(IMG_DIR, 'chuteira.png')).convert_alpha()
    assets[BAR_IMG] = pygame.transform.smoothscale(assets['bar_img'], (BAR_WIDTH, BAR_HEIGHT))
    assets[BRAZIL_IMG]= pygame.image.load(os.path.join(IMG_DIR, 'brasilpontos.png')).convert_alpha()
    assets[BRAZIL_IMG] = pygame.transform.smoothscale(assets['brazil_img'], (BRAZIL_WIDTH, BRAZIL_HEIGHT))

    explosion_animation = [] # Lista vazia para guardar as informações da explosão
    for i in range(9):
        # Os arquivos de animação são numerados de 00 a 08
        filename = os.path.join(IMG_DIR, 'regularExplosion0{}.png'.format(i))
        img = pygame.image.load(filename).convert()
        img = pygame.transform.smoothscale(img, (40, 40))
        explosion_animation.append(img)
    # Armazena a fonte carregada no dicionário 'assets' com a chave correspondente.
    assets[EXPLOSION_ANIMATION] = explosion_animation

    # Função para carregar a fonte desejada do arquivo no caminho definido em 'FNT_DIR' e com o tamanho 36.
    assets[FONTE_PLACAR] = pygame.font.Font(os.path.join(FNT_DIR, 'Senzow.ttf'), 36)

    # Carrega os sons do jogo
    pygame.mixer.music.load(os.path.join(SND_DIR, 'torcidafutebol.ogg')) # Função para carregar a música de fundo do jogo.
    pygame.mixer.music.set_volume(0.2) # Função para para definir o volume da música.
    # Armazena os sons carregados no dicionário assets com as chaves correspondentes.
    assets[GOAL_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'gol.wav'))
    assets[DIE_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'mariodies.wav'))
    assets[KICK_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'chute.wav'))
    return assets # Retorna o dicionário assets contendo todos os recursos carregados.