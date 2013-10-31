import sys
import dados
import pygame
from pygame.locals import *


class Editor:
	ALFABETO = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
	nome = "Entre com Seu Nome: "

	def __init__(self, screen):
		self.screen = screen
		self.fonte = pygame.font.Font(dados.carrega_fonte("GOODTIME.ttf"), 25)

	def tratador_eventos(self):
		for evento in pygame.event.get():
			tipo = evento.type
			if tipo == KEYDOWN:
				chave = evento.key-97
				if chave == -70:
					self.sair = True
				elif chave < len(self.ALFABETO) and chave >= 0:
					self.nome+= self.ALFABETO[chave]
				elif chave == -89:
					#volta
				elif chave == -84:
					#concluido

	def desenhar(self):
		rend = self.fonte.render(self.nome, 1, (80, 100, 250))
		self.screen.fill((0,0,0))
		self.screen.blit(rend, [10, 10])
		pygame.display.flip()

	def loop(self):
		self.sair = False
		while not self.sair:
			self.tratador_eventos()
			self.desenhar()


if __name__ == '__main__':
	pygame.init()
	pygame.mouse.set_visible(0)
	pygame.display.set_caption("Editor")
	screen = pygame.display.set_mode((900, 400))
	editor = Editor(screen)
	editor.loop()
