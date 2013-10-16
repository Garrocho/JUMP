import media
import pygame
import atores
from pygame.locals import *


class Jogo:
    screen      = None
    screen_size = None
    run         = True
    
    def __init__( self, screen ):
        self.screen      = screen
        self.screen_size = self.screen.get_size()
        self.carrega_dados()

    def carrega_dados( self ):
        # carregando dados
        #media.executar_musica("musica_inicio_do_jogo.ogg", 0.75)
        self.bg_game = media.carrega_imagem_menu('jogo_background_1.jpg')
        self.img_louco = media.carrega_imagem_menu('louco.png')

        # Carregando Atores
        posicao      = [ self.screen_size[ 0 ] / 2, self.screen_size[ 1 ] - 200 ]
        self.jogador = atores.Jogador(imagem=self.img_louco, posicao=posicao)

        # Lista de Atores
        self.lista_atores = {
            "jogador" : pygame.sprite.RenderPlain(self.jogador)
        }

    def tratador_eventos( self ):
        for event in pygame.event.get():
            t = event.type
            if t in ( KEYDOWN, KEYUP ):
                k = event.key
        
            if t == QUIT:
                self.run = False

            elif t == KEYDOWN:
                if   k == K_ESCAPE:
                    self.run = False
                elif k == K_UP:
                    self.jogador.pular()

    def atualizar_atores(self):
        for ator in self.lista_atores.values():
            ator.update()

    def desenhar_atores(self):
        self.screen.blit(self.bg_game, (0, 0))

        for ator in self.lista_atores.values():
            ator.draw(self.screen)

    def acao_atores( self ):
        # Verifica se personagem foi atingido por um tiro, se trombou em algum inimigo
        # se atingiu algum alvo. Aumenta a experiencia baseado no numero de acertos, etc
        pass

    def administrar( self ):
        # Fazer inimigos executar alguma acao, modificar level do jogo, etc.
        pass

    def loop( self ):

        while self.run:

            # Trata os eventos de entrada.
            self.tratador_eventos()

            # Atualiza Elementos
            self.atualizar_atores()

            # Faca os atores atuarem
            self.acao_atores()

            # Faca a manutencao do jogo, como criar inimigos, etc.
            self.administrar()
            
            # Desenhe os elementos do jogo.
            self.desenhar_atores()
            
            # Por fim atualize o screen do jogo.
            pygame.display.flip()