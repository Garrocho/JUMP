BasicGame.GameOver = function (game) {
	this.musica = null;
	this.input;
	this.time;
	this.ALFABETO = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
	this.nome = "";
	this.tempo = 0;
};

BasicGame.GameOver.prototype = {

	create: function () {
	    this.fundo1 = this.add.tileSprite(0, 0, 1024, 512, 'nuvem');
	    this.fundo2 = this.add.tileSprite(0, 512, 1024, 512, 'nuvem');
		this.musica = this.add.audio('som_musica');
		this.musica.play('',0,1,true);
		
        this.estilo1 = { font: "bold 60pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 15 };
        this.estilo = { font: "bold 22pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 5 };
        this.titulo = this.add.text(0, 0, "Game Over!", this.estilo1);
        
        this.moeda_cont = this.add.sprite(200, 400, 'moeda');
        this.moeda_cont.animations.add('correr');
        this.moeda_cont.animations.play('correr', 10, true);
        
        this.corredor_cont = this.add.sprite(200, 500, 'correndo_min');
        this.corredor_cont.animations.add('correr');
        this.corredor_cont.animations.play('correr', 10, true);
        
        this.estilo = { font: "bold 20pt Arial", fill: "#ffffff", stroke: "#000000", strokeThickness: 3 };
        this.texto1 = this.add.text(250, 400, this.contador, this.estilo);
        this.texto1.anchor.setTo(0.5, 0.5);
        this.texto2 = this.add.text(250, 500, this.kmh, this.estilo);
        this.texto2.anchor.setTo(0.5, 0.5);
        
        this.texto = this.add.text(250, 450, "SEU NOME: ", this.estilo);
        this.texto.anchor.setTo(0.5, 0.5);
        
        this.botao_sair = this.add.button(750, 25, 'botao_sair', this.menu, this, 2, 1, 0);
	},

	update: function () {
	    this.fundo1.tilePosition.x -= 0.5;
	    this.fundo2.tilePosition.x -= 1;
	    this.processa_letras();
	    this.texto.setText("NOME: " + this.nome);
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
                        console.log(i);
                        var chave = i-65;
                        if (chave < this.ALFABETO.length && chave >= 0) {
	                        if (this.nome.length < 10) {
	                            console.log(this.ALFABETO[chave]);
		                        this.nome += this.ALFABETO[chave];
		                    }
		                }
                    }
                    this.tempo = this.time.now + 250;
                }
            }
        }
	},
};
