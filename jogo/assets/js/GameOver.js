BasicGame.GameOver = function (game) {
    this.ALFABETO = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
    this.nome = "";
    this.tempo = 0;
    this.localizacao = "não identificado";
};

BasicGame.GameOver.prototype = {
    create: function () {
        this.fundo1 = this.add.tileSprite(0, 0, 1024, 512, 'nuvem');
        this.fundo2 = this.add.tileSprite(0, 512, 1024, 512, 'nuvem');
        this.som_musica = this.add.audio('game_over');
        
        this.estilo1 = { font: "bold 80pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 15 };
        this.estilo2 = { font: "bold 30pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 10 };
        this.estilo3 = { font: "bold 25pt Arial", fill: "#ffffff", align: "left", stroke: "#10661343", strokeThickness: 3 };
        this.estilo = { font: "bold 30pt Arial", fill: "#ffffff", stroke: "#000000", strokeThickness: 7 };
        this.titulo = this.add.text(20, 0, "Fim de Jogo!", this.estilo1);
        this.titulo1 = this.add.text(30, 150, "Você Morreu!\nEntre Com Seu Nome Para Registrar Seu Recorde no Ranking!", this.estilo3);
        this.titulo2 = this.add.text(10, 710, "", this.estilo2);
        this.recorde = JSON.parse(localStorage['recorde']);
        this.informacao = "\nMoedas: " + this.recorde['moedas'] + "\nVelocidade: " + this.recorde['kmh'] + " Km/h";
        this.texto = this.add.text(215, 450, this.informacao, this.estilo);
        this.texto.anchor.setTo(0.5, 0.5);
        this.botao_sair = this.add.button(760, 700, 'botao_sair', this.menu, this, 2, 1, 0);
        if (this.stage.scale.isFullScreen == null)
            this.botao_tela = this.add.button(this.world.centerX + 370, 2, 'botao_tela_cheia', this.mudar_tela, this, 2, 1, 0);
        else
            this.botao_tela = this.add.button(this.world.centerX + 370, 2, 'botao_tela_normal', this.mudar_tela, this, 2, 1, 0);

        this.som_musica.play();
        this.botao_som = this.add.button(this.world.centerX + 445, 0, 'botao_som_on', this.mudar_som, this, 2, 1, 0);
        this.valida_config();
    },

    update: function () {
        this.fundo1.tilePosition.x -= 0.5;
        this.fundo2.tilePosition.x -= 1;
        this.processa_letras();
        this.texto.setText("NOME: " + this.nome + this.informacao);
        if (this.nome.length > 3)
            this.titulo2.setText("Pressione Enter Para Continuar!")
        else
            this.titulo2.setText("");
    },

    menu: function (pointer) {
        this.som_musica.stop();
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
                            this.enviar_recorde(this.recorde);
                            this.menu();
                        }
                        else if (this.nome.length > 3) {
                            this.recorde['nome'] = this.nome;
                             this.enviar_recorde(this.recorde);
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
                    this.tempo = this.time.now + 165;
                }
            }
        }
    },

    mudar_tela: function() {
        if (this.stage.scale.isFullScreen == null) {
            this.stage.scale.startFullScreen();
            this.botao_tela.loadTexture('botao_tela_normal');
        }
        else {
            this.stage.scale.stopFullScreen();
            this.botao_tela.loadTexture('botao_tela_cheia');
        }
    },

    mudar_som: function () {
        if (this.som == 0) {
            this.botao_som.loadTexture('botao_som_on');
            this.som = 1;
        }
        else {
            this.botao_som.loadTexture('botao_som_off');
            this.som = 0;
        }
        this.som_musica.volume = this.som;
        if(typeof(Storage)!=="undefined")
            localStorage.setItem('jump_som', this.som);
    },
    
    valida_config: function() {
        if(typeof(Storage)!=="undefined")
            this.som = localStorage.getItem('jump_som');
        else
            this.som = 1
        if (this.som == null)
            this.som = 1;
        else
            this.som = parseInt(this.som);
        if (this.som == 0)
            this.botao_som.loadTexture('botao_som_off');
        else
            this.botao_som.loadTexture('botao_som_on');
        this.som_musica.volume = this.som;
    },
    
    enviar_recorde: function(recorde) {
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(function(position) {
                var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                var geocoder = new google.maps.Geocoder();
                geocoder.geocode({'latLng': pos}, function(results, status) {
                    if(status == google.maps.GeocoderStatus.OK){
                        if (results[1]){
                            lista_dados = results[0].formatted_address.split(", ");
                            cidade = lista_dados[2];
                            if (window.WebSocket) {
                                    recorde['localizacao'] = cidade;
                                    var conexao = new WebSocket('ws://127.0.0.1:1337');
                                    conexao.onopen = function(){
                                        conexao.send(JSON.stringify(recorde));
                                    };
                                } 
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
