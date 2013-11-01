import sys
import dados
import pygame
from pygame.locals import *


class Editor:
	ALFABETO = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
	nome = ""

	def __init__(self, screen, distancia, moedas):
		self.screen = screen
		self.distancia = distancia
		self.moedas = moedas
		self.fonte_grande = pygame.font.Font(dados.carrega_fonte("BLADRMF_.TTF"), 70)
		self.fonte_menor = pygame.font.Font(dados.carrega_fonte("GOODTIME.ttf"), 30)

	def tratador_eventos(self):
		for evento in pygame.event.get():
			tipo = evento.type
			if tipo == KEYDOWN:
				chave = evento.key-97
				if chave < len(self.ALFABETO) and chave >= 0:
					if len(self.nome) < 10:
						self.nome += self.ALFABETO[chave]
				elif chave == -89:
					self.nome = self.nome[:-1]
				elif chave == -70:
					if len(self.nome) == 0:
						self.nome = "Desconhecido"
					self.sair = True
				elif chave == -65:
					self.nome += " "
				elif chave == -84:
					if len(self.nome) > 2:
						self.sair = True

	def desenhar(self):
		ren_maior = self.fonte_grande.render("Fim de Jogo!", 1, (255, 255, 255))
		ren_pontua = self.fonte_menor.render("Distancia Percorrida: ", 1, (80, 100, 250))
		ren_pontua2 = self.fonte_menor.render("% 4d" % self.distancia, 1, (255, 255, 255))
		ren_moedas = self.fonte_menor.render("Moedas Conquistadas: ", 1, (80, 100, 250))
		ren_moedas2 = self.fonte_menor.render("% 4d" % self.moedas, 1, (255, 255, 255))
		text_rect = ren_maior.get_rect()
		text_x = (self.screen.get_width() - text_rect.width)/2
		text_y = self.screen.get_height()/5 - text_rect.height/5
		self.screen.fill((0,0,0))
		self.screen.blit(ren_maior, [text_x, text_y])
		self.screen.blit(ren_pontua, [text_x, text_y+150])
		self.screen.blit(ren_pontua2, [text_x+ren_pontua.get_rect().width, text_y+150])
		self.screen.blit(ren_moedas, [text_x, text_y+200])
		self.screen.blit(ren_moedas2, [text_x+ren_moedas.get_rect().width, text_y+200])
		if len(self.nome) > 2:
			ren_menor = self.fonte_menor.render("Pressione Enter Para Continuar!", 1, (255, 255, 255))
			self.screen.blit(ren_menor, [(self.screen.get_width() - ren_menor.get_rect().width)/2, text_y+500])

		rend = self.fonte_menor.render("Entre com Seu Nome:  ", 1, (80, 100, 250))
		rend2 = self.fonte_menor.render(self.nome, 1, (255, 255, 255))
		self.screen.blit(rend, [text_x, text_y+350])
		self.screen.blit(rend2, [text_x+rend.get_rect().width, text_y+350])
		pygame.display.flip()

	def loop(self):
		self.sair = False
		while not self.sair:
			self.tratador_eventos()
			self.desenhar()
		return self.nome