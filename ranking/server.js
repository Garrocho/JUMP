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
 
