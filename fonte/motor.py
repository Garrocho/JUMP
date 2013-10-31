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
    game_over = False

    def __init__(self, screen):
        self.screen = screen
        self.screen_size = self.screen.get_size()
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
            "buraco": dados.carrega_imagem_menu('buraco.png')
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
            atores.Fundo(imagem=self.lista_imagens['fundo_nuvem'], tam_px=0.2),
            atores.Fundo(imagem=self.lista_imagens['fundo_montanha'], tam_px=0.5),
            atores.Fundo(imagem=self.lista_imagens['fundo_caminho'], tam_px=5),
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
                self.run = False

            elif tipo == KEYDOWN:
                if chave == K_ESCAPE:
                    self.run = False
                elif chave == K_SPACE and not self.jogador.pulando and not self.game_over:
                    self.jogador.pular()
        if self.run == False:
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
            self.game_over = True
            dados.parar_musica()
            self.lista_sons["game_over"].play()
            dados.add_jogador_ranking(str(self.jogador.status["Distancia"]), self.jogador.status["Distancia"])

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
                nova_moeda = atores.AtorComEfeito(imagem=self.lista_imagens['moedas'], posicao=pos, velocidade=5, som=self.lista_sons["moeda"])
                self.lista_atores[3].add(nova_moeda)
            elif fase[0] == 'B':
                novo_buraco = atores.AtorSemEfeito(imagem=self.lista_imagens['buraco'], posicao=self.pos_buraco, velocidade=5, som=self.lista_sons["moeda"])
                self.lista_atores[4].add(novo_buraco)

    def draw_game_over(self):
        self.fonte_grande = pygame.font.Font(dados.carrega_fonte("BLADRMF_.TTF"), 120)
        self.fonte_menor = pygame.font.Font(dados.carrega_fonte("GOODTIME.ttf"), 25)
        ren_maior = self.fonte_grande.render("Game Over", 1, (255, 255, 255))
        ren_menor = self.fonte_menor.render("Pressione ESC Para Voltar ao Menu do Jogo!", 1, (80, 100, 250))
        ren_pontua = self.fonte_menor.render("Distancia Percorrida: % 4d" % self.jogador.status["Distancia"], 1, (50, 100, 50))
        ren_moedas = self.fonte_menor.render("Moedas Conquistadas: % 4d" % self.jogador.status["Moedas"], 1, (50, 100, 50))
        text_rect = ren_maior.get_rect()
        text_x = self.screen.get_width()/2 - text_rect.width/2
        text_y = self.screen.get_height()/5 - text_rect.height/5
        self.screen.fill((0,0,0))
        self.screen.blit(ren_maior, [text_x, text_y])
        self.screen.blit(ren_pontua, [text_x, text_y+150])
        self.screen.blit(ren_moedas, [text_x, text_y+200])
        self.screen.blit(ren_menor, [text_x+10, text_y+500])
        pygame.display.flip()

    def loop(self):

        while self.run:

            # Trata os eventos de entrada.
            self.tratador_eventos()

            if self.game_over:
                self.draw_game_over()
            else:

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