import json
import dados
import pygame
import atores
import random
from pygame.locals import *


class Jogo:
    screen = None
    screen_size = None
    run = True
    aguardar = False
    aguardar_tmp = 0
    pos_fase = 0

    def __init__(self, screen):
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.carrega_dados()

    def carrega_dados(self):
        # Lista de Imagens
        self.lista_imagens = {
            "jogador": dados.carrega_imagem_fatias(400, 200, 'gato.png'),
            "fundo_nuvem": dados.carrega_imagem_menu('background_nuvem.png'),
            "fundo_caminho": dados.carrega_imagem_menu('background_caminho.png'),
            "fundo_montanha": dados.carrega_imagem_menu('background_montanha.png'),
            "fundo_arvores": dados.carrega_imagem_menu('background_arvore.png'),
            "fundo_mato": dados.carrega_imagem_menu('background_mato.png'),
            "moedas": dados.carrega_imagem_fatias(44, 40, 'moedas.png')
        }

        # Lista de Sons
        self.lista_sons = {
            "moeda": dados.obter_som('moeda.wav'),
            "pulo": dados.obter_som('pulo.wav', 0.5),
        }

        # Carregando Atores
        pos_jogador = [self.screen_size[0] / 3, self.screen_size[1] - 100]
        self.pos_moeda = [self.screen_size[0], self.screen_size[1] - 100]
        self.jogador = atores.Jogador(imagem=self.lista_imagens['jogador'], posicao=pos_jogador)
        self.status_moedas = atores.StatusMoedas(self.jogador)

        # Lista de Atores
        self.lista_atores = {
            "jogador": pygame.sprite.RenderPlain(self.jogador),
            "moedas": pygame.sprite.RenderPlain(),
        }

        # Lista de Fundos
        self.lista_fundos = [
            atores.Fundo(imagem=self.lista_imagens['fundo_nuvem'], tam_px=0.2),
            atores.Fundo(imagem=self.lista_imagens['fundo_montanha'], tam_px=0.5),
            atores.Fundo(imagem=self.lista_imagens['fundo_arvores'], tam_px=2),
            atores.Fundo(imagem=self.lista_imagens['fundo_caminho'], tam_px=3)
        ]
        
        self.mato = atores.Fundo(imagem=self.lista_imagens['fundo_mato'], tam_px=6)

    def tratador_eventos(self):
        for evento in pygame.event.get():
            tipo = evento.type
            if tipo in (KEYDOWN, KEYUP):
                chave = evento.key

            if tipo == QUIT:
                self.run = False

            elif tipo == KEYDOWN:
                if chave == K_ESCAPE:
                    self.run = False
                elif chave == K_SPACE and not self.jogador.pulando:
                    self.lista_sons["pulo"].play()
                    self.jogador.pular()

    def atualizar_atores(self):
        self.mato.update()
        for fundo in self.lista_fundos:
            fundo.update()

        for ator in self.lista_atores.values():
            ator.update()

        self.status_moedas.update()

    def desenhar_atores(self):
        for fundo in self.lista_fundos:
            fundo.draw(self.screen)

        for ator in self.lista_atores.values():
            ator.draw(self.screen)

        self.status_moedas.draw(self.screen)
        self.mato.draw(self.screen)

    def checar_colisao_de_um_ator(self, ator, lista, matar):
        acertos = pygame.sprite.spritecollide(ator, lista, matar)
        if acertos:
            self.jogador.atingido()
        return acertos

    def checar_colisoes(self):
        moedas = self.checar_colisao_de_um_ator(self.jogador, self.lista_atores["moedas"], 1)
        if len(moedas) > 0:
            self.lista_sons["moeda"].play()
            
        for i in moedas:
            i.atingido()
        self.jogador.moedas += len(moedas)

    def administrar(self):
        if self.aguardar:
            self.aguardar_tmp = self.aguardar_tmp - 1
            if self.aguardar_tmp == 0:
                self.aguardar = False
        else:
            fase = carrega_fase(self.pos_fase)
            self.pos_fase = self.pos_fase + 1
            if fase == None:
                self.pos_fase = 0
            elif fase[0] == 'A':
                self.aguardar = True
                self.aguardar_tmp = int(fase[1])
            elif fase[0] == 'M':
                pos = [self.pos_moeda[0], self.pos_moeda[1]-random.randint(0, 450)]
                nova_moeda = atores.Moeda(imagem=self.lista_imagens['moedas'], posicao=pos, velocidade=5, som=self.lista_sons["moeda"])
                self.lista_atores['moedas'].add(nova_moeda)

    def loop(self):

        while self.run:

            # Trata os eventos de entrada.
            self.tratador_eventos()

            # Atualiza Elementos.
            self.atualizar_atores()

            # Checa se os Atores se Chocaram.
            self.checar_colisoes()

            # Faca a manutencao do jogo, como criar inimigos, etc.
            self.administrar()

            # Desenhe os elementos do jogo.
            self.desenhar_atores()

            # Por fim atualize o screen do jogo.
            pygame.display.flip()


def carrega_fase(posicao):
    try:
        fase = dados.carrega_fase('fase.json').read()
        fase = json.loads(fase)
        return fase[posicao].split(':')
    except:
        return None
