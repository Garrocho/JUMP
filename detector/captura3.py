# coding:utf-8

import cv2
import numpy as np
import sys


class Movimentos:
    '''
    Classe para simular uma enumeração com os possiveis valores para o movimento
    '''
    EM_PE = 0
    SUBINDO = 1
    DESCENDO = -1
    AGACHADO = -2


class DetectorMovimento:
    '''
    Classe para detectar o movimento
    '''
    # Constantes
    ARQUIVO_ESTADO_JOGADOR = './file/estado_jogador.json'
    ALTURA_QUADRADO_CENTRO = 150
    LARGURA_QUADRADO_CENTRO = 150
    # tem que receber false e so quando calibrar receber True
    MARGEM_ERRO = 20
    # evita que um simples aumento na altura da pessoa seja considerado um pulo
    MARGEM_TOLERANCIA = 70
    NUM_PONTOS_ANALIZADOS = 5

    Y_GUARDADOS = 5

    def __init__(self, id_camera=0):
        self.movimento = Movimentos.EM_PE
        # dentro do espaço delimitado pelas duas linhas amarelas, incluindo a
        # linha vermelha
        #dentro_espaco = False

        self.id_camera = id_camera

        self.camera = cv2.VideoCapture(self.id_camera)
        if not self.camera.isOpened():
            raise IOError('Não foi possivel ter acesso a camera')
        self.width, self.height = self.camera.get(3), self.camera.get(4)
        print 'Resolução da camera {0} x {1}'.format(self.width, self.height)

        self.ys = []
        self.desenhar_linhas = False
        self.calibrado = False

    def getThresholdedImage(self, hsv):
        min_cor = np.array((100, 150, 150), np.uint8)
        max_cor = np.array((130, 255, 255), np.uint8)

        cor = cv2.inRange(hsv, min_cor, max_cor)
        return cor

    def verificar_movimento(self):
        ultimos_valores_y = [0]
        if len(self.ys) >= self.NUM_PONTOS_ANALIZADOS:
            ultimos_valores_y = self.ys[
                len(self.ys) - self.NUM_PONTOS_ANALIZADOS:len(self.ys)]
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

    def atualizar_arquivo(self):
        novo_estado = 0
        if self.movimento == Movimentos.EM_PE:
            novo_estado = 0
        elif self.movimento == Movimentos.SUBINDO:
            novo_estado = 1
        elif self.movimento == Movimentos.AGACHADO:
            novo_estado = -1
        with open(self.ARQUIVO_ESTADO_JOGADOR, 'w') as arq:
            arq.write(str(novo_estado))

    def start(self):
        y_momento_pulo = None
        y_momento_agachar = None
        while(self.camera.isOpened()):
            _, frame = self.camera.read()
            frame = cv2.flip(frame, 1)
            blur = cv2.medianBlur(frame, 5)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            both = self.getThresholdedImage(hsv)
            erode = cv2.erode(both, None, iterations=3)
            dilate = cv2.dilate(erode, None, iterations=10)

            contours, hierarchy = cv2.findContours(
                dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            # desenha o quadrado no centro, para calibrar
            centro_x, centro_y = (int)(self.width / 2), (int)(self.height / 2)
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
                if y > centro_y - (self.ALTURA_QUADRADO_CENTRO / 2) - self.MARGEM_ERRO and \
                    y < centro_y - (self.ALTURA_QUADRADO_CENTRO / 2) + self.MARGEM_ERRO and \
                    y + h > centro_y + (self.ALTURA_QUADRADO_CENTRO / 2) - self.MARGEM_ERRO and \
                        y + h < centro_y + (self.ALTURA_QUADRADO_CENTRO / 2) + self.MARGEM_ERRO:
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
                #dentro_espaco = True
                if len(self.ys) >= self.Y_GUARDADOS:
                    self.ys = self.ys[1:self.Y_GUARDADOS]
                self.ys.append(y)
                # ta guardando ate Y_GUARDADOS Y
                if self.calibrado:
                    # verifica o tipo do movimento, 1 para subiu e -1 para
                    # desceu e 0 para nao movimentou
                    variacao_movimento = verificar_movimento()
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
                                if y_momento_agachar != None and y > y_momento_agachar - self.MARGEM_TOLERANCIA and y < y_momento_agachar + self.MARGEM_TOLERANCIA:
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
                            if y_momento_pulo != None and y > y_momento_pulo - self.MARGEM_TOLERANCIA and y < y_momento_pulo + self.MARGEM_TOLERANCIA:
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
                            atualizar_arquivo()
                    # nao houve variacao grande entre os pontos
                    else:
                        if y_momento_pulo != None and y > y_momento_pulo - self.MARGEM_TOLERANCIA and y < y_momento_pulo + self.MARGEM_TOLERANCIA:
                            if self.movimento == Movimentos.DESCENDO:
                                print 'De pé em px: {0}'.format(y)
                                self.movimento = Movimentos.EM_PE
                                y_momento_pulo = None
                                atualizar_arquivo()
                        if y_momento_agachar != None and y > y_momento_agachar - self.MARGEM_TOLERANCIA and y < y_momento_agachar + self.MARGEM_TOLERANCIA:
                            if self.movimento == Movimentos.AGACHADO:
                                print 'De pé em px: {0}'.format(y)
                                self.movimento = Movimentos.EM_PE
                                y_momento_agachar = None
                                atualizar_arquivo()

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

            cv2.imshow('Camera', frame)

            key = cv2.waitKey(25)
            # print 'key: ', key
            if key == 27:  # esc
                break

    def finish(self):
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
