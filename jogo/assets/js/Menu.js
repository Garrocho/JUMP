BasicGame.Menu = function (game) {
	this.musica = null;
	this.botao_jogar = null;
};

BasicGame.Menu.prototype = {

	create: function () {
	    this.fundo1 = this.add.tileSprite(0, 0, 1024, 512, 'nuvem');
	    this.fundo2 = this.add.tileSprite(0, 512, 1024, 512, 'nuvem');
		this.musica = this.add.audio('som_musica');
		this.musica.play('',0,1,true);
		this.estilo = { font: "bold 150pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 15 };
		this.estilo2 = { font: "bold 22pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 5 };
		this.estilo3 = { font: "bold 40pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 8 };
        this.titulo = this.add.text(this.world.centerX, this.world.centerY-270, "JUMP!", this.estilo);
        this.titulo.anchor.setTo(0.5, 0.5);
        this.titulo2 = this.add.text(this.world.centerX, this.world.centerY-160, "Jogo Unificado para Movimentação Projetada", this.estilo2);
        this.titulo2.anchor.setTo(0.5, 0.5);
		this.botao_jogar = this.add.button(this.world.centerX - 290, 330, 'botao_jogar', this.novo_jogo, this, 2, 1, 0);
		if (this.stage.scale.isFullScreen == null)
	        this.botao_tela = this.add.button(this.world.centerX + 30, 330, 'botao_tela_cheia', this.mudar_tela, this, 2, 1, 0);
	    else
	        this.botao_tela = this.add.button(this.world.centerX + 30, 330, 'botao_tela_normal', this.mudar_tela, this, 2, 1, 0);
		
		if (window.WebSocket) {
            this.conexao = new WebSocket('ws://108.59.6.230:14527');
            this.conexao.onmessage = function(message) {
                var json = JSON.parse(message.data);
                this.rank = "RANK";
                this.nome = "NOME";
                this.distancia = "DISTANCIA";
                this.moedas = "MOEDAS";
                this.localizacao = "LOCALIZAÇÃO";
                json.sort(function(a, b) {
                    return (b["distancia"] - a["distancia"]);
                });
                if(json != null){
                    for (i=0; i < json.length; i++){
                        if (i == 6)
                            break;
                        this.rank += "\n" + (i+1);
                        this.nome += "\n" + json[i]["nome"];
                        this.distancia += "\n" + json[i]["distancia"];
                        this.moedas += "\n" + json[i]["moedas"];
                        this.localizacao += "\n" + json[i]["localizacao"];
                    }
                }
            }
        }
        
        this.titulo3 = this.add.text(-10, this.world.centerY-120, "----------------------------------------------------------------------------------------", this.estilo3);        
        this.titulo3 = this.add.text(-10, this.world.centerY, "----------------------------------------------------------------------------------------", this.estilo3);
        
        this.rank = this.add.text(50, 610, "", this.estilo2);
        this.rank.anchor.setTo(0.5, 0.5);
        this.nome = this.add.text(200, 610, "", this.estilo2);
        this.nome.anchor.setTo(0.5, 0.5);
        this.distancia = this.add.text(400, 610, "Carregando Ranking, aguarde...", this.estilo2);
        this.distancia.anchor.setTo(0.5, 0.5);
        this.moedas = this.add.text(650, 610, "", this.estilo2);
        this.moedas.anchor.setTo(0.5, 0.5);        
        this.localizacao = this.add.text(900, 610, "", this.estilo2);
        this.localizacao.anchor.setTo(0.5, 0.5);
	},

	update: function () {
	    this.fundo1.tilePosition.x -= 0.5;
	    this.fundo2.tilePosition.x -= 1;
	    if (this.conexao.nome != undefined) {
	        this.rank.setText(this.conexao.rank);
	        this.nome.setText(this.conexao.nome);
	        this.distancia.setText(this.conexao.distancia);
	        this.moedas.setText(this.conexao.moedas);
	        this.localizacao.setText(this.conexao.localizacao);
	    }
	},

	novo_jogo: function (pointer) {
		this.musica.stop();
		this.game.state.start('Jogo');
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
};
