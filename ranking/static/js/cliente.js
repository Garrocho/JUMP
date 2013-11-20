// link API geolocalização: 
//https://developers.google.com/maps/documentation/javascript/geocoding?hl=pt-br

// criamos uma variável 'conexao'
var conexao = null;

// depois do carregamento da página, chamamos 'setConexao' e 'setEventos'
window.onload = function(){
    setConexao();
}
 
var setConexao = function () {
    // Se o objeto window.WebSocket não existe, imprimimos uma mensagem no console
    // e retornamos null
    
    if (!window.WebSocket) {
        return null;
    }
 
    // Vamos instanciar um novo objeto WebSocket e passar uma url específica ou no
    // endereço de ip '127.0.0.1' através do protocolo 'ws' na porta 1337
    conexao = new WebSocket('ws://127.0.0.1:1337');

    // 'onopen' é executado quando o cliente é conectado
    conexao.onopen = function () {
    };
 
    // 'onerror' é executado sempre que temos um erro na conexão
    conexao.onerror = function (error) {
    };
 
    // 'onmessage' é executado sempre que temos uma mensagem chegando do servidor
    conexao.onmessage = function (message) {
        document.getElementById("tabela_elementos").innerHTML="";
        
        // vamos tentar fazer um parse do objeto 'message.data' que é passado como
        // argumento do callback. Caso consigamos uma variável json é criada com
        // o parse de 'message.data', se não, imprimimos no console e retornamos o método.
        try{
            var json = JSON.parse(message.data);
            ordenarPorDistancia(json);
        }catch(e){
        }
        if(json != null){
            for (i=0; i < json.length; i++){
                if(json[i]["cidade"] == 'None' || json[i]["cidade"] == ''){
                    $("table#tabela tbody")
                    .append('<tr><th>' + (i+1) + '</th><td>' + json[i]["nome"] + ' </td><td>' + json[i]["distancia"] + '</td><td>' + json[i]["moedas"] + '</td><td> - </td></tr>')
                    .closest("table#tabela")
                    //.table("refresh")
                    .trigger("create");
                }else{
                    $("table#tabela tbody")
                    .append('<tr><th>' + (i+1) + '</th><td>' + json[i]["nome"] + ' </td><td>' + json[i]["distancia"] + '</td><td>' + json[i]["moedas"] + '</td><td><a href="http://localhost:8000/localizacao.html?jogador=' + json[i]["nome"] + '&localizacao=' + json[i]["cidade"] + '">' + json[i]["cidade"] + '</a></td></tr>')
                    .closest("table#tabela")
                    //.table("refresh")
                    .trigger("create");
                }
            }         
        }
    };
};

function ordenarPorDistancia(recorde) {
    recorde.sort(function(a, b) {
        return (b["distancia"] - a["distancia"]);
    });
}
