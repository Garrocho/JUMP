import sys
import dados
import motor
import pygame
from pygame.locals import *


def novo_jogo(screen):
    jogo = motor.Jogo(screen)
    jogo.loop()


def instrucoes(screen):
    pass


class Menu(object):

    def __init__(self, screen):
        dados.executar_musica("menu.ogg", 0.8)
        self.screen = screen
        self.menu = NFMenu(["Novo Jogo", lambda: novo_jogo(screen)], ["Instrucoes", lambda: instrucoes(screen)],  ["Sair", sys.exit])
        self.clock = pygame.time.Clock()
        events = pygame.event.get()
        self.menu.atualizar(events)
        self.menu.desenhar(self.screen)
        #self.bg = dados.carrega_imagem_menu('menu_background.jpg')
        self.fonte_grande = pygame.font.Font(dados.carrega_fonte("BLADRMF_.TTF"), 120)
        self.fonte_menor = pygame.font.Font(dados.carrega_fonte("GOODTIME.ttf"), 30)
        self.run = True

    def loop(self):
        while self.run:
            self.clock.tick(40)
            events = pygame.event.get()
            self.menu.atualizar(events)
            self.screen.fill((0,0,0))
            #self.screen.blit(self.bg, (0, 0))
            ren_maior = self.fonte_grande.render("JUMP!", 1, (255, 255, 255))
            self.posicao_x = self.screen.get_width()/2 - ren_maior.get_rect().width/2
            self.screen.blit(ren_maior, [self.posicao_x, 100])
            self.menu.desenhar(self.screen)
            pygame.display.flip()


class NFMenu:

    def __init__(self, *vetor_funcoes_menu):

        self.vetor_funcoes_menu = vetor_funcoes_menu
        self.som_menu_item = dados.obter_som('menu_item.ogg')
        self.hcolor = (255, 0, 0)
        self.fonte = pygame.font.Font(dados.carrega_fonte("GOODTIME.ttf"), 50)
        self.posicao_atual = 0
        self.width = 1
        self.color = [255, 255, 255]
        self.hcolor = [80, 100, 250]
        self.height = len(self.vetor_funcoes_menu) * self.fonte.get_height()
        for funcao in self.vetor_funcoes_menu:
            texto = funcao[0]
            ren = self.fonte.render(texto, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()
        self.x = 520 - (self.width / 2)
        self.y = 400 - (self.height / 2)

    def desenhar(self, surface):
        i = 0
        for funcao in self.vetor_funcoes_menu:
            if i == self.posicao_atual:
                clr = self.hcolor
            else:
                clr = self.color
            texto = funcao[0]
            ren = self.fonte.render(texto, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(
                ren, ((self.x + self.width / 2) - ren.get_width() / 2, self.y + i * (self.fonte.get_height() + 4)))
            i += 1

    def atualizar(self, events):
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
        if self.posicao_atual > len(self.vetor_funcoes_menu) - 1:
            self.posicao_atual = 0
        if self.posicao_atual < 0:
            self.posicao_atual = len(self.vetor_funcoes_menu) - 1
