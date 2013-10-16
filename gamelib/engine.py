import media
import pygame
from pygame.locals import *


class Game:
    screen      = None
    screen_size = None
    run         = True
    
    def __init__( self, screen ):
        #media.executar_musica("musica.ogg", 0.75)
        self.screen      = screen
        self.screen_size = self.screen.get_size()
        self.carrega_dados()

    def carrega_dados( self ):
        self.bg_carr_jogo = media.carrega_imagem_menu('menu_background.jpg')
        self.fonte = pygame.font.Font(media.carrega_fonte("GOODTIME.ttf"), 30)
        ren = self.fonte.render("Carregando Jogo...", 1, (255, 255, 255))

        # Desenhando na Tela Temporariamente...
        self.screen.blit(self.bg_carr_jogo, (0, 0))
        self.screen.blit(ren, (40, self.screen_size[1]-50))

        # carregando dados
        self.bg_game = media.carrega_imagem_menu('jogo_background_1.jpg')
        #self.img_louco = media.carrega_imagem_menu('louco.png')

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
                elif k == K_LCTRL or k == K_RCTRL:
                    print 'controle'
                elif k == K_UP:
                    print 'pro alto'
                elif k == K_DOWN:
                    print 'pra baixo'

    def atualizar_atores(self):
        #self.ator.update()
        pass

    def desenhar_atores(self):
        self.screen.blit(self.bg_game, (0, 0))

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