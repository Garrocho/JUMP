import os
import json
import pygame
import requests
import re
import GeoIP
from os.path import join as join_path


dados_py = os.path.abspath(os.path.dirname(__file__))
dados_dir = os.path.normpath(join_path(dados_py, '..', 'dados'))
ranking_dir = os.path.normpath(join_path(dados_py, '..', 'ranking'))


endereco_arquivos = dict(
    fontes=join_path(dados_dir, 'fontes'),
    imagens=join_path(dados_dir, 'imagens'),
    sons=join_path(dados_dir, 'sons'),
    fases=join_path(dados_dir, 'fases'),
    arquivos=join_path(dados_dir, 'arquivos'),
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


def carrega_arquivo(nome_arquivo):
    return open(endereco_arquivo('arquivos', nome_arquivo))


def carrega_imagem_menu(nome_arquivo):
    nome_arquivo = carrega('imagens', nome_arquivo)
    try:
        image = pygame.image.load(nome_arquivo).convert_alpha()
    except pygame.error:
        raise SystemExit, "Nao Conseguiu Carregar: " + nome_arquivo
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
        raise SystemExit, "Nao Conseguiu Carregar: " + nome_arquivo


def parar_musica():
    pygame.mixer.music.stop()


def obter_som(nome_arquivo, volume=3.0):
    nome_arquivo = carrega_son(nome_arquivo)
    som = pygame.mixer.Sound(nome_arquivo)
    som.set_volume(volume)
    return som


def carrega_imagem_fatias(w, h, nome_arquivo):
    imagens = []
    master_image = pygame.image.load(carrega('imagens', nome_arquivo)).convert_alpha()
    mestre_w, mestre_h = master_image.get_size()
    colunas = mestre_w / w
    linhas = mestre_h / h
    for i in xrange (linhas):
        for j in xrange (colunas):
            pequeno_sprite = master_image.subsurface((j*w,i*h,w,h))
            imagens.append(pequeno_sprite)
    return imagens


def carrega_mapa(posicao):
    try:
        fase = carrega_fase('fase.json').read()
        fase = json.loads(fase)
        return fase[posicao].split(':')
    except:
        return None

def obter_localizacao():
    # obtem as coordenadas do jogador a partir do ip da maquina
    geolocalizacao = GeoIP.open("/usr/share/GeoIP/GeoLiteCity.dat",GeoIP.GEOIP_STANDARD)
    ip_externo = str(re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' ,requests.get("http://www.telize.com/ip").text)[0])
    dados = geolocalizacao.record_by_addr(ip_externo)
    return dados.get('city')

def add_jogador_ranking(nome, distancia, moedas):
    arq_ranking = open(endereco_arquivo('arquivos', 'ranking.json')).read()
    cidade = obter_localizacao()
    if len(arq_ranking) > 10:
        json_ranking = json.loads(arq_ranking)
        json_ranking.append({'nome': nome, 'distancia': str(distancia), 'moedas' : str(moedas), 'cidade' : str(cidade)})
        json_ranking = json.dumps(json_ranking)
    else:
        json_ranking = json.dumps([{'nome': nome, 'distancia': str(distancia), 'moedas' : str(moedas), 'cidade' : str(cidade)}])
    arq_ranking = open(endereco_arquivo('arquivos', 'ranking.json'), 'w')
    arq_ranking.write(json_ranking)
    arq_ranking.close()


def obter_ranking():
    requisicao = requests.open()
    a = re.findall(r'<td>(.[0-9]{2}\.[0-9]{4,6})\,.(.[0-9]{2}\.[0-9]{4,6})', r.text)
    arq_ranking = open(endereco_arquivo('arquivos', 'ranking.json')).read()
    if len(arq_ranking) < 7:
        return None
    else:
        arq_json = json.loads(arq_ranking)
        arq_json = sorted(arq_json, cmp=comparacao)
        arq_json.reverse()
        return arq_json

def comparacao(x, y):
    return int(x['distancia']) - int(y['distancia'])
