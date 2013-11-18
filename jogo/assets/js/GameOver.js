// link: https://developers.google.com/maps/documentation/javascript/geocoding?hl=pt-br

BasicGame.GameOver = function (game) {
	this.musica = null;
	this.input;
	this.time;
	this.ALFABETO = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
	this.nome = "";
	this.tempo = 0;
	this.localizacao = "não identificado";
};

BasicGame.GameOver.prototype = {
	create: function () {
	    this.fundo1 = this.add.tileSprite(0, 0, 1024, 512, 'nuvem');
	    this.fundo2 = this.add.tileSprite(0, 512, 1024, 512, 'nuvem');
		this.musica = this.add.audio('som_musica');
		this.musica.play('',0,1,true);
		
        this.estilo1 = { font: "bold 80pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 15 };
        this.estilo2 = { font: "bold 30pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 10 };
        this.estilo = { font: "bold 30pt Arial", fill: "#ffffff", stroke: "#000000", strokeThickness: 7 };
        this.titulo = this.add.text(0, 0, "Game Over!", this.estilo1);
        this.titulo2 = this.add.text(0, 720, "Descreva Melhor Seu Nome e Pressione Enter", this.estilo2);
        this.texto = this.add.text(300, 400, this.informacao, this.estilo);
        this.texto.anchor.setTo(0.5, 0.5);
        this.recorde = JSON.parse(localStorage['recorde']);
        this.informacao = "Moedas: " + this.recorde['moedas'] + "\nVelocidade: " + this.recorde['kmh'] + " Km/h\n\nNOME: ";
        this.botao_sair = this.add.button(750, 25, 'botao_sair', this.menu, this, 2, 1, 0);        
        this.localizacao = this.iniciar();
	},

	update: function () {
	    this.fundo1.tilePosition.x -= 0.5;
	    this.fundo2.tilePosition.x -= 1;
	    this.processa_letras();
	    this.texto.setText(this.informacao + this.nome);
	    if (this.nome.length > 3)
	        this.titulo2.setText("Seu Nome Está OK! Pressione Enter Para Continuar!")
	    else
	        this.titulo2.setText("Descreva Melhor Seu Nome!");
	},

	menu: function (pointer) {
		this.musica.stop();
		this.game.state.start('Menu');
	},
	
	processa_letras: function () {
	    for (i=8; i <= 90; i++) {
	        if (this.input.keyboard._keys[i] != undefined && this.input.keyboard._keys[i].isDown) {
	            if (this.time.now > this.tempo) {
	                if (i == 8) {
	                    this.nome = this.nome.substring(0, this.nome.length-1);
	                }
                    else if (i == 13 || i == 27) {
	                    if (this.nome.length == 0) {
		                    this.nome = "NAO DEFINIDO";
		                    this.menu();
                        }
                        else if (this.nome.length > 3) {
                            this.menu();
                        }
                    }
                    else if (i == 32) {
	                    this.nome += " ";
	                }
	                else if (i >= 65 && i <= 90){
                        var chave = i-65;
                        if (chave < this.ALFABETO.length && chave >= 0) {
	                        if (this.nome.length < 8) {
		                        this.nome += this.ALFABETO[chave];
		                    }
		                }
                    }
                    this.tempo = this.time.now + 180;
                }
            }
        }
	},
	
	iniciar: function() {
        // Try HTML5 geolocation
        
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(function(position) {
                var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                var geocoder = new google.maps.Geocoder();
                geocoder.geocode({'latLng': pos}, function(results, status) {
                    if(status == google.maps.GeocoderStatus.OK){
                        if (results[1]){
                            lista_dados = results[0].formatted_address.split(", ");
                            gerarJson(lista_dados[2]);
                         }
                     }else{
                        alert("Erro no serviço de geolocalização: " + status);
                     }
                     }, function(){
                        this.handleNoGeolocation(true); 
                     }
                 )
            });
        }else{
            // Browser doesn't support Geolocation
            this.handleNoGeolocation(false);
        }
    },
    
    handleNoGeolocation: function(errorFlag) {
        if(errorFlag) {
            var content = 'Erro no serviço de geolocaliazção.';
        }else{
            var content = 'Seu navegador não suporta o serviço de geolocalização.';
        }
    }
};

function gerarJson(cidade){
    alert(cidade);
}
