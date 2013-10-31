import sys
import dados
import pygame
from pygame.locals import *


class Editor:
	ALFABETO = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
	nome = ""

	def __init__(self, screen):
		self.screen = screen
		self.fonte_grande = pygame.font.Font(dados.carrega_fonte("BLADRMF_.TTF"), 120)
        self.fonte_menor = pygame.font.Font(dados.carrega_fonte("GOODTIME.ttf"), 25)

	def tratador_eventos(self):
		for evento in pygame.event.get():
			tipo = evento.type
			if tipo == KEYDOWN:
				chave = evento.key-97
				if chave < len(self.ALFABETO) and chave >= 0:
					self.nome += self.ALFABETO[chave]
				elif chave == -89:
					self.nome = self.nome[:-1]
				elif chave == -70:
					self.sair = True
				elif chave == -65:
					self.nome += " "
				elif chave == -84:
					self.sair = False

	def desenhar(self):
		ren_maior = self.fonte_grande.render("Game Over", 1, (255, 255, 255))
		ren_menor = self.fonte_menor.render("Pressione ESC Para Voltar ao Menu do Jogo!", 1, (80, 100, 250))
		ren_pontua = self.fonte_menor.render("Distancia Percorrida: % 4d" % self.jogador.status["Distancia"], 1, (50, 100, 50))
		ren_moedas = self.fonte_menor.render("Moedas Conquistadas: % 4d" % self.jogador.status["Moedas"], 1, (50, 100, 50))
		text_rect = ren_maior.get_rect()
		text_x = self.screen.get_width()/2 - text_rect.width/2
		text_y = self.screen.get_height()/5 - text_rect.height/5
		self.screen.fill((0,0,0))
		self.screen.blit(ren_maior, [text_x, text_y])
		self.screen.blit(ren_pontua, [text_x, text_y+150])
		self.screen.blit(ren_moedas, [text_x, text_y+200])
		self.screen.blit(ren_menor, [text_x+10, text_y+500])
		pygame.display.flip()

		rend = self.fonte_menor.render("Entre com Seu Nome: " + self.nome, 1, (80, 100, 10))
		self.screen.fill((0,0,0))
		self.screen.blit(rend, [text_x, text_y+100])
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
	pygame.quit()
