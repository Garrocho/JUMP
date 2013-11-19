// vai ajudar numa série de coisas, uma delas é suporte nativo a JSON
"use strict";
 
// título do processo
process.title = 'server';
 
// endereco e porta que o servidor ouvirá
var endereco = '127.0.0.1'
var porta = 1337;
 
// http, com tudo que é necessário para server e client do protocolo http
var http = require('http');
 
// url, com o que é necessário para resolução e parsing de urls
var url = require("url");
 
// vai entender as requisições GET que fizermos
var st = require('node-static');

var fs = require('fs');

// vai monitorar o arquivo ranking.json e
var chokidar = require('chokidar');
var monitorador = chokidar.watch('./file/ranking.json', {persistence:true});

// Monitora se o arquivo é modificado, caso verdadeiro, envia a todos
// os clientes conectados no momento o novo ranking.
monitorador.on('change', function(path) {
    fs.readFile(path, 'utf8', function(error, data) {
        for (var i=0; i < clientes.length; i++) {
            clientes[i].sendUTF(data);
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
 
// clientes é um array simples onde colocaremos todos os clientes que forem conectados
var clientes = [];
 
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
    var conexao = request.accept(null, request.origin); 
 
    // index é o índice do usuário na "fila" que formamos de maneira que todas
    // as conexões no socket são adicionadas no array 'clientes' pelo método
    // 'push'. O método retorna o comprimento do array depois de adicionarmos
    // aquele elemento. Se subtraírmos um, temos a posição do último elemento.
   /* var index = clientes.push(conexao) - 1;
    fs.readFile('./file/ranking.json', 'utf8', function(error, data) {
        conexao.sendUTF(data);
    });*/
    
 
    // chamamos o método 'on' passando 'close' e um callback como você já deve
    // ter deduzido, o callback será chamado quando a conexão for fechada de
    // alguma forma. Comumente acontece quando fechamos o browser.
    conexao.on('close', function() {
        // chamamos o método 'splice' do array passando 'index' e 1 como parâmetros
        // assim vamos excluir 1 elemento na posição do 'index'. Logo, excluiremos
        // o cliente que se desconectou.
        clientes.splice(index, 1);
    });
    
   conexao.on('message', function(message) {
        console.log(message);
    });  
});
