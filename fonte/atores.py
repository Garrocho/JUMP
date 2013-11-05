import pygame
from pygame.locals import *


class Fundo:
    imagem = None
    var_largura = 0

    def __init__(self, imagem, tam_px):
        self.imagem = imagem
        self.tam_px = tam_px
        self.var_largura = tam_px
        self.largura, self.altura = imagem.get_size()

    def update(self):
        self.var_largura+=self.tam_px
        if (self.var_largura >= self.largura):
            self.var_largura=self.tam_px
        # Recorta a imagem. Os dois primeiros argumentos representam de qual posicao vai comecar o corte.
        # os outros dois argumentos representar o tamanho do corte.
        self.recorte1 = self.imagem.subsurface((self.var_largura, 0, self.largura-self.var_largura, self.altura))
        self.recorte2 = self.imagem.subsurface((0, 0, self.var_largura, self.altura))

    def draw(self, screen):
        screen.blit(self.recorte1, (0, 0))
        screen.blit(self.recorte2, (self.largura-self.var_largura, 0))


class Jogador(pygame.sprite.Sprite):

    def __init__(self, imagem, posicao, som):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagem[0]
        self.fatias = imagem
        self.rect = self.image.get_rect()
        self.rect.center = (posicao)
        self.pulando = False
        self.fases_pulo = 0
        self.tempo_fatia = 1
        self.tempo_fatia_1 = 4
        self.cont = 0
        self.som = som
        self.status = {"Moedas":0, "Distancia":0}

    def pular(self):
        self.fases_pulo = 80
        self.pulando = True
        self.image = self.fatias[33]
        self.som.play()

    def atingido(self):
        pass

    def update(self):
        if not self.pulando and self.cont < 36:
            if self.tempo_fatia_1 == 0:
                self.tempo_fatia_1 = 5
                self.cont+=3
                self.image = self.fatias[self.cont]
            else:
                self.tempo_fatia_1 = self.tempo_fatia_1 - 1
        else:
            self.cont = 0
            
        # Trata os pulos do jogador
        if self.pulando:
            if self.tempo_fatia == 0:
                if self.fases_pulo >= 40:
                    self.tempo_fatia = 1
                    self.rect.center = (self.rect.center[0], self.rect.center[1] - 10)
                    self.fases_pulo = self.fases_pulo - 1
                elif self.fases_pulo >= -1:
                    self.image = self.fatias[12]
                    self.tempo_fatia = 1
                    self.fases_pulo = self.fases_pulo - 1
                    self.rect.center = (self.rect.center[0], self.rect.center[1] + 10)
                else:
                    self.pulando = False
                    self.fases_pulo = 0
                    self.cont = 12
            else:
                self.tempo_fatia = self.tempo_fatia - 1


class AtorComEfeito(pygame.sprite.Sprite):

    def __init__(self, imagem, posicao, velocidade, som):
        pygame.sprite.Sprite.__init__(self)
        self.som = som
        self.image = imagem[0]
        self.fatias = imagem
        self.rect = self.image.get_rect()
        self.rect.center = (posicao)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.fatia_atual = -1
        self.fatia_tam = len(self.fatias)-1
        self.tempo_fatia = velocidade
        self.velocidade = velocidade

    def update(self):
        if self.tempo_fatia == 0:
            self.tempo_fatia = self.velocidade
            if self.fatia_atual < self.fatia_tam:
                self.fatia_atual = self.fatia_atual + 1
                if self.fatia_atual == self.fatia_tam:
                    self.fatia_atual = 0
            self.image = self.fatias[self.fatia_atual]
        else:
            self.tempo_fatia = self.tempo_fatia - 1

        self.rect.center = (self.rect.center[0] - self.velocidade, self.rect.center[1])

        if self.rect.left > self.area.right or self.rect.top > self.area.bottom or self.rect.right < 0:
            self.kill()
        if self.rect.bottom < -40:
            self.kill()
     
    def atingido(self):
        self.som.play()


class AtorSemEfeito(pygame.sprite.Sprite):

    def __init__(self, imagem, posicao, velocidade, som=None):
        pygame.sprite.Sprite.__init__(self)
        self.som = som
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.center = (posicao)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.velocidade = velocidade

    def update(self):
        if (self.rect.left+self.image.get_size()[0]) < 0:
            self.kill()
        self.rect.center = (self.rect.center[0] - self.velocidade, self.rect.center[1])
     
    def atingido(self):
        pass
        #self.som.play()


class Status:
    fonte = None
    cor = None
    imagem = None
    jogador = None
    identificador = None
    
    def __init__(self, jogador, posicao=None, fonte=None, tam_texto=35, cor="0xff0f0f", identificador=None):
        self.identificador = identificador
        self.jogador = jogador
        self.cor = pygame.color.Color(cor)
        self.posicao = posicao or [5, 5]
        self.fonte = pygame.font.Font(fonte, tam_texto)

    def update(self):
        pass

    def draw(self, screen):
        texto = self.identificador + ": % 4d" % self.jogador.status[self.identificador]
        desenho = self.fonte.render(texto, True, self.cor)
        screen.blit(desenho, self.posicao)