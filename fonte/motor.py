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
            "jogador": dados.carrega_imagem_fatias(160, 100, 'cachorro.png'),
            "fundo": dados.carrega_imagem_menu('jogo_background_1.png'),
            "moedas": dados.carrega_imagem_fatias(44, 40, 'moedas.png')
        }

        # Carregando Atores
        pos_jogador = [self.screen_size[0] / 2, self.screen_size[1] - 100]
        self.pos_moeda = [self.screen_size[0] - 100 / 2, self.screen_size[1] - 100]
        self.jogador = atores.Jogador(imagem=self.lista_imagens['jogador'], posicao=pos_jogador)
        self.status_moedas = atores.StatusMoedas(self.jogador)

        # Lista de Atores
        self.lista_atores = {
            "jogador": pygame.sprite.RenderPlain(self.jogador),
            "moedas": pygame.sprite.RenderPlain(),
        }

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
                    self.jogador.pular()

    def atualizar_atores(self):
        for ator in self.lista_atores.values():
            ator.update()
        self.status_moedas.update()

    def desenhar_atores(self):
        self.screen.blit(self.lista_imagens['fundo'], (0, 0))

        for ator in self.lista_atores.values():
            ator.draw(self.screen)
        self.status_moedas.draw(self.screen)

    def checar_colisao_de_um_ator(self, ator, lista, matar):
        acertos = pygame.sprite.spritecollide(ator, lista, matar)
        if acertos:
            self.jogador.atingido()
        return acertos

    def checar_colisoes(self):
        qtde_moedas = self.checar_colisao_de_um_ator(self.jogador, self.lista_atores["moedas"], 1)
        self.jogador.moedas += len(qtde_moedas)

    def administrar(self):
        if self.aguardar:
            self.aguardar_tmp = self.aguardar_tmp - 1
            if self.aguardar_tmp == 0:
                self.aguardar = False
        else:
            fase = carrega_fase(self.pos_fase)
            self.pos_fase = self.pos_fase + 1
            if fase == None:
                pass
            elif fase[0] == 'A':
                self.aguardar = True
                self.aguardar_tmp = int(fase[1])
            elif fase[0] == 'M':
                pos = [self.pos_moeda[0], self.pos_moeda[1]-random.randint(0, 250)]
                nova_moeda = atores.Moeda(imagem=self.lista_imagens['moedas'], posicao=pos, velocidade=5)
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