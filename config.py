# Importar a função 'path' da biblioteca 'os', que é usada para manipular caminhos de arquivo
from os import path

# Estabelece a pasta que contém as figuras, sons e fontes.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')

# Dados gerais do jogo.
WIDTH = 450 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define tamanhos
BALL_WIDTH = 20 # Largura da bola
BALL_HEIGHT = 20 # Altura da bola
BAR_WIDTH = 80 # Largura da chuteira
BAR_HEIGHT = 60 # Altura da chuteira
GOAL_WIDTH = 70 # Largura do gol
GOAL_HEIGHT = 40 # Altura do gol
BRAZIL_WIDTH = 50 # Largura das vidas
BRAZIL_HEIGHT = 50 # Altura das vidas

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Estados para controle do fluxo da aplicação
INIT = 0 # Estado inicial
INST = 1 # Tela de instruções
GAME = 2 # Estado de jogo
OVER = 3 # Estado de tela de game over do jogo
QUIT = 4 # Estado de encerramento do jogo