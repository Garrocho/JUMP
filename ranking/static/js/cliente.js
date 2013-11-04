// link API geolocalização: 
//https://developers.google.com/maps/documentation/javascript/geocoding?hl=pt-br

// criamos uma variável 'conexao'
var conexao = null;

// depois do carregamento da página, chamamos 'setConexao' e 'setEventos'
window.onload = function(){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(function(position){
            var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            var geocoder = new google.maps.Geocoder();
            var endereco;
            geocoder.geocode({'latLng': pos}, function(results, status){
                if(status == google.maps.GeocoderStatus.OK){
                    if(results[1]){
                        var endereco = results[5].formatted_address;
                        setConexao(endereco);
                        console.log(endereco);
                    }
                }else{
                    alert("Erro no serviço de geolocalização: " + status);
                }
            });
            
            //console.log(dados_localizacao[1]);            
        }, function(){
                handleNoGeolocation(true);
        });
    }else{
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
    }   
    //setConexao();
}
 
var setConexao = function (endereco) {
	// Se o objeto window.WebSocket não existe, imprimimos uma mensagem no console
	// e retornamos null
	
	var dados_localizacao = endereco.split(", ");
	console.log(dados_localizacao[0]);
	
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

        document.getElementById("tabela_elementos").innerHTML="";
        
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
                $("table#tabela tbody")
                .append('<tr><th>' + (i+1) + '</th><td>' + json[i]["nome"] + ' </td><td>' + json[i]["distancia"] + '</td><td>' + json[i]["moedas"] + '</td><td><a href="http://127.0.0.1:8000/static/localizacao.html">' + dados_localizacao[1] + '</a></td></tr>')
                .closest("table#tabela")
                .table("refresh")
                .trigger("create");
            }
    };
}

function ordenarPorDistancia(recorde) {
    recorde.sort(function(a, b) {
        return (b["distancia"] - a["distancia"]) ;
    });
}

function handleNoGeolocation(errorFlag) {
    if(errorFlag) {
        var content = 'Erro no serviço de geolocaliazção.';
    }else{
        var content = 'Seu navegador não suporta o serviço de geolocalização.';
    }
}
