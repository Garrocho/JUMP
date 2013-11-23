// vai ajudar numa série de coisas, uma delas é suporte nativo a JSON
"use strict";
 
// título do processo
process.title = 'server_estado_jogador';
 
// endereco e porta que o servidor ouvirá
var endereco = '127.0.0.1'
var porta = 1338;
 
// http, com tudo que é necessário para server e client do protocolo http
var http = require('http');
 
// url, com o que é necessário para resolução e parsing de urls
var url = require("url");
 
// vai entender as requisições GET que fizermos
var st = require('node-static');

var fs = require('fs');

// vai monitorar o arquivo ranking.json e
var chokidar = require('chokidar');

var monitorador_estado_jogador = chokidar.watch('./file/estado_jogador.json', {persistence: true, interval: 50, binaryInterval: 150}); //interval: 100, binaryInterval: 300

monitorador_estado_jogador.on('change', function(path) {
    fs.readFile(path, 'utf8', function(error, data) {
        if(cliente != null){
            cliente.sendUTF(data);
        }
        else{
            console.log("cliente null: não foi possivel enviar a mensagem");
        }
    });
});

// criamos um servidor de arquivos...
var fileServer = new st.Server();
 
// criamos um servidor de arquivos usando um método da variável 'http'
// esse método recebe um callback com 'request' e 'response' como argumentos
var servidor = http.createServer(function(request, response) {
 
    // adicionamos um evento a request, ou seja quando tivermos 'end',
    // no final da requisição, o callback que passamos como segundo parâmetro
    // será executado...
    request.addListener('end', function () {
        // adicionamos um console para ver toda a requisição para uma url específica
        console.log(request.url);
 
        // chamamos o método 'serve' de 'fileServer' passando 'request' e 'response' como argumento
        fileServer.serve(request, response);
    });
});
 
servidor.listen(porta, endereco, function() {
    // chamamos o método 'listen' de 'server' para indicarmos a porta que sera ouvida
    console.log((new Date()) + " Node rodando no endereco " + endereco + " na porta " + porta);
});
 
var webSocketServer = require('websocket').server;
 
var cliente = null;
 
// instanciamos um server passando um objeto como argumento esse objeto tem uma
// propriedade 'httpServer' que recebe 'servidor' nossa variável criada acima que
// nada mais é que o servidor http que usamos como host do nosso index.html
var wsServer = new webSocketServer({
    httpServer: servidor
});
 
// chamamos o método 'on' de 'wsServer' passando 'request' e um callback
// Ou seja, toda vez que temos uma requisição, o callback será executado
// esse callback recebe 'request' como argumento
wsServer.on('request', function(request) {
 
    // o objeto request tem um método chamado 'accept' onde aceitamos
    // a conexão passando o protocolo e a origem (deixemos isso para depois)
    cliente = request.accept(null, request.origin); 
});

console.log("Nao ta recebendo do cliente :(");
wsServer.on('connection', function(ws) {
    ws.on('message', function(message) {
        console.log('recebido: %s', message);
    });
});