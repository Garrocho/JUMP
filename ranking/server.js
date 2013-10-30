// vai ajudar numa série de coisas, uma delas é suporte nativo a JSON
"use strict";
 
// título do processo
process.title = 'server';
 
// a porta que o servidor ouvirá
var porta = 1337;
 
// http, com tudo que é necessário para server e client do protocolo http
var http = require('http');
 
// url, com o que é necessário para resolução e parsing de urls
var url = require("url");
 
// vai entender as requisições GET que fizermos
var st = require('node-static');
 
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
 
