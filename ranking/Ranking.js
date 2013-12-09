"use strict";

var URL_RANKING = "./file/ranking.json";

process.title = 'server';

var porta = 14527;

var http = require('http');
var url = require("url");
var st = require('node-static');
var fs = require('fs');

var fileServer = new st.Server();

var servidor = http.createServer(function(request, response) {
    request.addListener('end', function () {
        console.log(request.url);
        fileServer.serve(request, response);
    });
});

servidor.listen(porta, function() {
    console.log((new Date()) + " Node rodando na porta " + porta);
});

var webSocketServer = require('websocket').server;

var wsServer = new webSocketServer({
    httpServer: servidor
});

wsServer.on('request', function(request) {
    var conexao = request.accept(null, request.origin);

    conexao.on('message', function(message) {
        var mensagem = JSON.parse(message.utf8Data);
        if (mensagem['TIPO'] == 'GRAVAR') {
            fs.readFile(URL_RANKING, 'utf8', function(error, data) {
                console.log(data);
                var arq = JSON.parse(data);
                arq.push(mensagem['DADOS']);
                fs.writeFile(URL_RANKING, JSON.stringify(arq));
            });
        }
        else if (mensagem['TIPO'] == 'OBTER') {
            fs.readFile(URL_RANKING, 'utf8', function(error, data) {
                conexao.send(data);
            });
        }
    });
});
