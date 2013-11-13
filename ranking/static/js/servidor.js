// vai ajudar numa série de coisas, uma delas é suporte nativo a JSON
"use strict";
 
// título do processo
process.title = 'server';
 
// endereco e porta que o servidor ouvirá
var endereco = '127.0.0.1'
var porta = 1337;
 
// http, com tudo que é necessário para server e client do protocolo http

 
// url, com o que é necessário para resolução e parsing de urls
var url = require("url");
 
// vai entender as requisições GET que fizermos
var st = require('node-static');



// vai monitorar o arquivo ranking.json e
var chokidar = require('chokidar');
var monitorador = chokidar.watch('../../../dados/arquivos/ranking.json', {persistence:true});

// variáveis referentes a geolocalização
var app = http.createServer(handler);
var io = require('socket.io').listen(app);
var port = 8000;
var files = new st.Server('../.././static');

// Monitora se o arquivo é modificado, caso verdadeiro, envia a todos
// os clientes conectados no momento o novo ranking.
monitorador.on('change', function(path) {
    fs.readFile(path, 'utf8', function(error, data) {
        for (var i=0; i < clientes.length; i++) {
            clientes[i].sendUTF(data);
        }
    });
});

var fs = require('fs');
var servidorHTTP = require('http').createServer();
servidorHTTP.listen(4444, '127.0.0.1');
 
var webSocketServer = require('websocket').server;
var wsServer = new webSocketServer({
    httpServer: servidorHTTP
});

wsServer.on('request', function(request) {
    var conexao = request.accept(null, request.origin); 

    var index = clientes.push(conexao) - 1;
    fs.readFile('../../../dados/arquivos/ranking.json',
        'utf8', function(error, dados) {
        conexao.sendUTF(dados);
    });
    
    conexao.on('close', function() {
        clientes.splice(index, 1);
    });
});

// função que recebe uma requisião feita na porta 8000 e devolve o resultado da solicitação
function handler (request, response) {
	request.on('end', function() {
		files.serve(request, response);
	}).resume();
}

// captura logs do socket
io.set('log level', 1);

io.sockets.on('connection', function (socket) {

	socket.on('send:coords', function (data) {
		socket.broadcast.emit('load:coords', data);
	});
});
