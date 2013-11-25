from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import detector_movimento


class WebSocketWebCam(WebSocket):

    def handleMessage(self):
        if self.data is None:
            self.data = ''

        # echo message back to client
        self.sendMessage(str(self.data))

    def handleConnected(self):
        print self.address, 'connected'
        self.processo = detector_movimento.DetectorMovimento(conexao=self)
        self.processo.start()

    def handleClose(self):
        print self.address, 'closed'
        gerenciador_estado_jogador = detector_movimento.GerenciadorEstadoJogador()
        gerenciador_estado_jogador._set_vivo(False)


if __name__ == "__main__":
    server = SimpleWebSocketServer('', 1339, WebSocketWebCam)
    server.serveforever()
