import pygame
from pygame.locals import *


class Jogador(pygame.sprite.Sprite):

    def __init__(self, imagem, posicao):
    	pygame.sprite.Sprite.__init__(self)
        self.image 		 = imagem
        self.rect  		 = self.image.get_rect()
        self.rect.center = (posicao)
        self.pulando  	 = False
        self.fases_pulo	 = 0

    def pular(self):
    	self.fases_pulo	 = 30
    	self.pulando 	 = True

    def update(self):
    	if self.pulando:
    		if self.fases_pulo >= 15:
    			self.rect.center = (self.rect.center[0], self.rect.center[1] - 10)
    			self.fases_pulo = self.fases_pulo-1
    		elif self.fases_pulo >= -1:
    			self.fases_pulo = self.fases_pulo-1
    			self.rect.center = (self.rect.center[0], self.rect.center[1] + 10)
    		else:
    			self.pulando = False
    			self.fases_pulo	 = 0