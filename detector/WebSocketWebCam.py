from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import detector_movimento
import cv2



class WebSocketWebCam(WebSocket):

    camera = cv2.VideoCapture(0)
    processo = None

    def handleMessage(self):
        with open('./file/estado_jogo_cliente.json', 'w') as arq:
            arq.write(self.data)

    def handleConnected(self):
        print self.address, 'connected'
        if self.processo is None:
            if detector_movimento.processo is None:
                self.processo = detector_movimento.DetectorMovimento(conexao=self)
                detector_movimento.processo = self.processo
                self.processo.start()
            else:
                print 'teste1'
                self.processo = detector_movimento.processo
                self.processo.conexao = self
        else:
            print 'teste'
            self.processo.conexao = self

    def handleClose(self):
        print self.address, 'closed'
        gerenciador_estado_jogador = detector_movimento.GerenciadorEstadoJogador(
        )
        gerenciador_estado_jogador._set_vivo(False)
#        self.processo.calibrado = False


if __name__ == "__main__":

    server = SimpleWebSocketServer('', 1339, WebSocketWebCam)
    server.serveforever()
