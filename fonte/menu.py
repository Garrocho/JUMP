import sys
import dados
import motor
import pygame
import webbrowser
from pygame.locals import *


class Menu(object):

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption("JUMP!")
        # size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        # screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        screen = pygame.display.set_mode((1024, 768))
        dados.executar_musica("menu.ogg", 1.5)
        self.som_menu_item = dados.obter_som('menu_item.ogg')
        self.screen = screen
        self.fonte_grande = pygame.font.Font(dados.carrega_fonte("BLADRMF_.TTF"), 150)
        self.fonte_menor = pygame.font.Font(dados.carrega_fonte("GOODTIME.ttf"), 70)
        self.sair = False
        self.cor = [80, 100, 250]
        self.hcor = [255, 255, 255]
        self.funcoes = ["Jogar", "Ranking", "Instrucoes", "Sair"]
        self.posicao_atual = 1

    def loop(self):
        while not self.sair:
            self.atualizar()
            self.desenhar()
        pygame.quit()

    def atualizar(self):
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.posicao_atual += 1
                if e.key == pygame.K_UP:
                    self.posicao_atual -= 1
                if e.key == pygame.K_RETURN:
                    self.executar_funcao()
                if e.type == QUIT:
                    self.posicao_atual = 4
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    self.posicao_atual = 4
        if self.posicao_atual > len(self.funcoes):
            self.posicao_atual = 1
        if self.posicao_atual < 1:
            self.posicao_atual = len(self.funcoes)

    def desenhar(self):
        self.screen.fill((0,0,0))
        ren_maior = self.fonte_grande.render("JUMP!", 1, (255, 255, 255))
        self.pos_central = (self.screen.get_width() - ren_maior.get_rect().width)/2
        self.screen.blit(ren_maior, [self.pos_central, 100])
        
        i = 0
        for funcao in self.funcoes:
            i+=1
            cor_funcao = self.hcor
            if i == self.posicao_atual:
                cor_funcao = self.cor
            ren = self.fonte_menor.render(funcao, 1, cor_funcao)
            self.pos_central = (self.screen.get_width() - ren.get_rect().width)/2
            self.screen.blit(ren, [self.pos_central, (i*70)+300])

        pygame.display.flip()
    
    def executar_funcao(self):
        if self.posicao_atual == 1:
            jogo = motor.Jogo(self.screen)
            jogo.loop()
        elif self.posicao_atual == 2:
            webbrowser.open('http://127.0.0.1:8000', new=0, autoraise=True)
        elif self.posicao_atual == 3:
            pass
        else:
            self.sair = True
