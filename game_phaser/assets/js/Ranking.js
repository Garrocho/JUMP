BasicGame.Ranking = function (game) {
	this.musica = null;
};

BasicGame.Ranking.prototype = {

	create: function () {
	    this.fundo1 = this.add.tileSprite(0, 0, 1024, 512, 'nuvem');
	    this.fundo2 = this.add.tileSprite(0, 512, 1024, 512, 'nuvem');
		this.musica = this.add.audio('som_musica');
		this.musica.play('',0,1,true);
		
		if (window.WebSocket) {
            this.conexao = new WebSocket('ws://127.0.0.1:1337');
            this.conexao.onmessage = function(message) {
                var json = JSON.parse(message.data);
                this.rank = "RANK";
                this.nome = "NOME";
                this.distancia = "DISTANCIA";
                this.moedas = "MOEDAS";
                json.sort(function(a, b) {
                    return (b["distancia"] - a["distancia"]);
                });
                if(json != null){
                    for (i=0; i < json.length; i++){
                        if (i == 15)
                            break;
                        this.rank += "\n" + (i+1);
                        this.nome += "\n" + json[i]["nome"];
                        this.distancia += "\n" + json[i]["distancia"];
                        this.moedas += "\n" + json[i]["moedas"];
                    }
                }
            }
        }
        this.estilo1 = { font: "bold 60pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 15 };
        this.estilo = { font: "bold 22pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 5 };
        this.titulo = this.add.text(0, 0, "Ranking do JUMP!", this.estilo1);
        
        this.rank = this.add.text(50, 450, "RANK", this.estilo);
        this.rank.anchor.setTo(0.5, 0.5);
        this.nome = this.add.text(250, 450, "NOME", this.estilo);
        this.nome.anchor.setTo(0.5, 0.5);
        this.distancia = this.add.text(600, 450, "DISTANCIA", this.estilo);
        this.distancia.anchor.setTo(0.5, 0.5);
        this.moedas = this.add.text(900, 450, "MOEDAS", this.estilo);
        this.moedas.anchor.setTo(0.5, 0.5);
        
        this.botao_sair = this.add.button(750, 25, 'botao_sair', this.menu, this, 2, 1, 0);
	},

	update: function () {
	    this.fundo1.tilePosition.x -= 0.5;
	    this.fundo2.tilePosition.x -= 1;
	    if (this.conexao.nome != undefined) {
	        this.rank.setText(this.conexao.rank);
	        this.nome.setText(this.conexao.nome);
	        this.distancia.setText(this.conexao.distancia);
	        this.moedas.setText(this.conexao.moedas);
	    }
	},

	menu: function (pointer) {
		this.musica.stop();
		this.conexao.close();
		this.game.state.start('Menu');
	},
};
