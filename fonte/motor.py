import json
import dados
import pygame
import atores
import random
import editor
from pygame.locals import *


class Jogo:
    screen = None
    screen_size = None
    sair = False
    aguardar = False
    aguardar_tmp = 0
    pos_fase = 0
    game_over = False

    def __init__(self, screen):
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.relogio = pygame.time.Clock()
        self.carrega_dados()

    def carrega_dados(self):
        dados.parar_musica()
        dados.executar_musica("fase_1.wav", 0.2)

        # Lista de Imagens
        self.lista_imagens = {
            "jogador": dados.carrega_imagem_fatias(400, 200, 'gato.png'),
            "fundo_nuvem": dados.carrega_imagem_menu('background_nuvem.png'),
            "fundo_caminho": dados.carrega_imagem_menu('background_caminho.png'),
            "fundo_montanha": dados.carrega_imagem_menu('background_montanha.png'),
            "moedas": dados.carrega_imagem_fatias(44, 40, 'moedas.png'),
            "buraco": dados.carrega_imagem_menu('buraco.png'),
            "aux_buraco": dados.carrega_imagem_menu('aux_buraco.png')
        }

        # Lista de Sons
        self.lista_sons = {
            "moeda": dados.obter_som('moeda.wav'),
            "game_over": dados.obter_som('game_over.ogg'),
            "pulo": dados.obter_som('pulo.ogg', 0.5),
        }

        # Carregando Atores
        pos_jogador = [self.screen_size[0] / 4 , self.screen_size[1] - 170]
        self.pos_moeda = [self.screen_size[0], self.screen_size[1] - 170]
        self.pos_buraco = [self.screen_size[0]+120, self.screen_size[1] - 46]
        self.jogador = atores.Jogador(imagem=self.lista_imagens['jogador'], posicao=pos_jogador, som=self.lista_sons["pulo"])

        # Lista de Atores
        self.lista_atores = [
            atores.Fundo(imagem=self.lista_imagens['fundo_nuvem'], tam_px=0.6),
            atores.Fundo(imagem=self.lista_imagens['fundo_montanha'], tam_px=2),
            atores.Fundo(imagem=self.lista_imagens['fundo_caminho'], tam_px=12),
            pygame.sprite.RenderPlain(),
            pygame.sprite.RenderPlain(),
            pygame.sprite.RenderPlain(),
            pygame.sprite.RenderPlain(self.jogador),
            atores.Status(jogador=self.jogador, identificador="Distancia"),
            atores.Status(jogador=self.jogador, posicao=(5,35), identificador="Moedas")
        ]

    def tratador_eventos(self):
        for evento in pygame.event.get():
            tipo = evento.type
            if tipo in (KEYDOWN, KEYUP):
                chave = evento.key

            if tipo == QUIT:
                self.sair = False

            elif tipo == KEYDOWN:
                if chave == K_ESCAPE:
                    self.sair = True
                elif chave == K_SPACE and not self.jogador.pulando and not self.game_over:
                    self.jogador.pular()
        if self.sair == True:
            dados.parar_musica()
            dados.executar_musica("menu.ogg", 1.5)

    def atualizar_atores(self):
        for ator in self.lista_atores:
            ator.update()

    def desenhar_atores(self):
        for ator in self.lista_atores:
            ator.draw(self.screen)

    def checar_colisao_de_um_ator(self, ator, lista, matar):
        atores_atingido = pygame.sprite.spritecollide(ator, lista, matar)
        for ator in atores_atingido:
            ator.atingido()
        return len(atores_atingido)

    def checar_colisoes(self):
        self.jogador.status["Moedas"] += self.checar_colisao_de_um_ator(self.jogador, self.lista_atores[3], 1)

        if self.checar_colisao_de_um_ator(self.jogador, self.lista_atores[4], 0):
            self.jogador.kill()
            self.sair = True
            dados.parar_musica()
            self.lista_sons["game_over"].play()
            ed = editor.Editor(self.screen, self.jogador.status["Distancia"], self.jogador.status["Moedas"])
            nome = ed.loop()
            dados.add_jogador_ranking(nome, self.jogador.status["Distancia"], self.jogador.status["Moedas"])

    def administrar(self):
        if pygame.time.get_ticks()%200:
            self.jogador.status["Distancia"] += 1

        if self.aguardar:
            self.aguardar_tmp = self.aguardar_tmp - 1
            if self.aguardar_tmp == 0:
                self.aguardar = False
        else:
            fase = dados.carrega_mapa(self.pos_fase)
            self.pos_fase = self.pos_fase + 1
            if fase == None:
                self.pos_fase = 0
            elif fase[0] == 'A':
                self.aguardar = True
                self.aguardar_tmp = int(fase[1])
            elif fase[0] == 'M':
                pos = [self.pos_moeda[0], self.pos_moeda[1]-random.randint(0, 450)]
                nova_moeda = atores.AtorComEfeito(imagem=self.lista_imagens['moedas'], posicao=pos, velocidade=15, som=self.lista_sons["moeda"])
                self.lista_atores[3].add(nova_moeda)
            elif fase[0] == 'B':
                novo_buraco = atores.AtorSemEfeito(imagem=self.lista_imagens['buraco'], posicao=self.pos_buraco, velocidade=15)
                self.lista_atores[4].add(novo_buraco)

                pos_aux_buraco = [self.pos_buraco[0]-self.lista_imagens['aux_buraco'].get_size()[0]-40, self.pos_buraco[1]]
                aux_buraco = atores.AtorSemEfeito(imagem=self.lista_imagens['aux_buraco'], posicao=pos_aux_buraco, velocidade=15)
                self.lista_atores[5].add(aux_buraco)

                pos_aux_buraco = [self.pos_buraco[0]+self.lista_imagens['buraco'].get_size()[0], self.pos_buraco[1]]
                pos_aux_buraco[0]-=40
                aux_buraco = atores.AtorSemEfeito(imagem=self.lista_imagens['aux_buraco'], posicao=pos_aux_buraco, velocidade=15)
                self.lista_atores[5].add(aux_buraco)

    def loop(self):

        while not self.sair:

            # Trata os eventos de entrada.
            self.tratador_eventos()

            # Atualiza Elementos.
            self.atualizar_atores()

            # Checa se os Atores se Chocaram.
            self.checar_colisoes()

            # Faca a manutencao do jogo, como criar obstaculos, etc.
            self.administrar()

            # Desenhe os elementos do jogo.
            self.desenhar_atores()

            # Por fim atualize o screen do jogo.
            pygame.display.flip()

            # Pausa
            self.relogio.tick(30)