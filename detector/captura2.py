# coding:utf-8
# detecta se um objeto de cor azul se movimentou
# acima da linha vermelha: mapeia se o usuário pulou
# abaixo da linha vermelha: mapeia se o usuário agachou


import cv2
import numpy as np

def getThresholdedImage(hsv):
    #min_yellow = np.array((20, 100, 100), np.uint8)
    #max_yellow = np.array((30, 255, 255), np.uint8)
    min_yellow = np.array((20, 70, 70), np.uint8)
    max_yellow = np.array((30, 255, 255), np.uint8)

    yellow = cv2.inRange(hsv, min_yellow, max_yellow)
    return yellow


def verificar_movimento(ys):
    ultimo_y = ys[len(ys) - 1]
    primeiro_y = ys[0]
    if primeiro_y < ultimo_y:  #ta descendo
        return -1
    else:
        return 1

ALTURA_QUADRADO_CENTRO = 150
LARGURA_QUADRADO_CENTRO = 150
# tem que receber false e so quando calibrar receber True
CALIBRADO = False
MARGEM_ERRO = 20
MARGEM_TOLERANCIA = 20  # evita que um simples aumento na altura da pessoa seja considerado um pulo
NUM_PONTOS_ANALIZADOS = 5

Y_GUARDADOS = 5
movimento = 0  # 0 = parado, 1 subindo, -1 descendo, 2 agachado
# dentro do espaço delimitado pelas duas linhas amarelas, incluindo a
# linha vermelha
#dentro_espaco = False

c = cv2.VideoCapture(1)
if not c.isOpened():
    print 'Erro: Nao foi possivel ter acesso a camera'
    exit(0)
width, height = c.get(3), c.get(4)
print 'Resolução da camera {} x {}'.format(width, height)

ys = [height - 50]

desenhar_linhas = True
while(c.isOpened()):
    _, frame = c.read()
    frame = cv2.flip(frame, 1)
    blur = cv2.medianBlur(frame, 5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    both = getThresholdedImage(hsv)
    erode = cv2.erode(both, None, iterations=3)
    dilate = cv2.dilate(erode, None, iterations=10)

    contours, hierarchy = cv2.findContours(
        dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # desenha o quadrado no centro, para calibrar
    centro_x, centro_y = (int)(width / 2), (int)(height / 2)
    cv2.rectangle(
        frame, (centro_x - (LARGURA_QUADRADO_CENTRO / 2),
                centro_y - (ALTURA_QUADRADO_CENTRO / 2)),
        (centro_x + (LARGURA_QUADRADO_CENTRO / 2), centro_y + (ALTURA_QUADRADO_CENTRO / 2)), [0, 255, 0], 2)

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
        #if (cx > centro_x - (LARGURA_QUADRADO_CENTRO / 2)) and (cx < centro_x - (LARGURA_QUADRADO_CENTRO / 2) - MARGEM_ERRO) and (cx > centro_x + (LARGURA_QUADRADO_CENTRO / 2) - MARGEM_ERRO) and (cx < centro_x + (LARGURA_QUADRADO_CENTRO / 2)):
        #print y, y + h, centro_y - (ALTURA_QUADRADO_CENTRO / 2), centro_y + (ALTURA_QUADRADO_CENTRO / 2)

        if y > centro_y - (ALTURA_QUADRADO_CENTRO / 2) - MARGEM_ERRO and \
         y < centro_y - (ALTURA_QUADRADO_CENTRO / 2) + MARGEM_ERRO and \
         y + h > centro_y + (ALTURA_QUADRADO_CENTRO / 2) - MARGEM_ERRO and \
         y + h < centro_y + (ALTURA_QUADRADO_CENTRO / 2) + MARGEM_ERRO:
            if not CALIBRADO:
                print 'ta dentro'
                CALIBRADO = True

        # print hsv.item(cy, cx, 0), hsv.item(cy, cx, 1), hsv.item(cy, cx, 2)
        # if 100 < hsv.item(cy, cx, 0) < 120:
        cv2.rectangle(frame, (x, y), (x + w, y + h), [255, 0, 0], 2)
        if y > 50 and y < height - 50:
            #dentro_espaco = True
            if len(ys) >= Y_GUARDADOS:
                ys = ys[1:Y_GUARDADOS]
            ys.append(y)
            # ta guardando ate Y_GUARDADOS Y
            if CALIBRADO:
                ultimos_valores_y = [0]
                if len(ys) >= NUM_PONTOS_ANALIZADOS:
                    ultimos_valores_y = ys[len(ys)-NUM_PONTOS_ANALIZADOS:len(ys)]
                if max(ultimos_valores_y) - min(ultimos_valores_y) > MARGEM_TOLERANCIA:
                    novo_movimento = verificar_movimento(ys)
                    mudou_movimento = False
                    if novo_movimento == 1:
                        if movimento == 0:
                            movimento = 1
                            mudou_movimento = True
                        elif movimento == -2:
                            movimento = 0
                            mudou_movimento = True
                    elif novo_movimento == -1:
                        if movimento == 0:
                            movimento = -2
                            mudou_movimento = True
                        elif movimento == 1:
                            movimento == 0
                            mudou_movimento = True
                    if mudou_movimento:
                        if movimento == 1:
                            print 'Pulou em px: {}'.format((int(height) - 50) - y)
                        elif movimento == -2:
                            print 'Agachou em px: {}'.format((int(height) - 50) - y)
        else:
            #dentro_espaco = False
            pass

    if desenhar_linhas:
        # linha superior (640 x 50)
        cv2.line(frame, (0, 50), (int(width), 50), (0, 255, 255), 2)

        # linha inferior (640 x 430)
        cv2.line(frame, (0, int(height - 50)),
                 (int(width), int(height - 50)), (0, 255, 255), 2)

        # linha que define se o usuário agachou (640 x 330)
        cv2.line(frame, (0, int(height - 150)),
                (int(width), int(height - 150)), (0, 0, 255), 2)

    cv2.imshow('Camera', frame)

    key = cv2.waitKey(25)
    # print 'key: ', key
    if key == 27:  # esc
        break

cv2.destroyAllWindows()
c.release()
