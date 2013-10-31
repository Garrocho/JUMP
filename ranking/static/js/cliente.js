// criamos uma variável 'conexao'
var conexao = null;
 
// depois do carregamento da página, chamamos 'setConexao' e 'setEventos'
window.onload = function () {
    setConexao();
}
 
var setConexao = function () {
	// Se o objeto window.WebSocket não existe, imprimimos uma mensagem no console
	// e retornamos null
    if (!window.WebSocket) {
        console.log('O seu browser falhou com voce e nao pode abrir essa conexao');
        return null;
    }
 
    // Vamos instanciar um novo objeto WebSocket e passar uma url específica ou no
    // endereço de ip '127.0.0.1' através do protocolo 'ws' na porta 1337
    conexao = new WebSocket('ws://127.0.0.1:1337');

    // 'onopen' é executado quando o cliente é conectado
    conexao.onopen = function () {
        console.log('conexao aberta')
    };
 
    // 'onerror' é executado sempre que temos um erro na conexão
    conexao.onerror = function (error) {
        console.log('Erro na conexao');
    };
 
    // 'onmessage' é executado sempre que temos uma mensagem chegando do servidor
    conexao.onmessage = function (message) {

        document.getElementById("lista").innerHTML="";
        
        // vamos tentar fazer um parse do objeto 'message.data' que é passado como
        // argumento do callback. Caso consigamos uma variável json é criada com
        // o parse de 'message.data', se não, imprimimos no console e retornamos o método.
        try {
                var json = JSON.parse(message.data);
                ordenarPorDistancia(json);
            } catch (e) {
                json = JSON.parse(json);
                ordenarPorDistancia(json);
            }
            for (i=0; i < json.length; i++) {
                console.log(json[i]);
                $('#lista').append('<li>' + json[i]["nome"] + '<span class="ui-li-count">' + json[i]["distancia"] + ' Metros</span></li>').listview('refresh');
            }
    };
}

function ordenarPorDistancia(recorde) {
    recorde.sort(function(a, b) {
        return (b["distancia"] - a["distancia"]) ;
    });
}