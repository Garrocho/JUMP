import sys
import dados
import motor
import atores
import pygame
from pygame.locals import *


class Menu(object):

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption("JUMP!")
        #size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        #screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
        screen = pygame.display.set_mode((1024, 768))
        dados.executar_musica("menu.ogg", 1.5)
        self.som_menu_item = dados.obter_som('menu_item.ogg')
        self.fundo = atores.Fundo(imagem=dados.carrega_imagem_menu('background_nuvem.png'), tam_px=0.2)
        self.screen = screen
        self.fonte_grande = pygame.font.Font(dados.carrega_fonte("BLADRMF_.TTF"), 150)
        self.fonte_menor = pygame.font.Font(dados.carrega_fonte("GOODTIME.ttf"), 70)
        self.sair = False
        self.cor = [34, 139, 34]
        self.hcor = [0, 0, 0]
        self.funcoes = ["Jogar", "Ranking", "Instrucoes", "Configuracoes", "Sair"]
        self.posicao_atual = 1

    def loop(self):
        while not self.sair:
            self.atualizar()
            self.desenhar()
        pygame.quit()

    def atualizar(self):
        self.fundo.update()
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                self.som_menu_item.play()
                if e.key == pygame.K_DOWN:
                    self.posicao_atual += 1
                if e.key == pygame.K_UP:
                    self.posicao_atual -= 1
                if e.key == pygame.K_RETURN:
                    self.executar_funcao()
                if e.type == QUIT:
                    self.posicao_atual = 5
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    self.posicao_atual = 5
        if self.posicao_atual > len(self.funcoes):
            self.posicao_atual = 1
        if self.posicao_atual < 1:
            self.posicao_atual = len(self.funcoes)

    def desenhar(self):
        self.fundo.draw(self.screen)
        ren_maior = self.fonte_grande.render("JUMP!", 1, self.hcor)
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
            self.ranking()
        elif self.posicao_atual == 3:
            pass
        elif self.posicao_atual == 4:
            self.configuracoes()
        else:
            self.sair = True

    def configuracoes(self):
        self.fonte_g = pygame.font.Font(dados.carrega_fonte("BLADRMF_.TTF"), 66)
        self.fonte_m = pygame.font.Font(dados.carrega_fonte("GOODTIME.ttf"), 40)
        self.fonte = pygame.font.Font(dados.carrega_fonte("GOODTIME.ttf"), 30)
        self.pos = 1
        self.reso = ["1024x768", "Tela Cheia", "Voltar"]

        sair = False
        while not sair:
            self.fundo.update()
            eventos = pygame.event.get()
            for e in eventos:
                if e.type == pygame.KEYDOWN:
                    self.som_menu_item.play()
                    if e.key == pygame.K_DOWN:
                        self.pos += 1
                    if e.key == pygame.K_UP:
                        self.pos -= 1
                    if e.key == pygame.K_RETURN:
                        if self.pos == 1:
                            self.screen = pygame.display.set_mode((1024, 768))
                        elif self.pos == 2:
                            self.screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
                        else:
                            sair = True
                    if e.type == QUIT:
                        sair = True
                    if e.type == KEYDOWN and e.key == K_ESCAPE:
                        sair = True
            if self.pos > 3:
                self.pos = 1
            if self.posicao_atual < 1:
                self.pos = 3

            self.fundo.draw(self.screen)

            ren_maior = self.fonte_g.render("Configuracoes do JUMP!", 1, self.hcor)
            self.pos_central = (self.screen.get_width() - ren_maior.get_rect().width)/2
            self.screen.blit(ren_maior, [self.pos_central, 5])

            ren = self.fonte_m.render('Selecione uma Resolucao', 1, self.hcor)
            self.pos_cen = (self.screen.get_width() - ren.get_rect().width)/2
            self.screen.blit(ren, [self.pos_cen, 100])

            y = 100
            cont = 1
            for i in self.reso:
                if cont == self.pos:
                    ren = self.fonte.render(i, 1, self.cor)
                else:
                    ren = self.fonte.render(i, 1, self.hcor)
                self.pos_cen = (self.screen.get_width() - ren.get_rect().width)/2
                self.screen.blit(ren, [self.pos_cen, y+50])
                y+=50
                cont+=1

            ren = self.fonte.render('Pressione ESC para Retornar ao menu principal', 1, self.cor)
            self.screen.blit(ren, [self.pos_central, self.screen.get_height() - 35])
            pygame.display.flip()

    def ranking(self):
        rank_json = dados.obter_ranking()

        s = False
        while not s:
            self.fundo.update()
            self.fundo.draw(self.screen)
            self.fonte_g = pygame.font.Font(dados.carrega_fonte("BLADRMF_.TTF"), 92)
            ren_maior = self.fonte_g.render("Ranking do JUMP!", 1, self.hcor)
            self.pos_central = (self.screen.get_width() - ren_maior.get_rect().width)/2
            self.screen.blit(ren_maior, [self.pos_central, 5])

            self.fonte = pygame.font.Font(dados.carrega_fonte("GOODTIME.ttf"), 30)
            ren = self.fonte.render('Rank', 1, self.cor)
            self.screen.blit(ren, [5, 100])
            ren = self.fonte.render('Jogador', 1, self.cor)
            self.screen.blit(ren, [150, 100])
            ren = self.fonte.render('Distancia', 1, self.cor)
            self.screen.blit(ren, [550, 100])
            ren = self.fonte.render('Moedas', 1, self.cor)
            self.screen.blit(ren, [850, 100])
            cont = 1
            y = 140

            if rank_json is not None:
                for i in rank_json:
                    ren = self.fonte.render(str(cont), 1, self.hcor)
                    self.screen.blit(ren, [10, y])
                    ren = self.fonte.render(i['nome'], 1, self.hcor)
                    self.screen.blit(ren, [155, y])
                    ren = self.fonte.render(i['distancia'], 1, self.hcor)
                    self.screen.blit(ren, [555, y])
                    ren = self.fonte.render(i['moedas'], 1, self.hcor)
                    self.screen.blit(ren, [855, y])
                    cont += 1
                    y += 40
                    if cont == 16:
                        break

            ren = self.fonte.render('Pressione ESC para Retornar ao menu principal', 1, self.cor)
            self.screen.blit(ren, [self.pos_central, self.screen.get_height() - 35])

            pygame.display.flip()
            eventos = pygame.event.get()
            for e in eventos:
                if e.type == pygame.KEYDOWN:
                    if e.key == K_ESCAPE:
                        self.som_menu_item.play()
                        s = True