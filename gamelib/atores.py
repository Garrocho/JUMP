import pygame
from pygame.locals import *


class Jogador(pygame.sprite.Sprite):

    def __init__(self, imagem, posicao):
    	pygame.sprite.Sprite.__init__(self)
        self.image 		 = imagem
        self.rect  		 = self.image.get_rect()
        self.rect.center = (posicao[ 0 ], posicao[ 1 ])

    def pular(self):
    	pass