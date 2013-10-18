import os
import pygame
from os.path import join as join_path


dados_py = os.path.abspath(os.path.dirname(__file__))
dados_dir = os.path.normpath(join_path(dados_py, '..', 'dados'))


endereco_arquivos = dict(
    fontes=join_path(dados_dir, 'fontes'),
    imagens=join_path(dados_dir, 'imagens'),
    sons=join_path(dados_dir, 'sons'),
    fases=join_path(dados_dir, 'fases'),
)


def endereco_arquivo(tipo, nome_arquivo):
    return join_path(endereco_arquivos[tipo], nome_arquivo)


def carrega(tipo, nome_arquivo, modo='rb'):
    return open(endereco_arquivo(tipo, nome_arquivo), modo)


def carrega_fonte(nome_arquivo):
    return endereco_arquivo('fontes', nome_arquivo)


def carrega_imagem(nome_arquivo):
    return endereco_arquivo('imagens', nome_arquivo)


def carrega_fase(nome_arquivo):
    return open(endereco_arquivo('fases', nome_arquivo))


def carrega_imagem_menu(nome_arquivo):
    nome_arquivo = carrega('imagens', nome_arquivo)
    try:
        image = pygame.image.load(nome_arquivo)
    except pygame.error:
        raise SystemExit, "Unable to load: " + nome_arquivo
    return image


def carrega_son(nome_arquivo):
    return carrega('sons', nome_arquivo)


def executar_musica(nome_arquivo, volume=0.5, loop=-1):
    nome_arquivo = carrega_son(nome_arquivo)
    try:
        pygame.mixer.music.load(nome_arquivo)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)
    except:
        raise SystemExit, "Unable to load: " + nome_arquivo


def parar_musica():
    pygame.mixer.music.stop()


def obter_som(nome_arquivo, volume=1.0):
    nome_arquivo = carrega_son(nome_arquivo)
    try:
        som = pygame.mixer.Sound(nome_arquivo)
        som.set_volume(volume)
    except:
        raise SystemExit, "Unable to load: " + nome_arquivo
    return som


def carrega_imagem_fatias(w, h, nome_arquivo):
    fatias = []
    imagem_mestre = pygame.image.load(
        carrega('imagens', nome_arquivo)).convert_alpha()
    width_mestre, height_mestre = imagem_mestre.get_size()
    for i in xrange(int(width_mestre / w)):
        # Recorda varias partes da imagem
        fatias.append(imagem_mestre.subsurface((i * w, 0, w, h)))
    return fatias