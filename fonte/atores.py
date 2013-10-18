import pygame
from pygame.locals import *


class Jogador(pygame.sprite.Sprite):

    def __init__(self, imagem, posicao):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagem[0]
        self.fatias = imagem
        self.rect = self.image.get_rect()
        self.rect.center = (posicao)
        self.pulando = False
        self.fases_pulo = 0
        self.tempo_fatia = 1

    def pular(self):
        self.fases_pulo = 50
        self.pulando = True
        self.image = self.fatias[1]

    def atingido(self):
        print 'atingido'

    def update(self):
        # Trata os pulos do jogador
        if self.pulando:
            if self.tempo_fatia == 0:
                self.tempo_fatia = 1
                if self.fases_pulo >= 25:
                    self.rect.center = (
                        self.rect.center[0], self.rect.center[1] - 10)
                    self.fases_pulo = self.fases_pulo - 1
                elif self.fases_pulo >= -1:
                    self.fases_pulo = self.fases_pulo - 1
                    self.rect.center = (
                        self.rect.center[0], self.rect.center[1] + 10)
                else:
                    self.pulando = False
                    self.fases_pulo = 0
                    self.image = self.fatias[0]
            else:
                self.tempo_fatia = self.tempo_fatia - 1


class Fogo(pygame.sprite.Sprite):

    def __init__(self, imagem, posicao, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagem[0]
        self.fatias = imagem
        self.rect = self.image.get_rect()
        self.rect.center = (posicao)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.fatia_atual = 0
        self.soma = True
        self.fatia_tam = len(self.fatias) - 1
        self.tempo_fatia = velocidade
        self.velo = velocidade

    def update(self):
        if self.tempo_fatia == 0:
            if self.fatia_atual < self.fatia_tam and self.soma is True:
                self.tempo_fatia = self.velo
                self.fatia_atual = self.fatia_atual + 1
                if self.fatia_atual == self.fatia_tam:
                    self.soma = False
                    self.tempo_fatia = self.velo
            else:
                self.tempo_fatia = self.velo
                self.fatia_atual = self.fatia_atual - 1
                if self.fatia_atual == 0:
                    self.soma = True
                    self.tempo_fatia = self.velo
            self.image = self.fatias[self.fatia_atual]
        else:
            self.tempo_fatia = self.tempo_fatia - 1

        self.rect.center = (self.rect.center[0] - 3, self.rect.center[1])

        if self.rect.left > self.area.right or self.rect.top > self.area.bottom or self.rect.right < 0:
            print 'to morto'
            self.kill()
        if self.rect.bottom < -40:
            print 'to morto'
            self.kill()