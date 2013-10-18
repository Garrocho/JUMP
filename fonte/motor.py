import json
import dados
import pygame
import atores
from pygame.locals import *


class Jogo:
    screen      = None
    screen_size = None
    run         = True
    aguardar    = False
    aguardar_tmp = 0
    pos_fase    = 0
    
    def __init__(self, screen):
        self.screen      = screen
        self.screen_size = self.screen.get_size()
        self.carrega_dados()

    def carrega_dados(self):
        # carregando dados
        #dados.executar_musica("musica_inicio_do_jogo.ogg", 0.75)
        self.img_fundo   = dados.carrega_imagem_menu('jogo_background_1.jpg')
        self.img_jogador = dados.carrega_imagem_fatias(160, 100, 'cachorro.png')
        self.img_fogo    = dados.carrega_imagem_fatias(105, 93, 'fogo.png')

        # Carregando Atores
        pos_jogador  = [self.screen_size[ 0 ] / 2, self.screen_size[ 1 ] - 100]
        self.pos_fogo = [self.screen_size[ 0 ]-100 / 2, self.screen_size[ 1 ] - 100]
        self.jogador = atores.Jogador(imagem=self.img_jogador, posicao=pos_jogador)
        fogo = atores.Fogo(imagem=self.img_fogo, posicao=self.pos_fogo)

        # Lista de Atores
        self.lista_atores = {
            "jogador" : pygame.sprite.RenderPlain(self.jogador),
            "fogo"    : pygame.sprite.RenderPlain(fogo)
        }

    def tratador_eventos(self):
        for event in pygame.event.get():
            t = event.type
            if t in (KEYDOWN, KEYUP):
                k = event.key
        
            if t == QUIT:
                self.run = False

            elif t == KEYDOWN:
                if   k == K_ESCAPE:
                    self.run = False
                elif k == K_SPACE and not self.jogador.pulando:
                    self.jogador.pular()

    def atualizar_atores(self):
        for ator in self.lista_atores.values():
            ator.update()

    def desenhar_atores(self):
        self.screen.blit(self.img_fundo, (0, 0))

        for ator in self.lista_atores.values():
            ator.draw(self.screen)

    def checar_colisao_de_um_ator(self, ator, lista):
        if pygame.sprite.spritecollide(ator, lista, 0):
            self.jogador.atingido()

    def checar_colisoes(self):
        self.checar_colisao_de_um_ator(self.jogador, self.lista_atores["fogo"])

    def administrar(self):
        if self.aguardar:
            self.aguardar_tmp = self.aguardar_tmp-1
            if self.aguardar_tmp == 0:
                self.aguardar = False
        else:
            fase = carrega_fase(self.pos_fase)
            self.pos_fase = self.pos_fase+1
            if fase == None:
                pass
            elif fase[0] == 'AGUARDE':
                self.aguardar = True
                self.aguardar_tmp = int(fase[1])
            else:
                novo_fogo = atores.Fogo(imagem=self.img_fogo, posicao=self.pos_fogo)
                self.lista_atores["fogo"].add(novo_fogo)

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
