# coding:utf-8
''' v 0.1 - It tracks two objects of blue and yellow color each '''
# detect_jump.py

import cv2
import numpy as np
import time
from threading import Thread

class PosicionamentoJogador(Thread):
    def __init__(self):
        Thread.__init__(self)
        #self.c = c
        self.lista_dados = []
        self.media = 0

    def run(self):
        c = cv2.VideoCapture(0)
        width, height = c.get(3), c.get(4)
        i = 0
        Y_GUARDADOS = 2
        dentro_espaco = False # dentro do espaço delimitado pelas duas linhas amarelas, incluindo a linha vermelha 
        ys = [height - 50]
        desenhar_linhas = True        
        while i < 100:
            i = i + 1
            time.sleep(0.1)
            _, f = c.read()
            f = cv2.flip(f, 1)
            blur = cv2.medianBlur(f, 5)
            hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)

            both = getThresholdedImage(hsv)
            erode = cv2.erode(both, None, iterations=3)
            dilate = cv2.dilate(erode, None, iterations=10)

            contours, hierarchy = cv2.findContours(
                dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

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

                #print hsv.item(cy, cx, 0), hsv.item(cy, cx, 1), hsv.item(cy, cx, 2)
                #if 100 < hsv.item(cy, cx, 0) < 120:
                cv2.rectangle(f, (x, y), (x + w, y + h), [255, 0, 0], 2)
                self.lista_dados.append(h)
                print h

            if desenhar_linhas:
                # linha superior (640 x 50)
                cv2.line(f, (0, 50), (int(width), 50), (0, 255, 255), 2)

                # linha inferior (640 x 430)
                cv2.line(f, (0, int(height - 50)),
                         (int(width), int(height - 50)), (0, 255, 255), 2)

            cv2.imshow('Camera', f)

            key = cv2.waitKey(25)
            # print 'key: ', key
            if key == 27:  # esc
                break
            elif key == 32:  # space
                desenhar_linhas = not desenhar_linhas
        
        cv2.destroyAllWindows()
        c.release()
        funcao_media = lambda x, y: x + y        
        self.media = (reduce(funcao_media, self.lista_dados))/len(self.lista_dados)
        print self.media

def getThresholdedImage(hsv):
    min_blue = np.array((0, 100, 100), np.uint8)
    max_blue = np.array((120, 255, 255), np.uint8)

    blue = cv2.inRange(hsv, min_blue, max_blue)
    return blue

def verificar_movimento(ys):
    #print 'distancia em px: {}'.format((int(height) - 50) - ys[len(ys)-1])
    ultimo_y = ys[len(ys)-1]
    menor_y = min(ys[0:len(ys)-1])
    if ultimo_y < menor_y and ultimo_y < 330:
        #print 'subindo'
        return 1
    elif ultimo_y == menor_y  and ultimo_y < 330:
        #print 'parado'
        return 0
    elif ultimo_y > menor_y  and ultimo_y < 330:
        #print 'descendo'    
        return -1
    elif ultimo_y > 330 and ultimo_y < 430:
        #print 'agachado'
        return 2


# programa principal
if __name__ == '__main__':
    #c = cv2.VideoCapture(0)
    #if(not c.isOpened()):
     #   print 'Erro: Nao foi possivel ter acesso a camera'
      #  exit(0)
    #width, height = c.get(3), c.get(4)
    #print 'Resolução da camera {} x {}'.format(width, height)
    
    PosicionamentoJogador = PosicionamentoJogador()
    PosicionamentoJogador.start()
    print 'a'
    '''    
    Y_GUARDADOS = 2
    MOVIMENTO = 0 # 0 = parado, 1 subindo, -1 descendo, 2 agachado
    dentro_espaco = False # dentro do espaço delimitado pelas duas linhas amarelas, incluindo a linha vermelha 
    ys = [height - 50]
    desenhar_linhas = True
    while(c.isOpened()):
        _, f = c.read()
        f = cv2.flip(f, 1)
        blur = cv2.medianBlur(f, 5)
        hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)

        both = getThresholdedImage(hsv)
        erode = cv2.erode(both, None, iterations=3)
        dilate = cv2.dilate(erode, None, iterations=10)

        contours, hierarchy = cv2.findContours(
            dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

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

            print hsv.item(cy, cx, 0), hsv.item(cy, cx, 1), hsv.item(cy, cx, 2)
            #if 100 < hsv.item(cy, cx, 0) < 120:
            cv2.rectangle(f, (x, y), (x + w, y + h), [255, 0, 0], 2)
            if y > 50 and y < height - 50:
                dentro_espaco = True
                if len(ys) >= Y_GUARDADOS:
                    ys = ys[1:Y_GUARDADOS]
                ys.append(y)
                # ta guardando ate Y_GUARDADOS Y
                movimento_atual = verificar_movimento(ys)
                if MOVIMENTO == 1 and movimento_atual == -1:
                    print 'Pulou em px: {}'.format((int(height) - 50) - y)
                elif MOVIMENTO == -1 and movimento_atual == 2:
                    print 'Agachou em px: {}'.format((int(height) - 50) - y)
                MOVIMENTO = movimento_atual
            else:
                dentro_espaco = False

        if desenhar_linhas:
            # linha superior (640 x 50)
            cv2.line(f, (0, 50), (int(width), 50), (0, 255, 255), 2)

            # linha inferior (640 x 430)
            cv2.line(f, (0, int(height - 50)),
                     (int(width), int(height - 50)), (0, 255, 255), 2)
     
            # linha que define se o usuário agachou (640 x 330)
            cv2.line(f, (0, int(height - 150)),
                    (int(width), int(height - 150)), (0, 0, 255), 2)

        cv2.imshow('Camera', f)

        key = cv2.waitKey(25)
        # print 'key: ', key
        if key == 27:  # esc
            break
        elif key == 32:  # space
            desenhar_linhas = not desenhar_linhas'''
    
    '''
    cv2.destroyAllWindows()
    c.release()'''
