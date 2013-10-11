import sys
import media
import pygame
from pygame.locals import *





class NFMenu:

    def __init__(self, *vetor_funcoes_menu):

        self.vetor_funcoes_menu = vetor_funcoes_menu
        self.som_menu_item = media.obter_som('menu_item.wav')
        self.hcolor = (255, 0, 0)
        self.fonte = pygame.font.Font(media.carrega_fonte("GOODTIME.ttf"), 50)
        self.posicao_atual = 0
        self.width = 1
        self.color = [255, 255, 255]
        self.hcolor = [150, 50, 100]
        self.height = len(self.vetor_funcoes_menu)*self.fonte.get_height()
        for funcao in self.vetor_funcoes_menu:
            texto = funcao[0]
            ren = self.fonte.render(texto, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()
        self.x = 350-(self.width/2)
        self.y = 450-(self.height/2)

    def draw(self, surface):
        i=0
        for funcao in self.vetor_funcoes_menu:
            if i==self.posicao_atual:
                clr = self.hcolor
            else:
                clr = self.color
            texto = funcao[0]
            ren = self.fonte.render(texto, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, ((self.x+self.width/2) - ren.get_width()/2, self.y + i*(self.fonte.get_height()+4)))
            i+=1
            
    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.posicao_atual += 1
                    self.som_menu_item.play()
                if e.key == pygame.K_UP:
                    self.posicao_atual -= 1
                    self.som_menu_item.play()
                if e.key == pygame.K_RETURN:
                    self.vetor_funcoes_menu[self.posicao_atual][1]()
                if e.type == QUIT:
                    sys.exit()
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    sys.exit()
        if self.posicao_atual > len(self.vetor_funcoes_menu)-1:
            self.posicao_atual = 0
        if self.posicao_atual < 0:
            self.posicao_atual = len(self.vetor_funcoes_menu)-1