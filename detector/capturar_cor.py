import cv2
import numpy as np
import sys

def tratar_mouse(event, x, y, flag, param):
    print param[y, x]

ALTURA_QUADRADO_CENTRO = 150
LARGURA_QUADRADO_CENTRO = 150

id_camera = int(sys.argv[1]) if len(sys.argv) > 1 else 0

c = cv2.VideoCapture(id_camera)
if not c.isOpened():
    print 'Erro: Nao foi possivel ter acesso a camera'
    exit(0)
width, height = c.get(3), c.get(4)

while(c.isOpened()):
    _, frame = c.read()
    frame = cv2.flip(frame, 1)
    blur = cv2.medianBlur(frame, 5)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    centro_x, centro_y = (int)(width / 2), (int)(height / 2)

    cv2.rectangle(
        frame, (centro_x - (LARGURA_QUADRADO_CENTRO / 2),
                centro_y - (ALTURA_QUADRADO_CENTRO / 2)),
        (centro_x + (LARGURA_QUADRADO_CENTRO / 2), centro_y + (ALTURA_QUADRADO_CENTRO / 2)), [0, 255, 0], 2)

    #print hsv[centro_x, centro_y]

    cv2.cv.SetMouseCallback('Camera', tratar_mouse, param=hsv)
    cv2.imshow('Camera', frame)

    key = cv2.waitKey(25)
    # print 'key: ', key
    if key == 27:  # esc
        break

cv2.destroyAllWindows()
c.release()
