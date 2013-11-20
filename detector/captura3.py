#!/usr/bin/env python
# coding:utf-8

import cv2
import numpy as np
import sys


class Movimentos(object):

    '''
    Classe para simular uma enumeração com os possiveis valores para o movimento
    '''
    EM_PE = 0
    SUBINDO = 1
    DESCENDO = -1
    AGACHADO = -2


class GerenciadorEstadoJogador(object):

    '''
    Classe para gerenciar o estado do jogador
    '''
    # Constantes
    ARQUIVO_ESTADO_JOGADOR = './file/estado_jogador.json'

    class EstadosJogador(object):

        '''
        Classe para simular uma enumeração com os etados do jogador
        '''
        EM_PE = 0
        PULANDO = 1
        AGACHADO = -1

    def atualizar_estado(self, movimento):
        '''
        Atualiza o estado do jogador no arquivo
        '''
        novo_estado = 0
        if movimento == Movimentos.EM_PE:
            novo_estado = self.EstadosJogador.EM_PE
        elif movimento == Movimentos.SUBINDO:
            novo_estado = self.EstadosJogador.PULANDO
        elif movimento == Movimentos.AGACHADO:
            novo_estado = self.EstadosJogador.AGACHADO
        # Recria o arquivo e insere o novo estado do jogador
        with open(self.ARQUIVO_ESTADO_JOGADOR, 'w') as arq:
            arq.write(str(novo_estado))


class DetectorMovimento(object):

    '''
    Classe para detectar o movimento
    '''
    # Constantes
    ALTURA_QUADRADO_CENTRO = 150
    LARGURA_QUADRADO_CENTRO = 150
    MARGEM_ERRO_CALIBRACAO = 20
    # evita que um simples aumento na altura da pessoa seja considerado um pulo
    MARGEM_TOLERANCIA = 70
    NUM_Y_ANALIZADOS = 5

    NUM_Y_GUARDADOS = 5

    def __init__(self, id_camera=0):
        '''
        Construtor da Classe
        :param id_camera: identificador da camera que será utilizada, o padrão é 0
        '''
        self.movimento = Movimentos.EM_PE
        # dentro do espaço delimitado pelas duas linhas amarelas, incluindo a
        # linha vermelha
        self.id_camera = id_camera

        self.camera = cv2.VideoCapture(self.id_camera)
        if not self.camera.isOpened():
            raise IOError('Não foi possivel ter acesso a camera')
        if self.NUM_Y_ANALIZADOS > self.NUM_Y_GUARDADOS:
            raise ValueError("Número de pontos analisados deve ser igual ou menor que o numero de Y guardados")
        self.width, self.height = self.camera.get(3), self.camera.get(4)
        print 'Resolução da camera {0} x {1}'.format(self.width, self.height)

        self.ys = []
        self.desenhar_linhas = False
        self.calibrado = False

        self.gerenciador_estado_jogador = GerenciadorEstadoJogador()

    def getThresholdedImage(self, hsv):
        '''
        Gera uma faixa de cor
        :param hsv: imagem no formato de cor hsv
        :returns: a faixa de cor
        '''
        min_cor = np.array((100, 150, 150), np.uint8)
        max_cor = np.array((130, 255, 255), np.uint8)

        faixa_cor = cv2.inRange(hsv, min_cor, max_cor)
        return faixa_cor

    def verificar_movimento(self):
        '''
        Verifica se houve movimento e se foi para baixo ou para cima
        :returns: 0 se não houve movimento, 1 se houve movimento para cima e -1 se houve movimento para baixo
        '''
        ultimos_valores_y = [0]
        if len(self.ys) >= self.NUM_Y_ANALIZADOS:
            ultimos_valores_y = self.ys[
                len(self.ys) - self.NUM_Y_ANALIZADOS:len(self.ys)]
        # houve diferenca maior que a margem entre dois pontos Y dentro do
        # numero de pontos analizados
        if max(ultimos_valores_y) - min(ultimos_valores_y) > self.MARGEM_TOLERANCIA:
            ultimo_y = self.ys[len(self.ys) - 1]
            primeiro_y = self.ys[0]
            if primeiro_y < ultimo_y:  # ta descendo
                return -1
            else:
                return 1
        else:
            return 0

    def start(self):
        '''
        Inicia a detecção
        '''
        y_momento_pulo = None
        y_momento_agachar = None
        centro_x, centro_y = (int)(self.width / 2), (int)(self.height / 2)
        while(self.camera.isOpened()):
            _, frame = self.camera.read()
            frame = cv2.flip(frame, 1)
            blur = cv2.medianBlur(frame, 5)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            faixa_cor = self.getThresholdedImage(hsv)
            erode = cv2.erode(faixa_cor, None, iterations=3)
            dilate = cv2.dilate(erode, None, iterations=10)

            contours, hierarchy = cv2.findContours(
                dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            # desenha o quadrado no centro, para calibrar
            cv2.rectangle(
                frame, (centro_x - (self.LARGURA_QUADRADO_CENTRO / 2),
                        centro_y - (self.ALTURA_QUADRADO_CENTRO / 2)),
                (centro_x + (self.LARGURA_QUADRADO_CENTRO / 2), centro_y + (self.ALTURA_QUADRADO_CENTRO / 2)), [0, 255, 0], 2)

            if not self.calibrado:
                self.ys = []
                y_momento_pulo = None
                y_momento_agachar = None

            if contours:
                maior_area = 0
                maior_contorno = contours[0]
                for cont in contours:
                    cx, cy, cw, ch = cv2.boundingRect(cont)
                    area = cw * ch
                    if area > maior_area:
                        maior_area = area
                        maior_contorno = cont

                x, y, w, h = cv2.boundingRect(maior_contorno)
                cx, cy = x + w / 2, y + h / 2

                # verifica se ta no centro
                if y > centro_y - (self.ALTURA_QUADRADO_CENTRO / 2) - self.MARGEM_ERRO_CALIBRACAO and \
                    y < centro_y - (self.ALTURA_QUADRADO_CENTRO / 2) + self.MARGEM_ERRO_CALIBRACAO and \
                    y + h > centro_y + (self.ALTURA_QUADRADO_CENTRO / 2) - self.MARGEM_ERRO_CALIBRACAO and \
                        y + h < centro_y + (self.ALTURA_QUADRADO_CENTRO / 2) + self.MARGEM_ERRO_CALIBRACAO:
                    if not self.calibrado:
                        print 'Calibrou'
                        self.calibrado = True
                    # dentro do quadrado
                    cv2.rectangle(
                        frame, (centro_x - (self.LARGURA_QUADRADO_CENTRO / 2),
                                centro_y - (self.ALTURA_QUADRADO_CENTRO / 2)),
                        (centro_x + (self.LARGURA_QUADRADO_CENTRO / 2), centro_y + (self.ALTURA_QUADRADO_CENTRO / 2)), [0, 0, 255], 2)

                # print hsv.item(cy, cx, 0), hsv.item(cy, cx, 1), hsv.item(cy, cx, 2)
                # if 100 < hsv.item(cy, cx, 0) < 120:
                cv2.rectangle(frame, (x, y), (x + w, y + h), [255, 0, 0], 2)

                if len(self.ys) >= self.NUM_Y_GUARDADOS:
                    self.ys = self.ys[1:self.NUM_Y_GUARDADOS]
                self.ys.append(y)
                # ta guardando ate NUM_Y_GUARDADOS Y
                if self.calibrado:
                    # verifica o tipo do movimento, 1 para subiu e -1 para
                    # desceu e 0 para nao movimentou
                    variacao_movimento = self.verificar_movimento()
                    if variacao_movimento:
                        # guarda o movimento antigo, mas pra nada
                        movimento_antigo = self.movimento
                        mudou_movimento = False
                        # subiu, mas o que houve?
                        if variacao_movimento == 1:
                            # pulou
                            if self.movimento == Movimentos.EM_PE:
                                self.movimento = Movimentos.SUBINDO
                                y_momento_pulo = y
                                mudou_movimento = True
                            # levantou
                            elif self.movimento == Movimentos.AGACHADO:
                                # and y > y_momento_agachar - self.MARGEM_TOLERANCIA
                                if y_momento_agachar != None and y < y_momento_agachar + self.MARGEM_TOLERANCIA:
                                    self.movimento = Movimentos.EM_PE
                                    mudou_movimento = True
                        # desceu, mas o que houve?
                        elif variacao_movimento == -1:
                            # agachou
                            if self.movimento == Movimentos.EM_PE:
                                y_momento_agachar = y
                                self.movimento = Movimentos.AGACHADO
                                mudou_movimento = True
                            # ta descendo do pulo
                            elif self.movimento == Movimentos.SUBINDO:
                                self.movimento = Movimentos.DESCENDO
                                mudou_movimento = True

                        if self.movimento == Movimentos.DESCENDO:
                            # voltou ao chao
                            print y, y_momento_pulo
                            # and y < y_momento_pulo + self.MARGEM_TOLERANCIA:
                            if y_momento_pulo != None and y > y_momento_pulo - self.MARGEM_TOLERANCIA:
                                self.movimento = Movimentos.EM_PE
                                y_momento_pulo = None
                                mudou_movimento = True
                        print 'mov:{0} mov_ant: {1} mov_var: {2}'.format(self.movimento, movimento_antigo, variacao_movimento)
                        if mudou_movimento:
                            if self.movimento == Movimentos.SUBINDO:
                                print 'Pulou em px: {0}'.format(y_momento_pulo)
                            elif self.movimento == Movimentos.AGACHADO:
                                print 'Agachou em px: {0}'.format(y_momento_agachar)
                            elif self.movimento == Movimentos.EM_PE:
                                print 'De pé em px: {0}'.format(y)
                            self.gerenciador_estado_jogador.atualizar_estado(
                                self.movimento)
                    # nao houve variacao grande entre os pontos
                    else:
                        # and y < y_momento_pulo + self.MARGEM_TOLERANCIA:
                        if y_momento_pulo != None and y > y_momento_pulo - self.MARGEM_TOLERANCIA:
                            if self.movimento == Movimentos.DESCENDO:
                                print 'De pé em px: {0}'.format(y)
                                self.movimento = Movimentos.EM_PE
                                y_momento_pulo = None
                                self.gerenciador_estado_jogador.atualizar_estado(
                                    self.movimento)
                        # and y > y_momento_agachar - self.MARGEM_TOLERANCIA:
                        if y_momento_agachar != None and y < y_momento_agachar + self.MARGEM_TOLERANCIA:
                            if self.movimento == Movimentos.AGACHADO:
                                print 'De pé em px: {0}'.format(y)
                                self.movimento = Movimentos.EM_PE
                                y_momento_agachar = None
                                self.gerenciador_estado_jogador.atualizar_estado(
                                    self.movimento)

            if self.desenhar_linhas:
                # linha superior (640 x 50)
                cv2.line(frame, (0, 50), (int(self.width), 50),
                         (0, 255, 255), 2)

                # linha inferior (640 x 430)
                cv2.line(frame, (0, int(self.height - 50)),
                         (int(self.width), int(self.height - 50)), (0, 255, 255), 2)

                # linha que define se o usuário agachou (640 x 330)
                cv2.line(frame, (0, int(self.height - 150)),
                         (int(self.width), int(self.height - 150)), (0, 0, 255), 2)

            cv2.imshow('JUMP! Detecção', frame)

            key = cv2.waitKey(25)
            if key == 27:  # esc
                break

    def finish(self):
        '''
        finaliza a detecção e os recursos
        '''
        cv2.destroyAllWindows()
        self.camera.release()

if __name__ == "__main__":
    try:
        id_camera = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    except ValueError as e:
        id_camera = 0
    detector_movimento = DetectorMovimento(id_camera)
    detector_movimento.start()
    detector_movimento.finish()
